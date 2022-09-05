from aiogram import types
from aiogram.types import CallbackQuery

from loader import dp, db_tovars, db_users
from keyboards.default import keyboard_menu


@dp.message_handler(text=['🗂️ Каталог', 'каталог'])
async def main(message: types.Message):
    await message.delete()
    await message.answer(f'ЭТО КАТАЛОГ!!!',
                         reply_markup=keyboard_menu.main)


@dp.message_handler(text=['🛍️ Корзина', 'корзина'])
async def main(message: types.Message):
    await message.delete()
    await message.answer(f'ЭТО КОРЗИНА!!!',
                         reply_markup=keyboard_menu.main)


@dp.message_handler(text=['⭐ Избранное', 'избранное'])
async def main(message: types.Message):
    await message.delete()
    await message.answer(f'ЭТО ИЗБРАННОЕ!!!',
                         reply_markup=keyboard_menu.main)


@dp.message_handler(text=['📲️Помощь', 'помощь'])
async def main(message: types.Message):
    await message.delete()
    await message.answer(f'ЭТО ПОМОЩЬ!!!',
                         reply_markup=keyboard_menu.main)


@dp.message_handler(text=['👤 Профиль', 'профиль'])
async def main(message: types.Message):
    await message.delete()
    await message.answer(f'ЭТО ПРОФИЛЬ!!!',
                         reply_markup=keyboard_menu.main)

