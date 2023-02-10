from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db_tovars, db_users
from data.config import admins_id


back_to_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back_to_menu')
         ]
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


def tovar_markup(catalog):
    m1 = db_tovars.tovar(catalog)
    markup = InlineKeyboardMarkup()
    for i in m1:
        markup.add(InlineKeyboardButton(text=f'{i[1]}', callback_data=f'tovar_{i[0]}'))
    markup.add(InlineKeyboardButton(text='Назад в каталог', callback_data='back_to_catalog'))

    return markup


def tovar_card_markup(tovar_id, user_id):
    category_id = db_tovars.category_id(tovar_id)
    btns = []
    string = "Добавить в избранное"
    if db_users.favourite_info(tovar_id, user_id) == 1:
        string = "Убрать из избранного"
    if user_id in admins_id:
        btns.append([InlineKeyboardButton(text='Изменить товар', callback_data=f'adminEditTovar_{tovar_id}'),
                    InlineKeyboardButton(text='Удалить товар', callback_data=f'adminDeleteTovar_{tovar_id}')])
    btns.append([InlineKeyboardButton(text=string, callback_data=f'setFavourite_{tovar_id}')])
         # [InlineKeyboardButton(text=f'➖', callback_data=f'test'),
         # InlineKeyboardButton(text=f'?', callback_data=f'test'),
         # InlineKeyboardButton(text=f'➕', callback_data=f'test')],
    btns.append([InlineKeyboardButton(text='Добавить в корзину', callback_data=f'basketAdd_{tovar_id}')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data=f'back_to_tovars_{category_id}')])
    return InlineKeyboardMarkup(inline_keyboard=btns)


def favourite_markup(user_id):
    m1 = db_users.favourite_list(user_id)
    btns = []
    for i in m1:
        btns.append([InlineKeyboardButton(text=f'{i[1]}', callback_data=f'tovar_{i[0]}'),
                    InlineKeyboardButton(text='Убрать', callback_data=f'delFavourite_{i[0]}')])
    if len(m1) > 0:
        btns.append([InlineKeyboardButton(text='Очистить список избранного', callback_data='cleanFavourite')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='back_to_menu')])
    markup = InlineKeyboardMarkup(inline_keyboard=btns)

    return markup


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
