from aiogram import types
from loader import dp
from handlers.users.commands import start_msg


@dp.message_handler()
async def main(message: types.Message):
    await start_msg(message)