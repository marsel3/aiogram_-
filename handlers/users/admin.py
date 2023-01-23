from filters import IsAdmin
from aiogram import types

from loader import dp, db_tovars, db_users
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from states import state
from utils.db_api import db_admin

@dp.message_handler(IsAdmin(), text='/admin')
async def admin(messsage: types.Message):
    await messsage.answer(f'Здравствуйте, {messsage.from_user.full_name},  вы попали в админ панель!',
                          reply_markup=db_admin.admin_panel)


@dp.callback_query_handler(text='admin_category')
async def admin_catalog(call: CallbackQuery):
    await call.message.edit_text(reply_markup=db_admin.admin_catalog_markup())


@dp.callback_query_handler(text='add_new_category')
async def add_new_category(call: CallbackQuery):
   #await call.message.edit_text(reply_markup=db_admin.admin_catalog_markup())
   await state.State.category_add.set()

@dp.message_handler(state=state.State.category_add)
async def state1(message: types.Message, state: FSMContext):
    answer = message.text
    db_tovars.category_add(answer)
    await state.finish()


@dp.callback_query_handler(text_startswith='adminEditTovar_')
async def admin_catalog(call: CallbackQuery):
    await call.message.edit_text('Введите id пользователя')
    await state.user_ad.set()

@dp.callback_query_handler(text_startswith='adminDeleteTovar_')
async def admin_catalog(call: CallbackQuery):
    await call.message.edit_text('Введите id пользователя')
    await state.user_ad.set()