from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from data.config import manager_url
from utils.db_api.db_asyncpg import *


back_to_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back_to_menu')
         ]
    ]
)


admin = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='⚙️ Редактор категорий', callback_data='admin_all_categories')],
        [InlineKeyboardButton(text='📢 Сделать рассылку', callback_data='admin_send_message')],
        [InlineKeyboardButton(text='📋 Пользователи', callback_data='admin_all_users_info')],

        [InlineKeyboardButton(text='Назад', callback_data='back_to_menu')]
    ]
)

back_to_admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='manager_main_menu')]
])


async def categories_markup(row_count=2):
    categories = await category_list()
    btns = list()
    btn_row = list()
    btns.append([InlineKeyboardButton(text='🔍 Поиск товара', callback_data='SearchTovar')])

    for i, category in enumerate(categories):
        if i % row_count == 0 and i != 0:
            btns.append(btn_row)
            btn_row = list()
        btn_row.append(InlineKeyboardButton(text=f'{category["category"]}', callback_data=f'category_1_{category["id"]}'))

    if btn_row:
        btns.append(btn_row)

    btns.append([InlineKeyboardButton(text='⬅️ Назад', callback_data='DeleteMessage')])

    return InlineKeyboardMarkup(inline_keyboard=btns)


async def tovar_list_markup(category_id, page=1):
    btns = list()
    tovar_list = await tovars_by_category(category_id=category_id)
    max_on_one_page = 10
    pages = len(tovar_list) // max_on_one_page + 1 if (len(tovar_list) // max_on_one_page) != (len(tovar_list) / max_on_one_page) else len(tovar_list) // max_on_one_page

    for tovar in tovar_list[(page - 1) * max_on_one_page:page * max_on_one_page]:
        btns.append([InlineKeyboardButton(text=f'{tovar["tovar"]}', callback_data=f'tovar-info_{page}_{category_id}_{tovar["id"]}_{1}')])

    if pages > 1:
        btns.append([InlineKeyboardButton(text='⬅️', callback_data=f'category_{page - 1 if page - 1 > 0 else pages}_{category_id}'),
                     InlineKeyboardButton(text=f'{page}', callback_data=f'_'),
                     InlineKeyboardButton(text='➡️', callback_data=f'category_{page + 1 if pages >= page + 1 else 1}_{category_id}')])

    btns.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'categories')])

    return InlineKeyboardMarkup(inline_keyboard=btns)


async def tovar_search_markup(tovars):
    btns = list()
    for tovar in tovars:
        btns.append([InlineKeyboardButton(text=f'{tovar["tovar"]}', callback_data=f'tovar-info_{1}_{tovar["id"]}_1')])
    btns.append([InlineKeyboardButton(text='⬅️ Назад', callback_data='categories')])

    return InlineKeyboardMarkup(inline_keyboard=btns)


async def tovar_info_markup(user_id, count, category_id, tovar_id, page, pages, prev_tovar_id=None, next_tovar_id=None):
    btns = []

    btns.append([InlineKeyboardButton(text='👩🏻‍💼 Связаться с менеджером', url=manager_url)])

    favourite_text = "☆ Добавить в избранное"
    if await tovar_is_favourite(product_id=tovar_id, user_id=user_id):
        favourite_text = "⭐ Убрать из избранного"
    btns.append([InlineKeyboardButton(text=favourite_text, callback_data=f'setFavourite_{page}_{category_id}_{tovar_id}_{count}')])
    btns.append([InlineKeyboardButton(text='🌟 Отзывы', callback_data=f'reviews/0/_1_{tovar_id}')])
    btns.append([InlineKeyboardButton(text=f'➖', callback_data=f'tovar-info_{page}_{category_id}_{tovar_id}_{1 if count-1 <= 1 else count - 1}'),
                 InlineKeyboardButton(text=f'{count}', callback_data=f'setTovarCount_{page}_{category_id}_{tovar_id}_{count}'),
                 InlineKeyboardButton(text=f'➕', callback_data=f'tovar-info_{page}_{category_id}_{tovar_id}_{count + 1}')])

    navigation_row = [
        InlineKeyboardButton(text='⬅️',
                             callback_data=f'tovar-info_{page - 1 if page - 1 > 0 else pages}_{category_id}_{prev_tovar_id}_{1}') if prev_tovar_id is not None else None,
        InlineKeyboardButton(text='➡️',
                             callback_data=f'tovar-info_{page + 1 if pages >= page + 1 else 1}_{category_id}_{next_tovar_id}_{1}') if next_tovar_id is not None else None
    ]

    navigation_row = [btn for btn in navigation_row if btn is not None]

    btns.append([InlineKeyboardButton(text='🛒 Добавить в корзину', callback_data=f'basketAdd_{page}_{category_id}_{tovar_id}_{count}')])
    if navigation_row and pages > 1:
        btns.append(navigation_row)

    btns.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'category_{page}_{category_id}')])

    return InlineKeyboardMarkup(inline_keyboard=btns)


