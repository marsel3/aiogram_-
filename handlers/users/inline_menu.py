from aiogram.types import CallbackQuery
from loader import dp, db_tovars, db_users
from states.state import State1
from keyboards.inline import inline_kb_menu
from aiogram.dispatcher import FSMContext
from aiogram import types
from handlers.users import default_menu


@dp.callback_query_handler(text='test1')
async def show_catalog(call: CallbackQuery):
    await call.message.edit_text('C новой обновой заработает...')


@dp.callback_query_handler(text='back_to_menu')
async def back_to_menu(call: CallbackQuery):
    await call.message.edit_text('Вы вернулись в главное меню\nНажимай на каталог и начинай собирать заказ 😉')


@dp.callback_query_handler(text='back_to_catalog')
async def back_to_catalog(call: CallbackQuery):
    await call.message.answer(f'Вы перешли в каталог, выберите категорию нужного вам товара.',
                              reply_markup=inline_kb_menu.catalog_markup())


@dp.callback_query_handler(text='search')
async def search(call: CallbackQuery):
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)

    await call.message.answer(f'Введи название неоходимого товара:')
    await State1.search_tovar.set()


@dp.message_handler(state=State1.search_tovar)
async def search_tovar(message: types.Message, state: FSMContext):
    answer = message.text.lower()
    m1 = db_tovars.tovar_search(answer)
    if len(m1) > 0:
        markup = inline_kb_menu.search_markup(m1)
        await message.answer('Список найденных товаров', reply_markup=markup)
    else:
        await message.answer('Товар не найден 😟', reply_markup=inline_kb_menu.catalog_markup())
    await state.finish()



@dp.callback_query_handler(text_startswith='category_id')
async def category_list(call: CallbackQuery):
    category_id = call.data[11:]
    await call.message.edit_text(f'Какой товар выберите?  😏',
                                 reply_markup=inline_kb_menu.tovar_markup(category_id))


@dp.callback_query_handler(text_startswith='back_to_tovars_')
async def back_to_tovars_(call: CallbackQuery):
    category_id = call.data[15:]
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    await dp.bot.send_message(chat_id=call.message.chat.id,
                              text=f'Вы вернулись в категорию "{db_tovars.category_name(category_id)}"'
                                   f'\n Какой товар выберите?  😏',
                              reply_markup=inline_kb_menu.tovar_markup(category_id))


@dp.callback_query_handler(text_startswith='tovar_')
async def tovar_card(call: CallbackQuery):
    tovar_id = call.data[6:]
    markup = inline_kb_menu.tovar_card_markup(tovar_id, call.from_user.id, 1)
    tovar_name, tovar_price, tovar_disc, tovar_photo = db_tovars.tovar_card(tovar_id)
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    try:
        await dp.bot.send_photo(chat_id=call.message.chat.id,
                                photo=tovar_photo,
                                caption=f'{tovar_name}: \t{tovar_price}₽ \n\n{tovar_disc}',
                                reply_markup=markup)
    except:
        await dp.bot.send_message(chat_id=call.from_user.id,
                                  text=f'{tovar_name}: \t{tovar_price}₽ \n\n{tovar_disc}',
                                  reply_markup=markup)


@dp.callback_query_handler(text_startswith='setFavourite_')
async def setFavourite_(call: CallbackQuery):
    pas, tovar_id, count = call.data.split('_')
    tovar_name = db_tovars.tovar_name(tovar_id)
    db_users.set_favourite(tovar_id, call.from_user.id, tovar_name)
    await call.message.edit_reply_markup(inline_kb_menu.tovar_card_markup(tovar_id, call.from_user.id, count))


@dp.callback_query_handler(text_startswith='delFavourite_')
async def delFavourite_(call: CallbackQuery):
    tovar_id = call.data[13:]
    user_id = call.from_user.id
    tovar_name = db_tovars.tovar_name(tovar_id)

    db_users.set_favourite(tovar_id, user_id, tovar_name)
    await call.message.edit_reply_markup(inline_kb_menu.favourite_markup(user_id))


@dp.callback_query_handler(text='cleanFavourite')
async def cleanFavourite(call: CallbackQuery):
    db_users.clean_favourite(call.from_user.id)
    await call.message.edit_reply_markup(reply_markup=inline_kb_menu.favourite_markup(call.from_user.id))


