from aiogram import types

from loader import dp, db_users
from keyboards.default import keyboard_menu
from utils.db_api.db_asyncpg import *

@dp.message_handler()
async def main(message: types.Message):
    exists = await user_exists(message.from_user.id)
    if not exists:
        referral = None
        await add_user(user_id=message.from_user.id,
                       fio=message.from_user.full_name,
                       referral=referral)

    await message.answer(f'👋 Приветствую, {message.from_user.full_name}!'
                         f'\nНажимай на каталог и начинай собирать заказ 😉',
                         reply_markup=keyboard_menu.main)
    await message.delete()

