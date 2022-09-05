from aiogram.types import CallbackQuery

from loader import dp, db_tovars, db_users

from keyboards.inline import inline_kb_menu


@dp.callback_query_handler(text=db_tovars.category_list())
async def show_catalog(call: CallbackQuery):
    print(call.data)
    await call.message.edit_text('Вы вернулись в главное меню',
                                 reply_markup=inline_kb_menu.tovar_markup(call.data))


@dp.callback_query_handler(text_startswith='tovar_')
async def show_catalog(call: CallbackQuery):
    tovar_id = call.data[6:]

    await call.message.edit_text('Вы вернулись в главное меню',
                                 reply_markup=inline_kb_menu.tovar_markup(call.data))

