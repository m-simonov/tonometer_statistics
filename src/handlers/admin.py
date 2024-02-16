import os

from aiogram import types
from dotenv import load_dotenv

from main import dp
from services.user import UserService


load_dotenv()
admin_id = os.environ.get('admin_id')


def auth_admin(func):
    async def wrapper(message):
        if str(message.from_user.id) not in admin_id:
            return await message.answer(text='Access Denied')
        return await func(message)
    return wrapper


@dp.message_handler(commands=['ppl'])
@auth_admin
async def show_users(message: types.Message):
    text = await UserService().get_users_list()
    await message.answer(text)
