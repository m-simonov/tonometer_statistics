from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from .callback_data import state_callback, open_users_callback, user_cmd_callback
import db


cancel_state = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Отмена",
                callback_data=state_callback.new(command="cancel")
            )
        ]
    ]
)

def open_users(observer: str):
    users = db.read_open_users(observer=observer) 
    open_users = InlineKeyboardMarkup(row_width=2)
    for user in users:
        open_users.add(
            InlineKeyboardButton(
                text=f"{user[1]}",
                callback_data=open_users_callback.new(user=user[0])
            )
        )
    return open_users

def open_user_cmd(user: str):
    user_commands = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Сегодняшние замеры",
                    callback_data=user_cmd_callback.new(
                        user=user,
                        cmd="today"
                    )
                ),
                InlineKeyboardButton(
                    text="Замеры текущего месяца",
                    callback_data=user_cmd_callback.new(
                        user=user,
                        cmd="this_month"
                    )
                )
            ],
            [
                InlineKeyboardButton(
                    text="Выбрать месяц",
                    callback_data=user_cmd_callback.new(
                        user=user,
                        cmd="by_month"
                    )
                ),
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=user_cmd_callback.new(
                        user=user,
                        cmd="back"
                    )
                )
            ]
        ]
    )
    return user_commands