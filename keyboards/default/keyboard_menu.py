from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='ℹ️Главная страница'),
        ],
    ],
    resize_keyboard=True
)