from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from utils.db_api.db_asyncpg import *

cancel = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Отмена')]],
                             resize_keyboard=True)

without_photo = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Без фото', callback_data='without_photo')]],
                                    resize_keyboard=True)

withoutdesc = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Без описания')]],
                                  resize_keyboard=True)

agreement = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Да')],
                                          [KeyboardButton(text='Нет')]],
                                resize_keyboard=True)


admin_panel = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⚙️ Редактор категорий', callback_data='admin_all_categories')],
        [InlineKeyboardButton(text='📢 Сделать рассылку', callback_data='admin_send_message')],
        [InlineKeyboardButton(text='📊 Статистика', callback_data='admin_statistic')],
        [InlineKeyboardButton(text='Назад', callback_data='back_to_menu')]
    ]
)

back_to_admin_panel = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='admin_panel')]
    ]
)


async def admin_catalog_markup():
    categories = await category_list()
    btns = list()

    for category in categories:
        btns.append([InlineKeyboardButton(text=f'{category["category"]}', callback_data=f'adminCategory_{category["id"]}')])
    btns.append([InlineKeyboardButton(text='⚙️ Добавить категорию', callback_data='AddNewCategory')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='admin_panel')])

    return InlineKeyboardMarkup(inline_keyboard=btns)


async def admin_tovars_markup(category):
    tovars = await tovar_by_category(category)
    btns = list()

    for tovar in tovars:
        btns.append([InlineKeyboardButton(text=f'{tovar["name"]}', callback_data=f'adminTovar_{tovar["id"]}')])

    btns.append([InlineKeyboardButton(text='⚙️ Добавить товар', callback_data=f'AddNewTovar_{category}')])
    btns.append([InlineKeyboardButton(text='⚙️ Изменить название категории', callback_data=f'adminEditCategory_{category}')])
    btns.append([InlineKeyboardButton(text='⚙️ Удалить категорию', callback_data=f'adminDelCategory_{category}')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='admin_all_categories')])
    return InlineKeyboardMarkup(inline_keyboard=btns)


async def admin_tovar_markup(tovar_id):
    category_id = await category_by_tovar(tovar_id)
    btns = list()

    """btns.append([InlineKeyboardButton(text='Изменить категорию', callback_data=f'_')])
    btns.append([InlineKeyboardButton(text='Изменить название', callback_data=f'_')])
    btns.append([InlineKeyboardButton(text='Изменить цену', callback_data=f'_')])
    btns.append([InlineKeyboardButton(text='Изменить описание', callback_data=f'_')])
    btns.append([InlineKeyboardButton(text='Изменить фото', callback_data=f'_')])"""
    btns.append([InlineKeyboardButton(text='Удалить товар', callback_data=f'adminDeleteTovar_{category_id}_{tovar_id}')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data=f'adminCategory_{category_id}')])
    return InlineKeyboardMarkup(inline_keyboard=btns)
