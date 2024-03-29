from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


main = ReplyKeyboardMarkup(
    keyboard=[
            [
                KeyboardButton(text='🗂️ Каталог'),
                KeyboardButton(text='🛍️ Корзина'),
            ],
            [
                KeyboardButton(text='⭐ Избранное'),
                KeyboardButton(text="📲️Контакты"),
            ],
            [
            KeyboardButton(text='👤 Профиль'),
            ],
        ],
    resize_keyboard=True
)