async def favourite_markup(user_id):
    tovar_list = await tovar_favourite_list(user_id)
    btns = list()
    for tovar in tovar_list:
        btns.append([InlineKeyboardButton(text=f'{tovar["tovar"]}', callback_data=f'tovar_1_{tovar["category"]}_{tovar["id"]}_{1}'),
                    InlineKeyboardButton(text='Убрать', callback_data=f'delFavourite_{tovar["id"]}')])
    if len(tovar_list) > 0:
        btns.append([InlineKeyboardButton(text='Очистить список избранного', callback_data='clearFavourite')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='back_to_menu')])
    return InlineKeyboardMarkup(inline_keyboard=btns)


async def basket_markup(basket, bonus=False):
    btns = list()
    if len(basket) > 0:
        for tovar in basket:
            btns.append([InlineKeyboardButton(text=f'{tovar["tovar"]}', callback_data=f'tovar-info_1_{tovar["category"]}_{tovar["id"]}_1'),
                         InlineKeyboardButton(text=f'✏', callback_data=f'setCountInBasket_{tovar["id"]}'),
                         InlineKeyboardButton(text=f'{tovar["count"]} шт.', callback_data=f'setCountInBasket_{tovar["id"]}'),
                         InlineKeyboardButton(text=f'🗑', callback_data=f'delBasket_{tovar["id"]}')])
        btns.append([InlineKeyboardButton(text='Очистить корзину', callback_data='clearBasket')])
        btns.append([InlineKeyboardButton(text='Не списывать бонусные рубли' if bonus else 'Cписывать бонусные рубли',
                                          callback_data=f'ApplyBonus_{not bonus}')])

        btns.append([InlineKeyboardButton(text='Оформить заказ', callback_data='pay')])
    btns.append([InlineKeyboardButton(text='Назад', callback_data='DeleteMessage')])
    return InlineKeyboardMarkup(inline_keyboard=btns)


async def continue_shopping():
    btns = list()
    btns.append([InlineKeyboardButton(text='Продолжить покупки', callback_data='categories')])
    btns.append([InlineKeyboardButton(text='Оформить заказ', callback_data='basket')])
    return InlineKeyboardMarkup(inline_keyboard=btns)


async def adminconfirm(user_id, app_id):
    btns = list()
    btns.append([InlineKeyboardButton(text='✅ Подтвердить', callback_data=f'admin-confirm_1_{user_id}_{app_id}')])
    btns.append([InlineKeyboardButton(text='❌ Отклонить', callback_data=f'admin-confirm_0_{user_id}_{app_id}')])
    return InlineKeyboardMarkup(inline_keyboard=btns)


