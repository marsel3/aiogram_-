from aiogram import types

from loader import dp, db_shop
from keyboards.default import keyboard_menu



@dp.message_handler()
async def main(message: types.Message):
    """if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id,
                    message.from_user.username,
                    message.from_user.full_name)"""

    await message.delete()
    await message.answer(f'👋 Приветствую, {message.from_user.full_name}!'
                         f'\nНажимай на каталог и начинай собирать заказ 😉',
                         reply_markup=keyboard_menu.main)