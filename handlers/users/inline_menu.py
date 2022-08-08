from aiogram import types
from aiogram.types import CallbackQuery

from loader import dp
import utils.db_api.db_asyncpg as db


@dp.callback_query_handler(text='catalog')
async def show_catalog(call: CallbackQuery):
    try:
        markup = await db.categories_markup()
        print(markup)
        await call.message.edit_reply_markup('catalog', reply_markup=markup)
    except:
        await call.message.answer('catalog')


@dp.callback_query_handler(text='cart')
async def show_catalog(call: CallbackQuery):
    await call.message.edit_text('catalog')


@dp.callback_query_handler(text='profil')
async def show_catalog(call: CallbackQuery):
    await call.message.edit_text('catalog')


@dp.callback_query_handler(text='help')
async def show_catalog(call: CallbackQuery):
    await call.message.edit_text('catalog')