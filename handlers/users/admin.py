from filters import IsAdmin
from aiogram import types

from loader import dp, db_tovars, db_users
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from states.state import State1
from utils.db_api import db_admin


@dp.message_handler(IsAdmin(), text='/admin')
async def admin(messsage: types.Message):
    await messsage.answer(f'Здравствуйте, {messsage.from_user.full_name},  вы попали в админ панель!',
                          reply_markup=db_admin.admin_panel)


@dp.callback_query_handler(text='admin_category')
async def admin_catalog(call: CallbackQuery):
    await call.message.edit_text('Вы в меню редактора категории', reply_markup=db_admin.admin_catalog_markup())

