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
    metering_result = message.text
    column = metering.determine_the_time()

    text = metering.write_to_db(user, metering_result, column)
    await message.answer(text)

@dp.message_handler()
async def wrong_message(message: types.Message):
    await message.answer('Некорректный формат ввода')
