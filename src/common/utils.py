import functools

from aiogram import types

from logger import logger


def log_call(func):
    @functools.wraps(func)
    def log_wrapper(*args, **kwargs):
        message: types.Message = args[0]
        logger.info(
            f"{func.__name__} is called",
            user_id=message.from_user.id,
            message_date=message.date.isoformat(),
            message_text=message.text,
        )
        return func(*args, **kwargs)
    return log_wrapper
