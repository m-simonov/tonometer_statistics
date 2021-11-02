from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from main import dp
from states.access_state import Access
from keybords.inline.access_buttons import cancel_state
from keybords.inline.callback_data import state_callback
from db import insert


@dp.message_handler(commands=['open_access'], state=None)
async def open_access_command(message: types.Message):
    text = "Введите юзернэйм или айди пользователся, чтобы открыть ему доступ"
    await message.answer(text=text, reply_markup=cancel_state)
    await Access.Q1.set()

@dp.message_handler(state=Access.Q1)
async def open_for(message: types.Message, state: FSMContext):
    user = message.from_user.id
    open = message.text

    await message.answer("Insert to db")
    # insert
    await state.finish()

@dp.callback_query_handler(state_callback.filter(command="cancel"),state=Access.Q1)
async def cancel_q1(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=2)
    await state.finish()
    await call.message.answer(
        text="Действие отменено"
    )