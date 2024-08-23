from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message
from fluent.runtime import FluentLocalization
from .get_exgange_rates import CurrencyConverter

router = Router()

@router.message(Command(commands=["start"]))
async def command_start(message: Message, l10n: FluentLocalization):
    """
    Приветственное сообщение от бота пользователю

    :param message: сообщение от пользователя с командой /start
    :param l10n: объект локализации
    """
    await message.answer(l10n.format_value("intro"))


@router.message(Command(commands=["help"]))
async def command_help(message: Message, l10n: FluentLocalization):
    """
    Справка для пользователя

    :param message: сообщение от пользователя с командой /help
    :param l10n: объект локализации
    """
    await message.answer(l10n.format_value("help"))

@router.message(F.text)
async def text_message(message: Message, bot: Bot, l10n: FluentLocalization):
    """
    Хэндлер на текстовые сообщения от пользователя

    :param message: сообщение от пользователя дла отправки валюты
    :param l10n: объект локализации
    """
    if answer := CurrencyConverter(l10n).build_answer(message):
        await bot.answer(answer.html_text, parse_mode="HTML")
    else: 
        return await message.reply(l10n.format_value("not-number-text-error"))
