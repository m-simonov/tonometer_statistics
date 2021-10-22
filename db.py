import sqlite3
from typing import Dict

from aiogram import types


def add_user(message: types.Message):
    base = sqlite3.connect('tonometer.db')
    cur = base.cursor()

    tid = message.from_user.id
    user_name = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    cur.execute(
        "INSERT OR IGNORE INTO "
        "users VALUES(?, ?, ?, ?)",
        (tid, user_name, first_name, last_name)
        )
    base.commit()
    base.close()

def insert(table_name: str, column_values: Dict):
    base = sqlite3.connect('tonometer.db')
    cur = base.cursor()

    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ', '.join('?' * len(column_values.keys()))
    cur.executemany(
        f"INSERT INTO {table_name} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values
    )
    base.commit()
    base.close()
