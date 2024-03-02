import asyncio
from aiogram import Bot, Dispatcher


from settings import BOT__TOKEN


dp = Dispatcher()


async def main(dp: Dispatcher) -> None:
    bot = Bot(BOT__TOKEN, parse_mode='HTML')
    await dp.start_polling(bot)



if __name__ == '__main__':
    from handlers import dp as hdp
    asyncio.run(main(hdp))
