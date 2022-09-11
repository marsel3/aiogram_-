
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db_tovars

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


def tovar_card_markup(tovar_id):
    markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Добавить в корзину', callback_data=f'add_{tovar_id}')],

            [InlineKeyboardButton(text=f'➖', callback_data=f'back_to_catalog'),
             InlineKeyboardButton(text=f'?', callback_data=f'back_to_catalog'),
             InlineKeyboardButton(text=f'➕', callback_data=f'back_to_catalog')],

            [InlineKeyboardButton(text='Назад', callback_data='back_to_menu')
             ],
        ]
    )

    return markup




