from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='10'),
            KeyboardButton(text='11'),
        ],
        [
            KeyboardButton(text='12'),
        ],
    ],
    resize_keyboard=True
)