import sqlite3
import datetime
import pytz

from aiogram import types

from main import bot, dp


@dp.message_handler(commands=['start'])
async def print_info(message: types.Message):
    text = "Hello"
    await message.answer(text=text)

    base = sqlite3.connect('tonometer_results.db')
    cur = base.cursor()

    tid = message.from_user.id
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    base.execute('CREATE TABLE IF NOT EXISTS users(tid PRIMARY KEY, username, fitst_name, last_name)')
    cur.execute('INSERT OR IGNORE INTO users VALUES(?, ?, ?, ?)', (tid, user_name, first_name, last_name))
    base.commit()
    base.close()