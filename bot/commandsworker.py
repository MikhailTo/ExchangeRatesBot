from aiogram import Bot
from aiogram.types import BotCommand

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Начало работы с ботом"),
        BotCommand(command="help", description="Справка по использованию бота"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())