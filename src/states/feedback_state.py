from aiogram.dispatcher.filters.state import StatesGroup, State


class FeedbackState(StatesGroup):
    waiting_for_feedback = State()
