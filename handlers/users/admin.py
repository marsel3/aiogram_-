from filters import IsAdmin
from aiogram import types

from loader import dp, db_tovars, db_users
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from states import State
from utils.db_api import db_admin


@dp.message_handler(IsAdmin(), text='/admin')
async def admin(messsage: types.Message):
    await messsage.answer(f'Здравствуйте, {messsage.from_user.full_name},  вы попали в админ панель!',
                          reply_markup=db_admin.admin_panel)


@dp.callback_query_handler(text='admin_category')
async def admin_catalog(call: CallbackQuery):
    await call.message.edit_text('Вы в меню редактора категории', reply_markup=db_admin.admin_catalog_markup())


@dp.callback_query_handler(text='add_new_category')
async def add_new_category(call: CallbackQuery):
   await call.message.edit_text("Введите название новой категории")
   await State.category_add.set()

@dp.message_handler(state=State.category_add)
async def state1(message: types.Message, state: FSMContext):
    answer = message.text
    db_tovars.category_add(answer)
    await message.answer(f"Категория '{answer}' добавлена в базу",
                         reply_markup=db_admin.admin_catalog_markup())
    await state.finish()


@dp.callback_query_handler(text_startswith='admin_category_')
async def admin_category_(call: CallbackQuery):
    category_id = call.data[15:]
    category = db_tovars.category_name(category_id)
    await call.message.edit_text(f'Вы в меню редактора категории "{category}"',
                                 reply_markup=db_admin.admin_tovars_markup(category_id))


@dp.callback_query_handler(text_startswith='delete_category_')
async def admin_category_(call: CallbackQuery):
    category_id = call.data[16:]
    category = db_tovars.category_name(category_id)
    db_tovars.category_delete(category_id)
    await call.message.answer(f'Категория "{category}" удалена!',
                              reply_markup=db_admin.admin_catalog_markup())



@dp.callback_query_handler(text_startswith='edit_category_')
async def admin_category_(call: CallbackQuery):
    category_id = call.data[14:]
    category = db_tovars.category_name(category_id)

    await call.message.answer(f'Введите новое название вместо "{category}"')
    State.category = category_id
    await State.category_edit.set()


@dp.message_handler(state=State.category_edit)
async def state2(message: types.Message, state: FSMContext):
    answer = message.text
    category_id = State.category
    db_tovars.category_edit_name(category_id, answer)

    await message.answer(f"Новое название категории '{answer}'",
                         reply_markup=db_admin.admin_tovars_markup(category_id))
    await state.finish()


@dp.callback_query_handler(text='add_new_tovar')
async def add_new_category(call: CallbackQuery):
   await call.message.edit_text("Введите название новой категории")
   await State.category_add.set()