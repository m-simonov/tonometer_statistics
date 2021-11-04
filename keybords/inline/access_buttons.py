from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from .callback_data import state_callback, open_users_callback
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
    open_users = InlineKeyboardMarkup()
    for user in users:
        open_users.add(
            InlineKeyboardButton(
                text=f"{user[1]}",
                callback_data=open_users_callback.new(user=user[0])
            )
        )
    return open_users