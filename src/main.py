from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import BOT__TOKEN


bot = Bot(BOT__TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp)
