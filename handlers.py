from datetime import date
from aiogram import types
from aiogram.types import message_auto_delete_timer_changed

import db
import metering
from main import bot, dp


@dp.message_handler(commands=['start'])
async def print_info(message: types.Message):
    text = (
        "Привет! Этот бот предназначен для ведения дневника давления.\n\n"
        "Результаты замеров фиксируются после отправки сообщения "
        "в следующем формате:\nСистолическое давление, "
        "диастолическое и пульс. Данные вводятся через пробел "
        "(например: 120 80 60)."
        "\nДалее бот, в зависимости от времени отправки сообщения, "
        "внесет замер в соответствующую категорию: "
        "утро, день или вечер.\n\n"
        "Дополнительные функции доступны по нажатию на иконку меню "
        "слева от поля ввода сообщения."
    )
    await message.answer(text=text)
    db.add_user(message)

@dp.message_handler(commands=['today_results'])
async def show_today_meterings(message: types.Message):
    user = message.from_user.id
    date = message.date.date()
    text = metering.show_meterings(user, date)
    await message.answer(text)

@dp.message_handler(regexp=r"^([1-9]\d{1,2}) ([1-9]\d{1,2}) ([1-9]\d{1,2})$")
async def write_metering(message: types.Message):
    user = message.from_user.id
    date = message.date.date()
    metering_result = message.text

    column = metering.determine_the_time()
    text = metering.write_to_db(user, date, column, metering_result)
    await message.answer(text)

@dp.message_handler()
async def wrong_message(message: types.Message):
    await message.answer('Некорректный формат ввода')
