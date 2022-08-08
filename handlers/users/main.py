from aiogram import types

from loader import dp
from keyboards.inline import inline_kb_menu


@dp.message_handler()
async def main(message: types.Message):
    await message.delete()
    await message.answer(f'👋Приветствую, {message.from_user.full_name}!'
                         f'\nУправление БОТом осуществляется через кнопки...', reply_markup=inline_kb_menu.main)