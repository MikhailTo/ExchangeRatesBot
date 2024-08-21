import asyncio
from aiogram import Bot, Dispatcher
from bot.config import settings

async def main():

    bot = Bot(token=settings.bot_token.get_secret_value())
    dp = Dispatcher()

asyncio.run(main())