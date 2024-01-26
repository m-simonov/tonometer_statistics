from aiogram.utils.callback_data import CallbackData


by_month_callback = CallbackData("by_month", "month")

state_callback = CallbackData("state", "command")

open_users_callback = CallbackData("open_users", "user")
user_cmd_callback = CallbackData("user_cmd", "user", "cmd")