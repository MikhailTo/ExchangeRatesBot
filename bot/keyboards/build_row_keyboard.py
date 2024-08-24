from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def build_row_keyboard(texts: list):

    builder = ReplyKeyboardBuilder()

    for text in texts:
        builder.add((KeyboardButton(text=text.upper())))

    builder.adjust(4)

    return builder.as_markup(
            resize_keyboard=True,
            one_time_keyboard=True)
        