from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.db_api.db_asyncpg import user_is_admin


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return await user_is_admin(user_id=message.from_user.id)