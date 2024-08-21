import asyncio
import logging
from aiogram import Bot, Dispatcher

from fluent.runtime import FluentLocalization, FluentResourceLoader
from pathlib import Path
from bot.config import settings

async def main():

    # Настройка логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s", 
    )

    # Локализация 
    locales_path = Path(__file__).parent.joinpath("locales")
    l10n_loader = FluentResourceLoader(str(locales_path) + "/{locale}")
    l10n = FluentLocalization(["en", "ru"], ["strings.ftl", "errors.ftl"], l10n_loader)

    
    bot = Bot(token=settings.bot_token.get_secret_value())
    dp = Dispatcher()

asyncio.run(main())