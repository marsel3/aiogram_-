
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import db_tovars

main = InlineKeyboardMarkup(row_width=2,
                            inline_keyboard=[
                                [InlineKeyboardButton(text='Запустить калькулятор', callback_data='start_process')
                                 ],
                                [
                                 InlineKeyboardButton(text='☎️ Служба поддержки', callback_data='help')
                                 ]
                            ])


back_to_menu = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='back_to_menu')
         ]
    ]
)


start_calculator = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Запустить', callback_data='run')
         ],
        [
        InlineKeyboardButton(text='Назад', callback_data='back_to_menu')
        ]
    ]
)


admin_panel = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Редактировать статусы', callback_data='admin_start')],
        [InlineKeyboardButton(text='Назад', callback_data='back_to_menu')]
    ]
)


def catalog_markup():
    m1 = db_tovars.category()
    markup = InlineKeyboardMarkup()

    for i in m1:
        markup.add(InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[0]}'))

    return markup


def tovar_markup(catalog):
    m1 = db_tovars.tovar(catalog)
    markup = InlineKeyboardMarkup()

    for i in m1:
        markup.add(InlineKeyboardButton(text=f'{i[1]}', callback_data=f'tovar_{i[0]}'))

    return markup




