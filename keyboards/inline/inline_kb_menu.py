
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db_tovars, db_users

main = InlineKeyboardMarkup(row_width=2,
                            inline_keyboard=[
                                [InlineKeyboardButton(text='Запустить калькулятор', callback_data='start_process')
                                 ],
                                [InlineKeyboardButton(text='☎️ Служба поддержки', callback_data='help')
                                 ]
                            ])


back_to_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back_to_menu')
         ]
    ]
)


def catalog_markup():
    m1 = db_tovars.category()
    markup = InlineKeyboardMarkup()

    for i in m1:
        markup.add(InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[0]}'))
    markup.add(InlineKeyboardButton(text='Назад', callback_data='back_to_menu'))

    return markup


def tovar_markup(catalog):
    m1 = db_tovars.tovar(catalog)
    markup = InlineKeyboardMarkup()

    for i in m1:
        markup.add(InlineKeyboardButton(text=f'{i[1]}', callback_data=f'tovar_{i[0]}'))
    markup.add(InlineKeyboardButton(text='Назад в каталог', callback_data='back_to_catalog'))

    return markup


def tovar_card_markup(tovar_id, user_id):
    print(tovar_id)
    string = "Добавить в избранное"
    if db_users.favourite_info(tovar_id, user_id) == 1:
        string = "Убрать из избранного"

    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=string, callback_data=f'setFavourite_{tovar_id}')
         ],

        [InlineKeyboardButton(text=f'➖', callback_data=f'test'),
         InlineKeyboardButton(text=f'?', callback_data=f'test'),
         InlineKeyboardButton(text=f'➕', callback_data=f'test')],

        [InlineKeyboardButton(text='Добавить в корзину', callback_data=f'basketAdd_{tovar_id}')
         ],

        [InlineKeyboardButton(text='Назад', callback_data='back_to_menu')
         ],
    ]
    )
    return markup