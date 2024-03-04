from aiogram import types

from main import dp
from services.user import UserService
from settings import ADMINS__ID


def auth_admin(func):
    async def wrapper(message):
        if message.from_user.id not in ADMINS__ID:
            return await message.answer(text='Access Denied')
        return await func(message)
    return wrapper


@dp.message_handler(commands=['ppl'])
@auth_admin
async def show_users(message: types.Message):
    text = await UserService().get_users_list()
    await message.answer(text or "Empty")
