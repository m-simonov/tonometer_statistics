from aiogram.types.callback_query import CallbackQuery
import db
import metering
from aiogram import types
from main import bot, dp
from keybords.inline.choice_buttons import by_month
from keybords.inline.callback_data import by_month_callback

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