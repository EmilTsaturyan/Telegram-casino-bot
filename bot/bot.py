import asyncio

from aiogram import Bot, Dispatcher
from include_routers import include_routers

from middlewares.anti_flood import AntiFloodMiddleware

from config_reader import config

from motor.motor_asyncio import AsyncIOMotorClient


async def main():
    bot = Bot(config.bot_token.get_secret_value())
    dp = Dispatcher()

    dp.message.middleware(AntiFloodMiddleware(time_limit=2))

    include_routers(dp=dp)

    cluster = AsyncIOMotorClient(host='localhost', port=27017)
    db = cluster.slot

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, db=db)


if __name__ == '__main__':
    asyncio.run(main())
