from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import admins_id


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.id in admins_id
