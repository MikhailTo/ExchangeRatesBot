from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization
from .currency_converter import CurrencyConverter

from config import settings


router = Router()


@router.message(Command("start"))
async def command_start(message: Message, l10n: FluentLocalization):
    """
    Приветственное сообщение от бота пользователю

    :param message: сообщение от пользователя с командой /start
    :param l10n: объект локализации
    """
    await message.answer(l10n.format_value("intro"))


@router.message(Command("help"))
async def command_help(message: Message, l10n: FluentLocalization):
    """
    Справка для пользователя

    :param message: сообщение от пользователя с командой /help
    :param l10n: объект локализации
    """
    await message.answer(l10n.format_value("help"))
