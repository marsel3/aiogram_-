from filters import IsAdmin
from aiogram import types

from loader import dp, db_tovars, db_users
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from states import state
from utils.db_api.db_admin import *

@dp.message_handler(IsAdmin(), text='/admin')
async def admin(messsage: types.Message):
    await messsage.answer(f'Здравствуйте, {messsage.from_user.full_name},  вы попали в админ панель!',
                          reply_markup=admin_panel)


@dp.callback_query_handler(text='admin_catalog')
async def admin_catalog(call: CallbackQuery):
    await call.message.edit_text('Введите id пользователя')





@dp.callback_query_handler(text_startswith='adminEditTovar_')
async def admin_catalog(call: CallbackQuery):
    await call.message.edit_text('Введите id пользователя')
    await state.user_ad.set()

@dp.callback_query_handler(text_startswith='adminDeleteTovar_')
async def admin_catalog(call: CallbackQuery):
    await call.message.edit_text('Введите id пользователя')
    await state.user_ad.set()