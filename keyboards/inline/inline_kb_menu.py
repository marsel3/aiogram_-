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
    btns.append([InlineKeyboardButton(text='Поиск товара', callback_data='search')])
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


def basket_markup(user_id):
    m1 = db_users.basket_list(user_id)
    btns = []
    if len(m1) > 0:
        for i in m1:
            btns.append([InlineKeyboardButton(text=f'{i[1]}', callback_data=f'tovar_{i[0]}'),
                         InlineKeyboardButton(text=f'✏', callback_data=f'setCount_{i[0]}'),
                         InlineKeyboardButton(text=f'{i[3]} шт.', callback_data=f'setCount_{i[0]}'),
                         InlineKeyboardButton(text=f'🗑', callback_data=f'delTovar_{i[0]}')])
        btns.append([InlineKeyboardButton(text='Очистить корзину', callback_data='cleanBasket')])
        btns.append([InlineKeyboardButton(text='Оформить заказ', callback_data='pay')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='back_to_menu')])
    markup = InlineKeyboardMarkup(inline_keyboard=btns)
    string = f'Корзина.\n'
    summ = 0
    count = 1
    if len(m1) > 0:
        for i in m1:
            string += f'\n\n{count}.  "{i[1]}" \n\t\t\tЦена: {i[2]} × {i[3]}  =  {i[2] * i[3]} рублей'

            #string += f"\n{count}. {i[1]}{i[3]}ед. ({i[2] * i[3]} рублей)"
            summ += i[2] * i[3]
            count += 1
        string += '\n__________________' + '_' * len(str(summ))

    string += f'\nИтого: {summ} рублей'

    return markup, string


def search_markup(m1):
    btns = []
    for i in m1:
        btns.append([InlineKeyboardButton(text=f'{i[0]}', callback_data=f'tovar_{i[1]}')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data=f'back_to_menu')])
    return InlineKeyboardMarkup(inline_keyboard=btns)
