from aiogram import types

from keyboards.default import kb_menu
from loader import dp


@dp.message_handler(text='/start')
async def command_start(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}! А теперь иди нахуй!', reply_markup=kb_menu)