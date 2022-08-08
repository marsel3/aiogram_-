
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main = InlineKeyboardMarkup(row_width=2,
                            inline_keyboard=[
                                [InlineKeyboardButton(text='📜 Каталог товаров', callback_data='catalog'),
                                 InlineKeyboardButton(text='🛒 Корзина', callback_data='cart')
                                 ],

                                [InlineKeyboardButton(text='👤 Профиль', callback_data='profil'),
                                 InlineKeyboardButton(text='🆘 Тех. Поддержка', callback_data='help')
                                 ]
                            ])