async def admin_categories_markup(row_count=2):
    categories = await category_list()
    btns = list()
    btn_row = list()

    for i, category in enumerate(categories):
        if i % row_count == 0 and i != 0:
            btns.append(btn_row)
            btn_row = list()
        btn_row.append(InlineKeyboardButton(text=f'{category["category"]}', callback_data=f'admin-category_1_{category["id"]}'))

    if btn_row:
        btns.append(btn_row)

    btns.append([InlineKeyboardButton(text='⚙️ Добавить категорию', callback_data='AddNewCategory')])
    btns.append([InlineKeyboardButton(text='⬅️ Назад', callback_data='manager_main_menu')])

    return InlineKeyboardMarkup(inline_keyboard=btns)


async def admin_tovar_list_markup(category_id, page=1):
    btns = list()
    tovar_list = await tovars_by_category(category_id=category_id)
    max_on_one_page = 10
    pages = len(tovar_list) // max_on_one_page + 1 if (len(tovar_list) // max_on_one_page) != (len(tovar_list) / max_on_one_page) else len(tovar_list) // max_on_one_page

    for tovar in tovar_list[(page - 1) * max_on_one_page:page * max_on_one_page]:
        btns.append([InlineKeyboardButton(text=f'{tovar["tovar"]}', callback_data=f'admin-tovar-info_{page}_{category_id}_{tovar["id"]}_{1}')])

    if pages > 1:
        btns.append([InlineKeyboardButton(text='⬅️', callback_data=f'admin-category_{page - 1 if page - 1 > 0 else pages}_{category_id}'),
                     InlineKeyboardButton(text=f'{page}', callback_data=f'_'),
                     InlineKeyboardButton(text='➡️', callback_data=f'admin-category_{page + 1 if pages >= page + 1 else 1}_{category_id}')])

    btns.append([InlineKeyboardButton(text='⚙️ Добавить товар', callback_data=f'AddNewTovar_{page}_{category_id}')])
    btns.append([InlineKeyboardButton(text='⚙️ Удалить категорию', callback_data=f'DeleteCategory_{page}_{category_id}')])

    btns.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'admin_all_categories')])

    return InlineKeyboardMarkup(inline_keyboard=btns)


async def admin_tovar_info_markup(tovar_id, category, page=1):
    btns = list()

    btns.append([InlineKeyboardButton(text='⚙️ Изменить название', callback_data=f'EditTovarTitle_{page}_{category}_{tovar_id}')])

    btns.append([InlineKeyboardButton(text='⚙️ Цена', callback_data=f'EditTovarPrice_{page}_{category}_{tovar_id}'),
                 InlineKeyboardButton(text='⚙️ Описание', callback_data=f'EditTovarDesc_{page}_{category}_{tovar_id}')])

    btns.append([InlineKeyboardButton(text='⚙️ Фото', callback_data=f'EditTovarPhoto_{page}_{category}_{tovar_id}'),
                 InlineKeyboardButton(text='⚙️ Рейтинг', callback_data=f'EditTovarRating_{page}_{category}_{tovar_id}')])

    btns.append([InlineKeyboardButton(text='⚙️ Удалить товар', callback_data=f'DeleteTovarById_1_{category}_{tovar_id}')])
    btns.append([InlineKeyboardButton(text='⬅️ Назад', callback_data=f'admin-category_{page}_{category}')])

    return InlineKeyboardMarkup(inline_keyboard=btns)


async def review_markup(page, pages, product_id):
    btns = list()
    btns.append([InlineKeyboardButton(text='➕ Оставить отзыв', callback_data=f'add-review/1/_{page}_{product_id}')])

    navigation_row = [
        InlineKeyboardButton(text='⬅️', callback_data=f'reviews/1/_{page - 1 if page - 1 > 0 else pages}_{product_id}'),
        InlineKeyboardButton(text=f'{page}', callback_data='_'),
        InlineKeyboardButton(text='➡️', callback_data=f'reviews/1/_{page + 1 if pages >= page + 1 else 1}_{product_id}')
    ]
    if navigation_row and pages > 1:
        btns.append(navigation_row)
    btns.append([InlineKeyboardButton(text='Назад', callback_data='DeleteMessage')])

    return InlineKeyboardMarkup(inline_keyboard=btns)
