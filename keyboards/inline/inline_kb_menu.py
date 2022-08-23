
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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


