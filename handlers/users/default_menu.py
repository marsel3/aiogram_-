from aiogram import types

from loader import dp, db_shop
from keyboards.default import keyboard_menu

from aiogram.dispatcher.filters import Command
from states import test


@dp.message_handler(text=['register', 'sosister'])
async def register(message: types.Message):
    await message.answer('HELLO!')
    await test.test1.set()
