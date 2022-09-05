from aiogram.types import CallbackQuery

from loader import dp, db_tovars, db_users

from keyboards.inline import inline_kb_menu


@dp.callback_query_handler(text_startswith='back_to_menu')
async def show_catalog(call: CallbackQuery):
    await call.message.edit_text('Вы вернулись в главное меню\nНажимай на каталог и начинай собирать заказ 😉')


@dp.callback_query_handler(text=db_tovars.category_list())
async def show_catalog(call: CallbackQuery):
    print(call.data)
    await call.message.edit_text('Какой товар выберите?  😏',
                                 reply_markup=inline_kb_menu.tovar_markup(call.data))


@dp.callback_query_handler(text='back_to_catalog')
async def show_catalog(call: CallbackQuery):
    await call.message.edit_text('C новой обновой заработает...')

    # await call.message.edit_text('Вы вернулись в каталог',
    #                           reply_markup=inline_kb_menu.tovar_markup(call.data))


@dp.callback_query_handler(text_startswith='tovar_')
async def show_catalog(call: CallbackQuery):
    tovar_id = call.data[6:]
    await call.message.edit_text('Эт тип карточка товара')

    # reply_markup=inline_kb_menu.tovar_card(call.data)
