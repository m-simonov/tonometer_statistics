from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from keybords.inline.callback_data import by_month_callback


months = [
    "Январь", "Февраль", "Март", "Апрель",
    "Май", "Июнь", "Июль", "Август",
    "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
]


pairs = [months[i:i + 2] for i in range(0, len(months), 2)]


keyboard = [
    [
        InlineKeyboardButton(text=pair[0], callback_data=by_month_callback.new(month=str(months.index(pair[0]) + 1).zfill(2))),
        InlineKeyboardButton(text=pair[1], callback_data=by_month_callback.new(month=str(months.index(pair[1]) + 1).zfill(2)))
    ] for pair in pairs
]


by_month = InlineKeyboardMarkup(inline_keyboard=keyboard)
