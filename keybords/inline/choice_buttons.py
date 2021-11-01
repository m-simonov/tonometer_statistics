from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from .callback_data import by_month_callback


by_month = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Январь", callback_data=by_month_callback.new(
                month="01"
            )),
            InlineKeyboardButton(text="Июль", callback_data=by_month_callback.new(
                month="07"
            )),
        ],
        [
           InlineKeyboardButton(text="Февраль", callback_data=by_month_callback.new(
               month="02"
           )),
           InlineKeyboardButton(text="Август", callback_data=by_month_callback.new(
               month="08"
           )),
        ],
        [
           InlineKeyboardButton(text="Март", callback_data=by_month_callback.new(
               month="03"
           )),
           InlineKeyboardButton(text="Сентябрь", callback_data=by_month_callback.new(
               month="09"
           )),
        ],
        [
           InlineKeyboardButton(text="Апрель", callback_data=by_month_callback.new(
               month="04"
           )),
           InlineKeyboardButton(text="Октябрь", callback_data=by_month_callback.new(
               month="10"
           )),
        ],
        [
           InlineKeyboardButton(text="Май", callback_data=by_month_callback.new(
               month="05"
           )),
           InlineKeyboardButton(text="Ноябрь", callback_data=by_month_callback.new(
               month="11"
           )),
        ],
        [
           InlineKeyboardButton(text="Июнь", callback_data=by_month_callback.new(
               month="06"
           )),
           InlineKeyboardButton(text="Декабрь", callback_data=by_month_callback.new(
               month="12"
           )),
        ],
    ]
)