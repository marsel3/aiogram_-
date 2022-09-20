from aiogram.types import CallbackQuery
from loader import dp, db_tovars, db_users
from states import State
from keyboards.inline import inline_kb_menu
from aiogram.dispatcher import FSMContext
from aiogram import types

@dp.callback_query_handler(text='test')
async def show_catalog(call: CallbackQuery):
    await call.message.edit_text('C новой обновой заработает...')


@dp.callback_query_handler(text_startswith='back_to_menu')
async def show_catalog(call: CallbackQuery):
    await call.message.edit_text('Вы вернулись в главное меню\nНажимай на каталог и начинай собирать заказ 😉')


@dp.callback_query_handler(text_startswith='back_to_catalog')
async def show_catalog(call: CallbackQuery):
    await call.message.answer(f'Вы перешли в каталог, выберите категорию нужного вам товара.',
                              reply_markup=inline_kb_menu.catalog_markup())


@dp.callback_query_handler(text=db_tovars.category_list())
async def show_catalog(call: CallbackQuery):
    await call.message.edit_text('Какой товар выберите?  😏',
                                 reply_markup=inline_kb_menu.tovar_markup(call.data))


@dp.callback_query_handler(text_startswith='back_to_tovars_')
async def show_catalog(call: CallbackQuery):
    tovar_id = call.data[15:]
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    await dp.bot.send_message(chat_id=call.message.chat.id,
                              text='Какой товар выберите?  😏',
                              reply_markup=inline_kb_menu.tovar_markup(tovar_id))


@dp.callback_query_handler(text_startswith='tovar_')
async def show_catalog(call: CallbackQuery):
    tovar_id = call.data[6:]

    markup = inline_kb_menu.tovar_card_markup(tovar_id, call.from_user.id)
    tovar_name, tovar_price, tovar_disc, tovar_photo = db_tovars.tovar_card(tovar_id)
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    await dp.bot.send_photo(chat_id=call.message.chat.id,
                            photo=tovar_photo,
                            caption=f'{tovar_name}: \t{tovar_price}₽ \n\n{tovar_disc}',
                            reply_markup=markup)

@dp.callback_query_handler(text_startswith='basketAdd_')
async def show_catalog(call: CallbackQuery):
    tovar_id = call.data[10:]
    tovar_price = db_tovars.tovar_price(tovar_id)
    tovar_name = db_tovars.tovar_name(tovar_id)
    db_users.add_tovar_(tovar_id, call.from_user.id, tovar_name, tovar_price=tovar_price, count=1)

    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    await dp.bot.send_message(call.message.chat.id, 'Товар добавлен в корзину! :)')


@dp.callback_query_handler(text_startswith='setFavourite_')
async def show_catalog(call: CallbackQuery):
    tovar_id = call.data[13:]
    tovar_name = db_tovars.tovar_name(tovar_id)
    db_users.set_favourite(tovar_id, call.from_user.id, tovar_name)
    await call.message.edit_reply_markup(inline_kb_menu.tovar_card_markup(tovar_id, call.from_user.id))


@dp.callback_query_handler(text_startswith='delFavourite_')
async def show_catalog(call: CallbackQuery):
    tovar_id = call.data[13:]
    user_id = call.from_user.id
    tovar_name = db_tovars.tovar_name(tovar_id)

    db_users.set_favourite(tovar_id, user_id, tovar_name)
    await call.message.edit_reply_markup(inline_kb_menu.favourite_markup(user_id))


@dp.callback_query_handler(text_startswith='setCount_')
async def show_catalog(call: CallbackQuery):
    tovar_id = call.data[9:]
    tovar_name = db_tovars.tovar_name(tovar_id)
    await call.message.answer(f'Введите количество необходимого товара "{tovar_name}":')
    await State.count.set()

@dp.message_handler(state=State.count)
async def state1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(count=answer)

    await message.answer(f'{answer} шт. уже в корзине 😉')
    await state.finish()
