from aiogram import types

import db
import metering
from main import bot, dp


@dp.message_handler(commands=['start'])
async def print_info(message: types.Message):
    text = "Hello"
    await message.answer(text=text)
    db.add_user(message)

@dp.message_handler(regexp=r"^([1-9]\d{1,2}) ([1-9]\d{1,2}) ([1-9]\d{1,2})$")
async def write_metering(message: types.Message):
    user = message.from_user.id
    date = message.date.date()
    metering_result = message.text
    hour = int(message.date.strftime('%H'))

    column = metering.determine_the_time(hour)
    text = metering.write_to_db(user, date, column, metering_result)
    await message.answer(text)

@dp.message_handler()
async def wrong_message(message: types.Message):
    await message.answer('Некорректный формат ввода')
