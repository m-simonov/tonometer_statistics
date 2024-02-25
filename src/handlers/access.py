from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

from common.utils import log_call
from keyboards.inline.access_buttons import (cancel_state, open_user_cmd,
                                             open_users)
from keyboards.inline.callback_data import (open_users_callback,
                                            state_callback, user_cmd_callback)
from main import dp
from services.access_rights import AccessRightsService
from services.measurement import MeasurementService
from states.access_state import Access


@dp.message_handler(commands=['open_access'], state=None)
@log_call
async def open_access_command(message: types.Message):
    text = 'Введите юзернейм или айди пользователся, чтобы открыть ему доступ'
    await message.answer(text=text, reply_markup=cancel_state)
    await Access.Q1.set()


@dp.message_handler(state=Access.Q1)
async def open_for(message: types.Message, state: FSMContext):
    user = message.from_user.id
    open_for = message.text
    text = await AccessRightsService().open_access(user, open_for)

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
@log_call
async def select_user(message: types.Message):
    observer = message.from_user.id

    text = "Результаты какого пользователя вы бы хотели посмотреть?"
    reply_markup = await open_users(observer)
    await message.answer(text, reply_markup=reply_markup)


@dp.callback_query_handler(open_users_callback.filter())
async def select_category(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)
    user = callback_data.get("user")
    text = "Какую категорию вы бы хотели посмотреть?"
    await call.message.edit_text(text, reply_markup=open_user_cmd(user))


@dp.callback_query_handler(user_cmd_callback.filter(cmd="today"))
async def show_today(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)
    text = await MeasurementService().get_measurements(
        tid=callback_data.get("user"),
        date=call.message.date.date(),
    )
    await call.message.answer(text, parse_mode="HTML")


@dp.callback_query_handler(user_cmd_callback.filter(cmd="this_month"))
async def show_user_month(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)
    date = call.message.date.date()

    text = await MeasurementService().get_month_measurements(
        tid=callback_data.get("user"),
        year=date.year,
        month=date.month,
    )
    await call.message.answer(text, parse_mode="HTML")


# @TODO
@dp.callback_query_handler(user_cmd_callback.filter(cmd="by_month"))
async def show_user_by_month(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)
    # tid = callback_data.get("user")

    # reply_markup = await ButtonService().get_by_month_reply_markup(tid)
    # await call.message.answer(
    #     text="За какой месяц вывести результаты замеров?",
    #     reply_markup=reply_markup,
    # )
    await call.message.answer(text="Функция находится в разработке")


@dp.callback_query_handler(user_cmd_callback.filter(cmd="back"))
async def back_to_users(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)
    observer = call.from_user.id

    text = "Результаты какого пользователя вы бы хотели посмотреть?"
    reply_markup = await open_users(observer)
    await call.message.edit_text(text, reply_markup=reply_markup)
