import datetime
import sqlite3

import pytz
from aiogram import types

import db
from main import bot, dp


@dp.message_handler(commands=['start'])
async def print_info(message: types.Message):
    text = "Hello"
    await message.answer(text=text)
    db.add_user(message)

@dp.message_handler()
async def wtite_results(message: types.Message):
    msk_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    hour = int(msk_time.strftime('%H'))
    date_now = msk_time.date()
    if 0 < hour < 12:
        time = 'morning'
    elif 12 < hour < 18:
        time = 'afternoon'
    else:
        time = 'evening'

    db.insert(
        'meterings',
        {
            'user': message.from_user.id,
            'date': date_now,
            time: message.text,
        }
    )

    await message.answer(f'{result}')
