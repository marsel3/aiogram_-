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
    try:
        await call.message.edit_text('C новой обновой заработает...')
    except:
        await dp.bot.delete_message(chat_id=call.message.chat.id,
                                    message_id=call.message.message_id)
        await dp.bot.send_message(chat_id=call.message.chat.id,
                                  text='C новой обновой заработает...')
    # await call.message.edit_text('Вы вернулись в каталог',
    #                           reply_markup=inline_kb_menu.tovar_markup(call.data))


@dp.callback_query_handler(text_startswith='tovar_')
async def show_catalog(call: CallbackQuery):
    tovar_id = call.data[6:]

    tovar_name, tovar_price, tovar_disc, tovar_photo = db_tovars.tovar_card(tovar_id)
    markup = inline_kb_menu.tovar_card_markup(tovar_id)

    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    await dp.bot.send_photo(caption=f'{tovar_name}: \t\t{tovar_price}₽ \n\n{tovar_disc}',
                            chat_id=call.message.chat.id,
                            photo=tovar_photo,
                            reply_markup=markup)
"""    try:

    except Exception as erros:
        print(erros)
        await dp.bot.send_message(chat_id=call.message.chat.id,
                                  text='Возникла ошибка с отправкой карточки товара, сообщите администратору!')
"""

@dp.callback_query_handler(text_startswith='add_')
async def show_catalog(call: CallbackQuery):
    tovar_id = call.data[4:]




    await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
    await dp.bot.send_message('Укажите',
                            chat_id=call.message.chat.id,
                            photo=tovar_photo,
                            reply_markup=markup)

    tovar_name, tovar_price, tovar_disc, tovar_photo = db_tovars.tovar_card(tovar_id)
    markup = inline_kb_menu.tovar_card_markup(tovar_id)


    try:
        await dp.bot.delete_message(call.message.chat.id, call.message.message_id)
        await dp.bot.send_photo(caption=f'{tovar_name}: \t\t{tovar_price}₽ \n\n{tovar_disc}',
                            chat_id=call.message.chat.id,
                            photo=tovar_photo,
                            reply_markup=markup)
    except:
        await dp.bot.send_message('Возникла ошибка с отправкой карточки товара, сообщите администратору!')

