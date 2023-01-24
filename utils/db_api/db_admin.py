from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db_tovars, db_users
from data.config import admins_id
import sqlite3
from loader import db_tovars, db_users

from slugify import slugify



admin_panel = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Категории', callback_data='admin_category')],
        #[InlineKeyboardButton(text='Товары', callback_data='admin_tovar')],
        #[InlineKeyboardButton(text='Назад', callback_data='back_to_menu')]
    ]
)



def admin_catalog_markup():
    m1 = db_tovars.category()
    btns = []

    for i in m1:
        btns.append([InlineKeyboardButton(text=f'{i[1]}', callback_data=f'admin_category_{i[0]}')])

    btns.append([InlineKeyboardButton(text='Добавить категорию', callback_data='add_new_category')])
    #btns.append([InlineKeyboardButton(text='Назад', callback_data='back_to_menu')])

    return InlineKeyboardMarkup(inline_keyboard=btns)


def admin_tovars_markup(category):
    m1 = db_tovars.tovar(category)
    btns = []

    for i in m1:
        btns.append([InlineKeyboardButton(text=f'{i[1]}', callback_data=f'admin_tovar_{i[0]}')])

    btns.append([InlineKeyboardButton(text='Добавить товар', callback_data='add_new_tovar')])
    btns.append([InlineKeyboardButton(text='Изменить название категории', callback_data=f'edit_category_{category}')])
    btns.append([InlineKeyboardButton(text='Удалить выбранную категорию', callback_data=f'delete_category_{category}')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='admin_category')])

    return InlineKeyboardMarkup(inline_keyboard=btns)
