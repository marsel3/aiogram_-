from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db_tovars, db_users
from data.config import admins_id
import sqlite3
from db_sqlite import DataBase
from loader import db_tovars, db_users


admin_panel = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Каталог', callback_data='admin_catalog')],
        [InlineKeyboardButton(text='Товары', callback_data='admin_tovar')],
        [InlineKeyboardButton(text='Назад', callback_data='back_to_menu')]
    ]
)

def catalog_markup():
    m1 = db_tovars.category()

    btns = []
    btns.append([InlineKeyboardButton(text='Поиск товара', callback_data='search')])
    for i in m1:
        btns.append([InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[0]}')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='back_to_menu')])

    return InlineKeyboardMarkup(inline_keyboard=btns)



class AdminDataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()


