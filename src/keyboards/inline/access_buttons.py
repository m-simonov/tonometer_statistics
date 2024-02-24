from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_data import state_callback, open_users_callback, user_cmd_callback
from services.user import UserService


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


async def open_users(observer: int):
    users = await UserService().get_open_users(observer)
    open_users = InlineKeyboardMarkup(row_width=2)
    for user in users:
        open_users.add(
            InlineKeyboardButton(
                text=f"{user.first_name} {user.last_name or ''} {user.username or ''}",
                callback_data=open_users_callback.new(user=user.tid)
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
