from aiogram import types

from loader import dp, db_users
from keyboards.default import keyboard_menu


@dp.message_handler()
async def main(message: types.Message):
    if not db_users.user_exists(message.from_user.id):
        db_users.add_user(message.from_user.id,
                          message.from_user.username,
                          message.from_user.full_name)
        db_users.create_basket(message.from_user.id)
        print('kek')
    await message.delete()
    await message.answer(f'👋 Приветствую, {message.from_user.full_name}!'
                         f'\nНажимай на каталог и начинай собирать заказ 😉',
                         reply_markup=keyboard_menu.main)
