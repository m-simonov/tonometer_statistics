from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from .callback_data import state_callback


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