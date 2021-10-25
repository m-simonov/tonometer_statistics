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
async def write_results(message: types.Message):
    msk_time = datetime.datetime.now(pytz.timezone('Europe/Moscow'))
    hour = int(msk_time.strftime('%H'))
    date_now = msk_time.date()
    if 0 < hour < 12:
        column = 'morning'
    elif 12 < hour < 18:
        column = 'afternoon'
    else:
        column = 'evening'

    user = message.from_user.id
    metering = message.text

    if db.count_meterings(user, date_now) == 3:
        await message.answer('Все данные на сегодня заполнены')
    elif db.count_meterings(user, date_now) == 0:
        db.insert(
            'meterings',
            {
                'user': user,
                'date': date_now,
                column: metering,
            }
        )
    else:
        db.update_metering(
            user,
            date_now,
            column,
            metering,
        )

    await message.answer(f'{metering}')
