import db
import metering
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery
from keyboards.inline.access_buttons import cancel_state, open_user_cmd, open_users
from keyboards.inline.callback_data import open_users_callback, state_callback, user_cmd_callback
from main import dp
from states.access_state import Access


@dp.message_handler(commands=['open_access'], state=None)
async def open_access_command(message: types.Message):
    text = 'Введите юзернейм или айди пользователся, чтобы открыть ему доступ'
    await message.answer(text=text, reply_markup=cancel_state)
    await Access.Q1.set()


@dp.message_handler(state=Access.Q1)
async def open_for(message: types.Message, state: FSMContext):
    user = message.from_user.id
    open_for = message.text

    all_users = db.read_users()
    text = "Список пользователей пуст"
    for row in all_users:
        if open_for == row[1] or open_for == row[0]:
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
            break
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


@dp.callback_query_handler(state_callback.filter(command="cancel"), state=Access.Q1)
async def cancel_q1(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=2)
    await state.finish()
    await call.message.answer(
        text='Действие отменено'
    )


@dp.message_handler(commands=['user_results'])
async def select_user(message: types.Message):
    observer = message.from_user.id

    text = "Результаты какого пользователя вы бы хотели посмотреть?"
    await message.answer(text, reply_markup=open_users(observer))


@dp.callback_query_handler(open_users_callback.filter())
async def select_category(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)
    user = callback_data.get("user")
    text = "Какую категорию вы бы хотели посмотреть?"
    await call.message.edit_text(text, reply_markup=open_user_cmd(user))
    # await call.message.edit_reply_markup(open_user_cmd(user))


@dp.callback_query_handler(user_cmd_callback.filter(cmd="today"))
async def show_today(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)
    user = callback_data.get("user")
    date = call.message.date.date()
    text = metering.show_today_meterings(user, date)
    await call.message.answer(text)


@dp.callback_query_handler(user_cmd_callback.filter(cmd="this_month"))
async def show_user_month(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)
    user = callback_data.get("user")
    date = call.message.date.date()
    year = date.strftime('%Y')
    month = date.strftime('%m')

    text = metering.show_monthly_meterings(user, year, month)
    await call.message.answer(text)


# TODO
# @dp.callback_query_handler(user_cmd_callback.filter(cmd="by_month"))
# async def show_user_by_month(call: CallbackQuery, callback_data: dict):
#     await call.answer(cache_time=2)
#     user = callback_data.get("user")


@dp.callback_query_handler(user_cmd_callback.filter(cmd="back"))
async def back_to_users(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)
    observer = call.from_user.id

    text = "Результаты какого пользователя вы бы хотели посмотреть?"
    await call.message.edit_text(text, reply_markup=open_users(observer))
