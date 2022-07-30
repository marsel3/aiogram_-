
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


main = InlineKeyboardMarkup(row_width=2,
                            inline_keyboard=[
                                [InlineKeyboardButton(text='', callback_data='',
                                                      )],
                                [InlineKeyboardButton]
                            ])