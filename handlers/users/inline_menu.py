from loader import dp
from keyboards.inline import inline_kb_menu
from aiogram import types
from utils.db_api.db_asyncpg import *
from states.state import SetCount, SetCountInBasket, Search
from aiogram.dispatcher import FSMContext
from handlers.users.default_menu import send_basket


async def delete_messages(messages, chat_id):
    for msg_id in messages:
        try:
            await dp.bot.delete_message(chat_id=chat_id, message_id=msg_id)
        except:
            pass


async def try_delete_call(call: types.CallbackQuery):
    try:
        await call.message.delete()
    except:
        pass


async def try_delete_msg(chatId, msgId):
    try:
        await dp.bot.delete_message(chat_id=chatId, message_id=msgId)
    except:
        pass


async def try_edit_call(callback, text, markup):
    try:
        msg = await callback.message.edit_text(text=text, parse_mode='HTML', reply_markup=markup)
    except:
        await try_delete_call(callback)
        msg = await callback.message.answer(text=text, parse_mode='HTML', reply_markup=markup)
    return msg


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


@dp.callback_query_handler(text='test')
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
    await try_edit_call(callback=call, text=text, markup=markup)


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
    await try_delete_call(call)
    await SetCount.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer('Укажите количество товара')
        data["msg_list"] = [msg.message_id]
        data["tovar_id"] = call.data.split('_')[1]
    await SetCount.count.set()


@dp.message_handler(state=SetCount.count)
async def SetCount_count(message: types.Message, state: FSMContext):
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
    await try_delete_call(call)

    await call.message.answer(text=f'Товар доавлен в корзину 😉\nВы перешли в каталог, '
                                   f' категорию нужного вам товара.',
                              reply_markup=await inline_kb_menu.categories_markup())


@dp.callback_query_handler(text_startswith='delFavourite_')
async def delFavourite_(call: types.CallbackQuery):
    user_id = int(call.from_user.id)
    await tovar_favourite_del(tovar_id=int(call.data.split('_')[1]), user_id=user_id)
    await call.message.edit_reply_markup(await inline_kb_menu.favourite_markup(user_id))


@dp.callback_query_handler(text='clearFavourite')
async def clearFavourite(call: types.CallbackQuery):
    user_id = int(call.from_user.id)
    await tovar_favourite_clear(user_id=user_id)
    await call.message.edit_reply_markup(reply_markup=await inline_kb_menu.favourite_markup(user_id))


@dp.callback_query_handler(text_startswith='delBasket_')
async def delBasket_(call: types.CallbackQuery):
    user_id = int(call.from_user.id)
    await basket_tovar_del(tovar_id=int(call.data.split('_')[1]), user_id=user_id)
    await send_basket(chat_id=call.message.chat.id, user_id=user_id)
    await try_delete_call(call)


@dp.callback_query_handler(text='clearBasket')
async def clearBasket(call: types.CallbackQuery):
    await basket_clear(user_id=call.from_user.id)
    await send_basket(chat_id=call.message.chat.id, user_id=call.from_user.id)
    await try_delete_call(call)


@dp.callback_query_handler(text_startswith='setCountInBasket_')
async def setCountInBasket_(call: types.CallbackQuery):
    await try_delete_call(call)

    await SetCountInBasket.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer('Укажите количество товара')
        data["msg_list"] = [msg.message_id]
        data["tovar_id"] = int(call.data.split('_')[1])
    await SetCountInBasket.count.set()


@dp.message_handler(state=SetCountInBasket.count)
async def SetCountInBasket_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user_id = int(message.from_user.id)
        if message.text.isdigit():
            if int(message.text) > 0:
                await basket_tovar_set_count(tovar_id=data["tovar_id"], count=int(message.text))
            else:
                await basket_tovar_del(tovar_id=data["tovar_id"], user_id=user_id)

        await send_basket(chat_id=message.chat.id, user_id=user_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
    await state.finish()


@dp.callback_query_handler(text='SearchTovar')
async def search(call: types.CallbackQuery):
    await try_delete_call(call)
    await call.message.answer(f'Введи название неоходимого товара:')
    await Search.tovar_name.set()


@dp.message_handler(state=Search.tovar_name)
async def search_tovar(message: types.Message, state: FSMContext):
    tovar_list = await search_tovar_by_name(message.text)
    text = 'Список найденных товаров' if len(tovar_list) > 0 else 'Товар не найден 😟'

    await message.answer(text=text, reply_markup=await inline_kb_menu.tovar_markup(tovar_list))
    await state.finish()
