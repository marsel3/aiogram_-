from filters import IsAdmin
from aiogram import types

from loader import dp, db_tovars, db_users
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from states import state
from keyboards.inline import inline_kb_menu
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@dp.message_handler(IsAdmin(), text='/admin')
async def admin(messsage: types.Message):
    await messsage.answer(f'Здравствуйте, {messsage.from_user.full_name},  вы попали в админ панель!',
                          reply_markup=inline_kb_menu.admin_panel)


@dp.callback_query_handler(text='admin_start')
async def register(call: CallbackQuery):
    await call.message.edit_text('Введите id пользователя')
    await state.user_ad.set()
