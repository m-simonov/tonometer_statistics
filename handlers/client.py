import os
from datetime import datetime

import db
import matplotlib.pyplot as plt
import metering
from aiogram import types
from aiogram.types.base import InputFile
from aiogram.types.callback_query import CallbackQuery
from keybords.inline.callback_data import by_month_callback
from keybords.inline.choice_buttons import by_month
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
    text = metering.show_today_meterings(user, date)
    await message.answer(text)

@dp.message_handler(commands=['this_month_results'])
async def show_this_months_meterings(message: types.Message):
    user = message.from_user.id
    date = message.date.date()
    year = date.strftime('%Y')
    month = date.strftime('%m')

    text = metering.show_monthly_meterings(user, year, month)
    await message.answer(text)    

@dp.message_handler(commands=['by_month_results'])
async def by_month_command(message: types.Message):
    await message.answer(
        text="За какой месяц вывести результаты замеров?",
        reply_markup=by_month
        )

@dp.callback_query_handler(by_month_callback.filter())
async def show_meterings_by_month(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)
    user = call.from_user.id
    month = callback_data.get("month")
    year = call.message.date.strftime('%Y')
    
    text = metering.show_monthly_meterings(user, year, month)
    if text:
        await call.message.answer(text=text)
    else:
        await call.message.answer(text="Нет данных")

@dp.message_handler(commands=['show_month_graph'])
async def show_month_graph(message: types.Message):
    user = message.from_user.id
    date = message.date.date()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    month_results = db.read_monthly_meterings(user, year, month)

    days = []
    morning_sys = []
    morning_dia = []
    morning_pulse = []
    afternoon_sys = []
    afternoon_dia = []
    afternoon_pulse = []
    evening_sys = []
    evening_dia = []
    evening_pulse = []
    for row in month_results:
        days.append(datetime.strptime(f'{row[2]}', '%Y-%m-%d').strftime('%d'))
        morning_res = row[3]
        afternoon_res = row[4]
        evening_res = row[5]
        if morning_res:
            morning_sys.append(int(morning_res.split()[0]))
            morning_dia.append(int(morning_res.split()[1]))
            morning_pulse.append(int(morning_res.split()[2]))
        else:
            morning_sys.append(0)
            morning_dia.append(0)
            morning_pulse.append(0)
    
    bar = plt.bar(days, morning_sys)
    plt.title("This month morning results")
    plt.xlabel("Days")
    plt.ylabel("SYS")

    for rect, res in zip(bar, morning_sys):
        height = rect.get_height()
        plt.text(rect.get_x(), height, res)

    plt.savefig("test_1.png")

    img = open("test_1.png", "rb")
    os.remove("test_1.png")

    await message.answer_photo(photo=img)

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
