
from loader import dp
from keyboards.inline import inline_kb_menu
from aiogram.dispatcher import FSMContext
from aiogram import types
from handlers.users import default_menu
from utils.db_api.db_asyncpg import *
from states.state import SetCount
from aiogram.dispatcher import FSMContext


async def delete_messages(messages, chat_id):
    for msg_id in messages:
        try:
            await dp.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except:
            pass


async def send_tovar_info(chatId, msgId, tovar_id, user_id, count=1):
    tovar_info = await tovar_by_id(tovar_id)

    text = f'{tovar_info["name"]}: \t{tovar_info["price"]}₽ \n\n{tovar_info["disc"]}'
    photo = tovar_info["photo"]
    markup = await inline_kb_menu.tovar_card_markup(tovar_id, count, user_id)

    await dp.bot.delete_message(chat_id=chatId, message_id=msgId)
    try:
        await dp.bot.send_photo(chat_id=chatId, photo=photo, caption=text, reply_markup=markup)
    except:
        await dp.bot.send_message(chat_id=chatId, text=text, reply_markup=markup)


@dp.callback_query_handler(text='test1')
async def show_catalog(call: types.CallbackQuery):
    await call.message.edit_text('C новой обновой заработает...')


@dp.callback_query_handler(text='back_to_menu')
async def back_to_menu(call: types.CallbackQuery):
    await call.message.edit_text(text='Вы вернулись в главное меню\nНажимай на каталог и начинай собирать заказ 😉')


@dp.callback_query_handler(text='back_to_catalog')
async def back_to_catalog(call: types.CallbackQuery):
    await call.message.edit_text(text=f'Вы перешли в каталог, выберите категорию нужного вам товара.',
                                 reply_markup=await inline_kb_menu.categories_markup())


@dp.callback_query_handler(text_startswith='category_')
async def tovar_list(call: types.CallbackQuery):
    category_id = int(call.data.split('_')[1])
    tovar_list = await tovar_by_category(category_id)
    text = f'Какой товар выберите?  😏'
    markup = await inline_kb_menu.tovar_markup(tovar_list)
    try:
        await call.message.edit_text(text=text, reply_markup=markup)
    except:
        await call.message.answer(text=text, reply_markup=markup)
        await call.message.delete()


@dp.callback_query_handler(text_startswith='tovar_')
async def tovar_info(call: types.CallbackQuery):
    tovar_id = int(call.data.split('_')[1])
    await send_tovar_info(chatId=call.message.chat.id, msgId=call.message.message_id, tovar_id=tovar_id,
                          user_id=call.from_user.id)



@dp.callback_query_handler(text_startswith='minusCount_')
async def minusCount_(call: types.CallbackQuery):
    pas, tovar_id, count = call.data.split('_')
    count = int(count)
    if count - 1 > 0:
        await call.message.edit_reply_markup(reply_markup=await inline_kb_menu.tovar_card_markup(tovar_id=int(tovar_id),
                                                                                                 count=count-1,
                                                                                                 user_id=int(call.from_user.id)))


@dp.callback_query_handler(text_startswith='plusCount_')
async def plusCount_(call: types.CallbackQuery):
    pas, tovar_id, count = call.data.split('_')
    await call.message.edit_reply_markup(reply_markup=await inline_kb_menu.tovar_card_markup(tovar_id=int(tovar_id),
                                                                                             count=int(count) + 1,
                                                                                             user_id=int(call.from_user.id)))


@dp.callback_query_handler(text_startswith='setTovarCount_')
async def plusCount_(call: types.CallbackQuery):
    await call.message.delete()
    await SetCount.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer('Укажите количество товара')
        data["msg_list"] = [msg.message_id]
        data["tovar_id"] = call.data.split('_')[1]
    await SetCount.count.set()


@dp.message_handler(state=SetCount.count)
async def MainMenuState(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        count = int(message.text) if message.text.isdigit() and int(message.text) > 0 else 1
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
        await send_tovar_info(chatId=message.chat.id, msgId=message.message_id, tovar_id=int(data["tovar_id"]),
                              count=count,  user_id=message.from_user.id)
    await state.finish()


@dp.callback_query_handler(text_startswith='setFavourite_')
async def setFavourite_(call: types.CallbackQuery):
    tovar_id = int(call.data.split('_')[1])

    await tovar_set_favourite(tovar_id=tovar_id, user_id=call.from_user.id)
    await call.message.edit_reply_markup(await inline_kb_menu.tovar_card_markup(tovar_id=tovar_id,
                                                                                count=int(call.data.split('_')[2]),
                                                                                user_id=int(call.from_user.id)))

@dp.callback_query_handler(text_startswith='basketAdd_')
async def basketAdd_(call: types.CallbackQuery):
    await tovar_add_to_basket(user_id=int(call.from_user.id), tovar_id=int(call.data.split('_')[1]),
                              count=int(call.data.split('_')[2]))
    await call.message.delete()

    await call.message.answer(text=f'Товар доавлен в корзину 😉\nВы перешли в каталог, '
                                   f' категорию нужного вам товара.',
                              reply_markup=await inline_kb_menu.categories_markup())


@dp.callback_query_handler(text_startswith='delFavourite_')
async def delFavourite_(call: types.CallbackQuery):
    user_id = int(call.from_user.id)
    await tovar_set_favourite(tovar_id=int(call.data.split('_')[1]), user_id=user_id)
    await call.message.edit_reply_markup(await inline_kb_menu.favourite_markup(user_id))


@dp.callback_query_handler(text='clearFavourite')
async def cleanFavourite(call: types.CallbackQuery):
    user_id = int(call.from_user.id)
    await tovar_favourite_clear(user_id=user_id)
    await call.message.edit_reply_markup(reply_markup=await inline_kb_menu.favourite_markup(user_id)



"""
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



@dp.callback_query_handler(text='cleanBasket')
async def cleanBasket(call: CallbackQuery):
    db_users.clean_basket(call.from_user.id)
    markup, string = inline_kb_menu.basket_markup(call.from_user.id)
    await call.message.edit_text(text=string, reply_markup=markup)




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


"""