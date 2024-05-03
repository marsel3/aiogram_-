from aiogram.utils.markdown import hlink

from data.config import admin_chat
from loader import dp
from keyboards.inline import inline_kb_menu
from keyboards.default import keyboard_menu
from aiogram import types
from utils.db_api.db_asyncpg import *
from states.state import SetCount, SetCountInBasket, Search, ConfirmOrder
from aiogram.dispatcher import FSMContext
from handlers.users.admin import try_edit_call, try_delete_call, try_delete_msg, delete_messages, tovar_info_text
from handlers.users.commands import start_menu


@dp.message_handler(text='отмена', state="*")
async def start_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data["msg_list"].append(message.message_id)
            await delete_messages(messages=data["msg_list"], chat_id=message.from_user.id)
        except:
            pass

        await state.finish()
        await start_menu(message)


@dp.message_handler(commands='start', state="*")
async def start_state(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data["msg_list"].append(message.message_id)
            await delete_messages(messages=data["msg_list"], chat_id=message.from_user.id)
        except:
            pass

        await state.finish()
        await start_menu(message)


async def send_basket(chat_id, user_id, bonus=False):
    basket = await basket_list(user_id)
    markup = await inline_kb_menu.basket_markup(basket=basket, bonus=bonus)
    sale = (await user_info_by_id(user_id))["bonus"]

    string = f'<b>Корзина.</b>'
    summ = 0
    count = 1
    if len(basket) > 0:
        for tovar in basket:
            string += f'\n\n{count}. «<code>{tovar["tovar"]}</code>» ' \
                      f'\n\t\t\tЦена: {tovar["price"]} × {tovar["count"]}  =  {tovar["price"] * tovar["count"]} рублей'
            summ += tovar["price"] * tovar["count"]
            count += 1
        string += '\n__________________' + '_' * len(str(summ))
    if bonus:
        string += f'\nИспользовано бонусов: {sale}₽'
        summ -= sale
    string += f'\nИтого: {summ} рублей'

    await dp.bot.send_message(chat_id=chat_id, text=string, reply_markup=markup, parse_mode="HTML")


@dp.callback_query_handler(text='DeleteMessage')
async def DeleteMessage(call: types.CallbackQuery):
    await try_delete_call(call)


@dp.callback_query_handler(text_startswith='_')
async def show_catalog(call: types.CallbackQuery):
    await call.message.edit_text('Блок в разработке..')


@dp.callback_query_handler(text='back_to_menu')
async def back_to_menu(call: types.CallbackQuery):
    await call.message.edit_text(text='Вы вернулись в главное меню\nНажимай на каталог и начинай собирать заказ 😉')


@dp.callback_query_handler(text='back_to_catalog')
async def back_to_catalog(call: types.CallbackQuery):
    await call.message.edit_text(text=f'Вы перешли в каталог, выберите категорию нужного вам товара.',
                                 reply_markup=await inline_kb_menu.categories_markup())


@dp.callback_query_handler(text_startswith='categories')
async def categories_menu(call: types.CallbackQuery):
    markup = await inline_kb_menu.categories_markup()
    text = 'Вы перешли в каталог, выберите категорию нужного вам товара.'

    await try_edit_call(callback=call, text=text, markup=markup)


@dp.callback_query_handler(text_startswith='category_')
async def tovar_list(call: types.CallbackQuery):
    page = int(call.data.split('_')[1])
    category_id = int(call.data.split('_')[2])

    text = f'Какой товар выберите?  😏'
    markup = await inline_kb_menu.tovar_list_markup(category_id=category_id, page=page)
    await try_edit_call(callback=call, text=text, markup=markup)


@dp.callback_query_handler(text_startswith='tovar-info_')
async def tovar_info_menu(call: types.CallbackQuery):
    page = int(call.data.split('_')[1])
    category_id = int(call.data.split('_')[2])
    tovar_id = int(call.data.split('_')[3])
    count = int(call.data.split('_')[4])
    tovar_info = await tovar_info_by_id(id=tovar_id)
    if tovar_info:
        tovar_list = await tovars_by_category(category_id=category_id)
        tovar_list_indexes = [tovar['id'] for tovar in tovar_list]
        pages = len(tovar_list_indexes)
        prev_tovar_id = tovar_list_indexes[page - 2] if page - 2 >= 0 else tovar_list_indexes[-1]
        next_tovar_id = tovar_list_indexes[page % pages] if page % pages != 0 else tovar_list_indexes[0]

        msg_text = await tovar_info_text(title=tovar_info["tovar"], price=tovar_info["price"],
                                         description=tovar_info["description"],
                                         iscount=True, pages=pages, page=1+tovar_list_indexes.index(tovar_id))
        photo = tovar_info["photo"]
        markup = await inline_kb_menu.tovar_info_markup(user_id=call.from_user.id, page=page, category_id=category_id,
                                                        tovar_id=tovar_id, pages=pages, next_tovar_id=next_tovar_id,
                                                        prev_tovar_id=prev_tovar_id, count=count)

        try:
            await try_delete_call(call)
            await call.message.answer_photo(photo=photo, caption=msg_text, reply_markup=markup)
        except:
            await try_edit_call(callback=call, text=msg_text, markup=markup)
    else:
        await call.answer('Товар больше не доступен!')


"""@dp.callback_query_handler(text_startswith='setTovarCount_')
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
"""


@dp.callback_query_handler(text_startswith='setFavourite_')
async def setFavourite_(call: types.CallbackQuery):
    product_id = int(call.data.split('_')[3])
    await tovar_set_favourite(product_id=product_id, user_id=call.from_user.id)
    await tovar_info_menu(call)


@dp.callback_query_handler(text_startswith='basketAdd_')
async def basketAdd_(call: types.CallbackQuery):
    await tovar_add_to_basket(user_id=int(call.from_user.id), product_id=int(call.data.split('_')[3]),
                              count=int(call.data.split('_')[4]))
    await try_delete_call(call)

    await call.message.answer(text=f'Товар добавлен в корзину 😉',
                              reply_markup=await inline_kb_menu.continue_shopping())


@dp.callback_query_handler(text='confirm_order')
async def confirm_order(call: types.CallbackQuery):
    await try_delete_call(call)
    await ConfirmOrder.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer(text='Напишите имя получателя', reply_markup=keyboard_menu.cancel)
        data["msg_list"] = [msg.message_id]
        data["callback"] = call
    await ConfirmOrder.fio.set()


@dp.message_handler(state=ConfirmOrder.fio)
async def ConfirmOrder_fio(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
        data["msg_list"] = []

        data["fio"] = message.text
        msg = await message.answer('Укажите ваш номер телефона, для связи', reply_markup=keyboard_menu.phone)
        data["msg_list"].append(msg.message_id)
        await ConfirmOrder.phone.set()

    await ConfirmOrder.phone.set()


@dp.message_handler(state=ConfirmOrder.phone, content_types=types.ContentType.ANY)
async def ConfirmOrder_phone(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
        data["msg_list"] = []

        if message.contact:
            data['phone'] = message.contact.phone_number
        elif len(message.text) > 1 and message.text[1:].isdigit():
            data['phone'] = message.text

        else:
            msg = await message.answer(text='📲 Введите правильный номер телефона!')
            data["msg_list"].append(msg.message_id)
            await ConfirmOrder.phone.set()
            return

        try:
            basket = await basket_list(user_id=user_id)
            if not basket:
                await state.finish()
                await message.answer(text='Кажется ваша корзина пуста! Попробуйте снова :)',
                                     reply_markup=keyboard_menu.main)

            string = f'<b>Корзина.</b>:'
            count, summ = 1, 0

            for tovar in basket:
                string += f'\n{count}. «{tovar["tovar"]}»(Артикул: <code>{tovar["id"]}</code>) ' \
                          f'\n\t\t\tЦена: {tovar["price"]} × {tovar["count"]}  =  {tovar["price"] * tovar["count"]}₽\n'
                summ += tovar["price"] * tovar["count"]
                count += 1

                string += '__________________' + '_' * len(str(summ))
            string += f'\nИтого: {summ}₽'

            app_id = await add_history(user_id=user_id, total=summ)
            msg_text = f'Заказ №{app_id}' \
                       f'\n\nОт {hlink(data["fio"], message.from_user.url)}' \
                       f'{"(@" + message.from_user.username + ")" if message.from_user.username else ""}' \
                       f'\n\n<b>Контакты</b>: {data["phone"]}' \
                       f'\n\n{string}'
            markup = await inline_kb_menu.adminconfirm(user_id=user_id, app_id=app_id)
            await dp.bot.send_message(chat_id=admin_chat, text=msg_text, reply_markup=markup)
            await message.answer(text='Заявка направлкна менеджеру! В ближайшее время мы с вами свяжемся! 💫',
                                 reply_markup=keyboard_menu.main)
            await basket_clear(user_id=user_id)
        except:
            await message.answer(text='Упс.. Что-то пошло не так, пожалуйста, попробуйте снова!',
                                 reply_markup=keyboard_menu.main)

    await state.finish()


@dp.callback_query_handler(text_startswith='admin-confirm_')
async def adminconfirm(call: types.CallbackQuery):
    user_id = int(call.data.split('_')[2])
    app_id = int(call.data.split('_')[3])
    new_text = f'{call.message.html_text}' \
               f'\n\nРешение администратора({hlink(call.from_user.full_name, call.from_user.url)} ' \
               f'{"@" + call.from_user.username if call.from_user.username else ""}): '

    if call.data.split('_')[1] == '1':
        try:
            await dp.bot.send_message(chat_id=user_id, text='Менеджер подтвердил вашу заявку! 🙌')
        except:
            pass
        new_text += f'<code>Заявка подтверждена</code>'

    else:
        await del_history(id=app_id)
        try:
            await dp.bot.send_message(chat_id=user_id, text='К сожалению, менеджер отклонил вашу заявку! :(')
        except:
            pass
        new_text += f'<code>Заявка отклонена</code>'

    await try_edit_call(callback=call, text=new_text, markup=None)


@dp.callback_query_handler(text_startswith='delFavourite_')
async def delFavourite_(call: types.CallbackQuery):
    user_id = int(call.from_user.id)
    await tovar_favourite_del(product_id=int(call.data.split('_')[1]), user_id=user_id)
    await call.message.edit_reply_markup(await inline_kb_menu.favourite_markup(user_id))


@dp.callback_query_handler(text='clearFavourite')
async def clearFavourite(call: types.CallbackQuery):
    user_id = int(call.from_user.id)
    await tovar_favourite_clear(user_id=user_id)
    await call.message.edit_reply_markup(reply_markup=await inline_kb_menu.favourite_markup(user_id))


@dp.callback_query_handler(text_startswith='ApplyBonus_')
async def ApplyBonus_(call: types.CallbackQuery):
    await try_delete_call(call)
    await send_basket(chat_id=call.message.chat.id, user_id=call.from_user.id, bonus=eval(call.data.split('_')[1]))


@dp.callback_query_handler(text_startswith='delBasket_')
async def delBasket_(call: types.CallbackQuery):
    user_id = int(call.from_user.id)
    await basket_tovar_del(product_id=int(call.data.split('_')[1]), user_id=user_id)
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
        data["product_id"] = int(call.data.split('_')[1])
    await SetCountInBasket.count.set()


@dp.message_handler(state=SetCountInBasket.count)
async def SetCountInBasket_count(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)

        user_id = int(message.from_user.id)
        if message.text.isdigit():
            if int(message.text) > 0:
                await basket_tovar_set_count(product_id=data["product_id"], count=int(message.text))
            else:
                await basket_tovar_del(product_id=data["product_id"], user_id=user_id)

        await send_basket(chat_id=message.chat.id, user_id=user_id)
    await state.finish()


@dp.callback_query_handler(text='SearchTovar')
async def search(call: types.CallbackQuery):
    await try_delete_call(call)
    msg = await call.message.answer(f'Введи название неоходимого товара:')
    await Search.msg_list.set()

    state = dp.get_current().current_state()
    async with state.proxy() as data:
        data["msg_list"] = [msg.message_id]
    await Search.tovar_name.set()


@dp.message_handler(state=Search.tovar_name)
async def search_tovar(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)

    tovar_list = await search_tovar_by_name(message.text)
    text = 'Список найденных товаров' if len(tovar_list) > 0 else 'Товар не найден 😟'

    await message.answer(text=text, reply_markup=await inline_kb_menu.tovar_search_markup(tovars=tovar_list))
    await state.finish()
