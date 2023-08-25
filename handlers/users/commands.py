from loader import dp
from aiogram import types
from keyboards.inline import inline_kb_menu
from keyboards.default import keyboard_menu
from utils.db_api.db_asyncpg import *


def extract_unique_code(text):
    return int(text.split()[1]) if len(text.split()) > 1 else None


@dp.message_handler(commands='start')
async def start(message: types.Message):
    exists = await user_exists(message.from_user.id)
    if not exists:
        referral = None
        unique_code = extract_unique_code(message.text)
        if unique_code and await user_exists(unique_code):
            referral = unique_code

        await add_user(user_id=message.from_user.id,
                       fio=message.from_user.full_name,
                       referral=referral)

    await message.answer(f'👋 Приветствую, {message.from_user.full_name}!'
                         f'\nНажимай на каталог и начинай собирать заказ 😉',
                         reply_markup=keyboard_menu.main)
    await message.delete()

