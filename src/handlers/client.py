import os
from datetime import datetime

import matplotlib.pyplot as plt
from aiogram import types
from aiogram.dispatcher.storage import FSMContext
from aiogram.types.callback_query import CallbackQuery

import db
from common.utils import log_call
from keyboards.inline.base import cancel_state
from keyboards.inline.callback_data import by_month_callback, state_callback
from logger import logger
from main import bot, dp
from services.button import ButtonService
from services.feedback import FeedbackService
from services.measurement import MeasurementService
from services.user import UserService
from settings import ADMINS__ID
from states.feedback_state import FeedbackState


@dp.message_handler(commands=['start'])
@log_call
@logger.catch
async def print_info(message: types.Message):
    text = (
        "Привет! Этот бот предназначен для ведения дневника давления.\n\n"
        "Результаты замеров фиксируются после отправки сообщения "
        "в следующем формате:\nСистолическое давление, "
        "диастолическое и пульс. Данные вводятся через пробел "
        "(например: 120 80 60)."
        "\nДалее бот, в зависимости от времени отправки сообщения, "
        "внесет замер в соответствующую категорию: "
        "утро, день или вечер.\n\n"
        "Дополнительные функции доступны по нажатию на иконку меню "
        "слева от поля ввода сообщения."
    )
    await message.answer(text=text)
    await UserService().add_user(message)


@dp.message_handler(commands=['today_results'])
@log_call
@logger.catch
async def show_today_measurements(message: types.Message):
    text = await MeasurementService().get_measurements(
        tid=message.from_user.id,
        date=message.date.date(),
    )
    await message.answer(text, parse_mode="HTML")


@dp.message_handler(commands=['this_month_results'])
@log_call
@logger.catch
async def show_this_month_measurements(message: types.Message):
    date = message.date.date()
    text = await MeasurementService().get_month_measurements(
        tid=message.from_user.id,
        year=date.year,
        month=date.month,
    )
    await message.answer(text, parse_mode="HTML")


@dp.message_handler(commands=['by_month_results'])
@log_call
@logger.catch
async def by_month_command(message: types.Message):
    reply_markup = await ButtonService().get_by_month_reply_markup(message.from_user.id)
    await message.answer(
        text="За какой месяц вывести результаты замеров?",
        reply_markup=reply_markup,
    )


@dp.callback_query_handler(by_month_callback.filter())
@logger.catch
async def show_measurements_by_month(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=2)

    text = await MeasurementService().get_month_measurements(
        tid=call.from_user.id,
        year=call.message.date.year,
        month=callback_data.get("month"),
    )
    if text:
        await call.message.answer(text=text, parse_mode="HTML")
    else:
        await call.message.answer(text="Нет данных")


@dp.message_handler(commands=['show_month_graph'])
@log_call
@logger.catch
async def show_month_graph(message: types.Message):
    user = message.from_user.id
    date = message.date.date()
    year = date.strftime('%Y')
    month = date.strftime('%m')
    month_results = db.read_monthly_meterings(user, year, month)

    days = []
    morning_sys = []
    morning_dia = []
    morning_pulse = []
    # afternoon_sys = []
    # afternoon_dia = []
    # afternoon_pulse = []
    # evening_sys = []
    # evening_dia = []
    # evening_pulse = []
    for row in month_results:
        days.append(datetime.strptime(f'{row[2]}', '%Y-%m-%d').strftime('%d'))
        morning_res = row[3]
        # afternoon_res = row[4]
        # evening_res = row[5]
        if morning_res:
            morning_sys.append(int(morning_res.split()[0]))
            morning_dia.append(int(morning_res.split()[1]))
            morning_pulse.append(int(morning_res.split()[2]))
        else:
            morning_sys.append(0)
            morning_dia.append(0)
            morning_pulse.append(0)

    bar = plt.bar(days, morning_sys)
    plt.title("This month morning results")
    plt.xlabel("Days")
    plt.ylabel("SYS")

    for rect, res in zip(bar, morning_sys):
        height = rect.get_height()
        plt.text(rect.get_x(), height, res)

    plt.savefig("test_1.png")

    img = open("test_1.png", "rb")
    os.remove("test_1.png")

    await message.answer_photo(photo=img)


@dp.message_handler(commands=['send_feedback'])
@log_call
@logger.catch
async def start_feedback(message: types.Message):
    await message.answer(
        "Ваш отзыв будет передан разработчику. Пожалуйста, введите сообщение.",
        reply_markup=cancel_state,
    )
    await FeedbackState.waiting_for_feedback.set()


@dp.message_handler(state=FeedbackState.waiting_for_feedback)
@log_call
@logger.catch
async def collect_feedback(message: types.Message, state: FSMContext):
    await bot.send_message(ADMINS__ID[0], f"Новый отзыв от {message.from_user.username} | {message.from_user.id}:\n{message.text}")
    await FeedbackService().add_feedback(message.from_user.id, message.text)
    await message.answer("Спасибо за отзыв! Ваше сообщение было передано разработчику.")
    await state.finish()


@dp.callback_query_handler(state_callback.filter(command="cancel"), state=FeedbackState.waiting_for_feedback)
async def cancel_q1(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=2)
    await state.finish()
    await call.message.answer(
        text='Действие отменено'
    )


@dp.message_handler(regexp=r"^([1-9]\d{1,2}) ([1-9]\d{1,2}) ([1-9]\d{1,2})$")
@log_call
@logger.catch
async def write_measurement(message: types.Message):
    measurement_service = MeasurementService()
    text = await measurement_service.add_measurement(
        tid=message.from_user.id,
        date=message.date.date(),
        column=measurement_service.choose_day_time(),
        value=message.text,
    )
    await message.answer(text)


@dp.message_handler()
@log_call
@logger.catch
async def wrong_message(message: types.Message):
    await message.answer("Некорректный формат ввода. Попробуйте ввести данные в формате '120 80 60'.")
