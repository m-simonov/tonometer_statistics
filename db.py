import sqlite3
from typing import Dict, List

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

def update_metering(user: str, date: str, column: str, value: str):
    base = sqlite3.connect('tonometer.db')
    cur = base.cursor()

    cur.execute(
        "UPDATE meterings "
        f"SET {column} == ? "
        "WHERE user == ? AND date == ?",
        (value, user, date)
    )
    base.commit()
    base.close()

def read_users():
    base = sqlite3.connect('tonometer.db')
    cur = base.cursor()

    selected = cur.execute(
        "SELECT * FROM users"
    ).fetchall()
    base.close()
    return selected

def read_meterings_by_date(user: str, date: str):
    base = sqlite3.connect('tonometer.db')
    cur = base.cursor()

    selected = cur.execute(
        "SELECT morning, afternoon, evening "
        "FROM meterings "
        "WHERE user == ? AND date == ?",
        (user, date)
    ).fetchone()
    base.close()
    return selected

def read_monthly_meterings(user: str, year: str, month: str):
    base = sqlite3.connect('tonometer.db')
    cur = base.cursor()

    selected = cur.execute(
        "SELECT * FROM meterings "
        f"WHERE date LIKE '%{year}-{month}%' "
        "AND user = ?",
        (user,)
    ).fetchall()
    base.close()
    return selected