@dp.callback_query_handler(text='cleanBasket')
async def cleanBasket(call: CallbackQuery):
    db_users.clean_basket(call.from_user.id)
    markup, string = inline_kb_menu.basket_markup(call.from_user.id)
    await call.message.edit_text(text=string, reply_markup=markup)


@dp.callback_query_handler(text_startswith='basketAdd_')
async def basketAdd_(call: CallbackQuery):
    pas, tovar_id, count = call.data.split('_')

    markup = inline_kb_menu.catalog_markup()
    tovar_name = db_tovars.tovar_name(tovar_id)
    tovar_price = db_tovars.tovar_price(tovar_id)
    db_users.basket_add(tovar_id, call.from_user.id, tovar_name, tovar_price, count=int(count))
    await dp.bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
    await call.message.answer(f'Товар доавлен в корзину 😉\nВы перешли в каталог, выберите категорию нужного вам товара.',
                                reply_markup=markup)


@dp.callback_query_handler(text_startswith='minusCount_')
async def basketAdd_(call: CallbackQuery):
    pas, tovar_id, count = call.data.split('_')
    count = int(count)
    if count - 1 > 0:
        await call.message.edit_reply_markup(reply_markup=inline_kb_menu.tovar_card_markup(tovar_id,
                                                                                           call.from_user.id, count-1))
    else:
        pass

@dp.callback_query_handler(text_startswith='plusCount_')
async def basketAdd_(call: CallbackQuery):
    pas, tovar_id, count = call.data.split('_')
    count = int(count) + 1
    await call.message.edit_reply_markup(reply_markup=inline_kb_menu.tovar_card_markup(tovar_id,
                                                                                       call.from_user.id, count))

"""@dp.callback_query_handler(text_startswith='basketAdd_')
async def basketAdd_(call: CallbackQuery):
    tovar_id = call.data[10:]

    await State1.tovar_id.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        data["tovar_id"] = tovar_id

    tovar_name = db_tovars.tovar_name(tovar_id)
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    await call.message.answer(f'Введите количество необходимого товара "{tovar_name}":')
    await State1.count.set()

@dp.message_handler(state=State1.count)
async def add_to_basket(message: types.Message, state: FSMContext):
    answer = message.text
    markup = inline_kb_menu.catalog_markup()
    if answer.isdigit() and int(answer) > 0:
        async with state.proxy() as data:
            tovar_id = data['tovar_id']
        tovar_name = db_tovars.tovar_name(tovar_id)
        tovar_price = db_tovars.tovar_price(tovar_id)
        db_users.basket_add(tovar_id, message.from_user.id, tovar_name, tovar_price, count=int(answer))
        await message.answer(f'Товар доавлен в корзину 😉\nВы перешли в каталог, выберите категорию нужного вам товара.',
                             reply_markup=markup)
    else:
        await message.answer(f'Товар не добавлен 😟. В следующий раз вводи число😉'
                             f'\nВы перешли в каталог, выберите категорию нужного вам товара.',
                             reply_markup=markup)
    await state.finish()
"""

@dp.callback_query_handler(text_startswith='delTovar_')
async def setCount_(call: CallbackQuery):
   tovar_id = call.data[9:]
   db_users.basket_delete(tovar_id, call.from_user.id)
   markup, string = inline_kb_menu.basket_markup(call.from_user.id)
   await dp.bot.send_message(chat_id=call.from_user.id,
                             text=string, reply_markup=markup)


@dp.callback_query_handler(text_startswith='setCount_')
async def setCount_(call: CallbackQuery):
    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    tovar_id = call.data[9:]
    tovar_name = db_tovars.tovar_name(tovar_id)

    await State1.tovar_id.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        data["tovar_id"] = tovar_id

    await call.message.answer(f'Сколько единиц товара "{tovar_name}" оставить в корзине:')
    await State1.new_count.set()


@dp.message_handler(state=State1.new_count)
async def set_to_basket(message: types.Message, state: FSMContext):
    answer = message.text
    if answer.isdigit():
        async with state.proxy() as data:
            tovar_id = data['tovar_id']

        if int(answer) > 0:
            db_users.basket_set(tovar_id, message.from_user.id, int(answer))
        else:
            db_users.basket_delete(tovar_id, message.from_user.id)
            await message.answer(f'Я тебя понял))) это означало удалить этот товар из корзины!')
    else:
        await message.answer(f'Количество не изменено 😟. В следующий раз вводи число😉')
    await state.finish()
    await default_menu.show_basket(message)


