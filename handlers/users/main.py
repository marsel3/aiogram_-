from  aiogram import types
from loader import dp


@dp.message_handler()
async def main(message: types.Message):
    await message.answer(f'Привет {message.from_user.full_name}!')