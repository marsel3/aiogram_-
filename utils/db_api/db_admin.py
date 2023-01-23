from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db_tovars, db_users
from data.config import admins_id
import sqlite3
from loader import db_tovars, db_users

from slugify import slugify



admin_panel = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Категории', callback_data='admin_category')],
        [InlineKeyboardButton(text='Товары', callback_data='admin_tovar')],
        [InlineKeyboardButton(text='Назад', callback_data='back_to_menu')]
    ]
)

def admin_catalog_markup():
    m1 = db_tovars.category()
    btns = []

    for i in m1:
        btns.append([InlineKeyboardButton(text=f'{i[1]}', callback_data=f'admin_category_{i[0]}')])

    btns.append([InlineKeyboardButton(text='Добавить категорию', callback_data='add_new_category')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='back_to_menu')])

    return InlineKeyboardMarkup(inline_keyboard=btns)


def admin_tovars_markup(category):
    m1 = db_tovars.tovar()
    btns = []

    for i in m1:
        btns.append([InlineKeyboardButton(text=f'{i[1]}', callback_data=f'admin_tovar_{i[0]}')])

    btns.append([InlineKeyboardButton(text='Добавить товар', callback_data='add_new_tovar')])
    btns.append([InlineKeyboardButton(text='Удалить выбранную категорию', callback_data='add_new_tovar')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='back_to_menu')])

    return InlineKeyboardMarkup(inline_keyboard=btns)




class AdminDataBase:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def category_add(self, category):
        with self.connection:
            result = self.cursor.execute(f'INSERT INTO "category" VALUES ("{slugify(category)}", "{category}")')
            self.connection.commit()
            return result

    def category_delete(self, category_id):
        with self.connection:
            result = self.cursor.execute(f'DELETE FROM "category" WHERE "category_id"="{category_id}"').fetchall()
            self.connection.commit()
            return result

