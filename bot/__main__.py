import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from fluent.runtime import FluentLocalization, FluentResourceLoader
from pathlib import Path

from bot.commandsworker import set_bot_commands
from bot.middlewares import L10nMiddleware
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

    # Настройка бота
    bot = Bot(token=settings.bot_token.get_secret_value(), 
        default=DefaultBotProperties(
                parse_mode=ParseMode.HTML
                )
        )

    dp = Dispatcher()
    router = setup_routers()
    dp.include_router(router)
    
    # Регистрация мидлварей
    dp.update.middleware(L10nMiddleware(l10n))

    # Регистрация команд в интерфейсе
    await set_bot_commands(bot)

    # Запуск бота c автоматической настройкой на получение только релевантных для него типов обновлений.
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

if __name__ == "__main__":
    asyncio.run(main())