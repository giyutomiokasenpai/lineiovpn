from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from texts import text_keyboards

command_start = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=text_keyboards.my_keys)],
        [KeyboardButton(text=text_keyboards.buy_key)]
    ],
        resize_keyboard=True
)