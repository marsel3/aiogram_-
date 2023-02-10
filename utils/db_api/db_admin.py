from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from loader import db_tovars, db_users
from data.config import admins_id
import sqlite3
from loader import db_tovars, db_users

from slugify import slugify


admin_main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='/start')]],
    resize_keyboard=True)

admin_panel = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Категории', callback_data='admin_category')],
        #[InlineKeyboardButton(text='Товары', callback_data='admin_tovar')],
        #[InlineKeyboardButton(text='Назад', callback_data='back_to_menu')]
    ]
)

without_photo = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Без фото', callback_data='without_photo')],
        #[InlineKeyboardButton(text='Товары', callback_data='admin_tovar')],
        #[InlineKeyboardButton(text='Назад', callback_data='back_to_menu')],
], resize_keyboard=True)

agreement = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Да')],
        [KeyboardButton(text='Нет')]],
    resize_keyboard=True)



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

    btns.append([InlineKeyboardButton(text='Добавить товар', callback_data=f'add_new_tovar_{category}')])
    btns.append([InlineKeyboardButton(text='Изменить название категории', callback_data=f'edit_category_{category}')])
    btns.append([InlineKeyboardButton(text='Удалить выбранную категорию', callback_data=f'delete_category_{category}')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='admin_category')])
    return InlineKeyboardMarkup(inline_keyboard=btns)


def set_tovar_card(tovar_id):
    btns = []

    btns.append([InlineKeyboardButton(text='Изменить категорию', callback_data=f'edit_tovar_category_{tovar_id}')])
    btns.append([InlineKeyboardButton(text='Изменить название', callback_data=f'edit_tovar_name_{tovar_id}')])
    btns.append([InlineKeyboardButton(text='Изменить цену', callback_data=f'edit_tovar_price_{tovar_id}')])
    btns.append([InlineKeyboardButton(text='Изменить описание', callback_data=f'edit_tovar_disc_{tovar_id}')])
    btns.append([InlineKeyboardButton(text='Изменить описание', callback_data=f'edit_tovar_photo_{tovar_id}')])

    btns.append([InlineKeyboardButton(text='Назад', callback_data='admin_category')])
    return InlineKeyboardMarkup(inline_keyboard=btns)


def admin_card(tovar_id):
    category_name = db_tovars.category_name_bytovar(tovar_id)
    tovar_card = db_tovars.tovar_card(tovar_id)

    text = f'категория: {category_name}\nназвание: {tovar_card[0]}\nцена: {tovar_card[1]}\nописание: {tovar_card[2]}'
    photo = tovar_card[-1]

    return text, photo