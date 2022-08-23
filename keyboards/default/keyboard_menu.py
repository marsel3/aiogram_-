from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main = ReplyKeyboardMarkup(
    keyboard=[
            [
                KeyboardButton(text='🗂️ Каталог'),
                KeyboardButton(text='🛍️ Корзина'),
            ],
            [
                KeyboardButton(text='⭐ Избранное'),
                KeyboardButton(text='📲️Помощь'),
            ],
            [
            KeyboardButton(text='👤 Профиль'),
            ],
        ],
    resize_keyboard=True
)