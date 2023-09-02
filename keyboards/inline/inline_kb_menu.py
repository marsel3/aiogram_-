from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.db_api.db_asyncpg import *


back_to_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back_to_menu')
         ]
    ]
)


async def categories_markup():
    categories = await category_list()
    btns = list()
    btns.append([InlineKeyboardButton(text='Поиск товара', callback_data='SearchTovar')])
    for category in categories:
        btns.append([InlineKeyboardButton(text=f'{category["category"]}', callback_data=f'category_{category["id"]}')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='back_to_menu')])

    return InlineKeyboardMarkup(inline_keyboard=btns)


async def tovar_markup(tovars):
    markup = InlineKeyboardMarkup()
    for tovar in tovars:
        markup.add(InlineKeyboardButton(text=f'{tovar["name"]}', callback_data=f'tovar_{tovar["id"]}'))
    markup.add(InlineKeyboardButton(text='Назад в каталог', callback_data='back_to_catalog'))
    return markup


async def tovar_card_markup(tovar_id, count, user_id):
    btns = []
    category_id = await category_by_tovar(tovar_id)
    favourite_text = "Добавить в избранное"
    if await tovar_is_favourite(tovar_id, user_id):
        favourite_text = "Убрать из избранного"
    btns.append([InlineKeyboardButton(text=favourite_text, callback_data=f'setFavourite_{tovar_id}_{count}')])
    btns.append([InlineKeyboardButton(text=f'➖', callback_data=f'minusCount_{tovar_id}_{count}'),
                 InlineKeyboardButton(text=f'{count}', callback_data=f'setTovarCount_{tovar_id}'),
                 InlineKeyboardButton(text=f'➕', callback_data=f'plusCount_{tovar_id}_{count}')])

    btns.append([InlineKeyboardButton(text='Добавить в корзину', callback_data=f'basketAdd_{tovar_id}_{count}')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data=f'category_{category_id}')])
    return InlineKeyboardMarkup(inline_keyboard=btns)


async def favourite_markup(user_id):
    tovar_list = await tovar_favourite_list(user_id)
    btns = list()
    for tovar in tovar_list:
        btns.append([InlineKeyboardButton(text=f'{tovar["name"]}', callback_data=f'tovar_{tovar["tovar_id"]}'),
                    InlineKeyboardButton(text='Убрать', callback_data=f'delFavourite_{tovar["tovar_id"]}')])
    if len(tovar_list) > 0:
        btns.append([InlineKeyboardButton(text='Очистить список избранного', callback_data='clearFavourite')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='back_to_menu')])
    return InlineKeyboardMarkup(inline_keyboard=btns)


async def basket_markup(basket, bonus=False):
    btns = list()
    if len(basket) > 0:
        for tovar in basket:
            btns.append([InlineKeyboardButton(text=f'{tovar["name"]}', callback_data=f'tovar_{tovar["id"]}'),
                         InlineKeyboardButton(text=f'✏', callback_data=f'setCountInBasket_{tovar["id"]}'),
                         InlineKeyboardButton(text=f'{tovar["count"]} шт.', callback_data=f'setCountInBasket_{tovar["id"]}'),
                         InlineKeyboardButton(text=f'🗑', callback_data=f'delBasket_{tovar["id"]}')])
        btns.append([InlineKeyboardButton(text='Очистить корзину', callback_data='clearBasket')])

        btns.append([InlineKeyboardButton(text='Не списывать бонусные рубли' if bonus else 'Cписывать бонусные рубли',
                                          callback_data=f'ApplyBonus_{not bonus}')])
        btns.append([InlineKeyboardButton(text='Оформить заказ', callback_data='pay')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='back_to_menu')])
    return InlineKeyboardMarkup(inline_keyboard=btns)
