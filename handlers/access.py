import db
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from keybords.inline.access_buttons import cancel_state
from keybords.inline.callback_data import state_callback
from main import dp
from states.access_state import Access


@dp.message_handler(commands=['open_access'], state=None)
async def open_access_command(message: types.Message):
    text = 'Введите юзернейм пользователся, чтобы открыть ему доступ'
    await message.answer(text=text, reply_markup=cancel_state)
    await Access.Q1.set()

@dp.message_handler(state=Access.Q1)
async def open_for(message: types.Message, state: FSMContext):
    user = message.from_user.id
    open_for = message.text
    
    all_users = db.read_users()
    for row in all_users:
        if open_for == row[1]:
            db.insert(
                'access_rights',
                {
                    "user": user,
                    "open_for": row[0]
                }
            )
            text = (
                "Результаты ваших замеров теперь доступны "
                f"пользователю {open_for}"
            )
        else:
            text = (
                f'Не удалось открыть доступ пользователю "{open_for}".\n'
                'Возможные причины:\n'
                '1. Такого пользователя не существует\n'
                f'2. "{open_for}" не является пользователем бота\n'
                '3. Вы ввели неверный юзернейм'
            )

    await message.answer(text)
    await state.finish()

@dp.callback_query_handler(state_callback.filter(command="cancel"),state=Access.Q1)
async def cancel_q1(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=2)
    await state.finish()
    await call.message.answer(
        text='Действие отменено'
    )