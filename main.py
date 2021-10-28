import os

from aiogram import Bot, Dispatcher, executor
from dotenv import load_dotenv


load_dotenv()

proxy_url = 'http://proxy.server:3128'
BOT_TOKEN = os.environ.get('BOT_TOKEN')
bot = Bot(BOT_TOKEN, proxy=proxy_url)
dp = Dispatcher(bot)

if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp)
