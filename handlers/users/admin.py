from filters import IsAdmin
from aiogram import types
from loader import dp
from aiogram.dispatcher import FSMContext
from states.state import FSMAdmin, FSMAdminEdit, AdminSpam
from keyboards import admin_keyboards
from utils.db_api.db_asyncpg import *
from handlers.users.inline_menu import try_edit_call, try_delete_call, delete_messages, try_delete_msg


@dp.message_handler(IsAdmin(), text='/admin')
async def admin(messsage: types.Message):
    await messsage.answer(f'Здравствуйте, {messsage.from_user.full_name},  вы попали в админ панель!',
                          reply_markup=admin_keyboards.admin_panel)


@dp.callback_query_handler(text='admin_panel')
async def admin_panel(call: types.CallbackQuery):
    await try_edit_call(callback=call, markup=admin_keyboards.admin_panel,
                        text=f'Здравствуйте, {call.from_user.full_name},  вы попали в админ панель!')


@dp.callback_query_handler(text='admin_send_message')
async def admin_send_message(call: types.CallbackQuery):
    msg = await try_edit_call(callback=call, markup=admin_keyboards.cancel,
                              text=f'Введите сообщения для рассылки всем пользователям')
    await AdminSpam.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        data["msg_list"] = [msg.message_id]
    await AdminSpam.next()


@dp.message_handler(state=AdminSpam.text)
async def AdminSpam_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        if message.text.lower() == 'отмена':
            msg = await message.answer('Рассылка отменена!', reply_markup=None)
            data["msg_list"].append(msg.message_id)
            await admin(message)
            await state.finish()
            await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)

        else:
            data["text"] = message.text
            msg = await message.answer(text=data["text"])
            msg2 = await message.answer("Всё верно?", reply_markup=admin_keyboards.agreement)   # Для удаления клавы
            data["msg_list"].append(msg.message_id)
            data["msg_list"].append(msg2.message_id)
            await AdminSpam.confirm.set()


@dp.message_handler(state=AdminSpam.confirm)
async def AdminSpam_confirm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        if message.text.lower() == 'да':
            await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
            await state.finish()
            users = await user_list()
            msg = await message.answer('Бот начал рассылку!')
            for user in users:
                try:
                    await dp.bot.send_message(chat_id=user["user_id"], text=data["text"])
                except:
                    pass
            await message.answer('Рассылка завершена!', reply_markup=None)
        else:
            await message.answer('Рассылка отменена!', reply_markup=None)

    data["msg_list"].append(msg.message_id)
    await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
    await admin(message)
    await state.finish()


@dp.callback_query_handler(text='admin_statistic')
async def admin_statistic(call: types.CallbackQuery):
    users = await user_list()
    await try_edit_call(callback=call, text=f'Сейчас ботом пользуются {len(users)} чел.',
                        markup=admin_keyboards.back_to_admin_panel)


@dp.callback_query_handler(text='admin_all_categories')
async def admin_all_categories(call: types.CallbackQuery):
    await try_edit_call(callback=call, text='Вы в меню редактора категорий',
                        markup=await admin_keyboards.admin_catalog_markup())


@dp.callback_query_handler(text='AddNewCategory')
async def add_new_category(call: types.CallbackQuery):
    await try_delete_call(call)
    await FSMAdmin.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer('Укажите название новой категории',
                                        reply_markup=admin_keyboards.cancel)
        data["msg_list"] = [msg.message_id]
    await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.category)
async def FSMAdmin_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() != 'отмена':
            await add_category(message.text)
        msg = await message.answer("Обработка...", reply_markup=None)   # Для удаления клавы
        data["msg_list"].append(message.message_id)
        data["msg_list"].append(msg.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
        await message.answer(text='Вы в меню редактора категорий',
                             reply_markup=await admin_keyboards.admin_catalog_markup())
    await state.finish()


@dp.callback_query_handler(text_startswith='adminCategory_')
async def adminCategory_(call: types.CallbackQuery):
    category_id = int(call.data.split('_')[1])
    category = await category_name_by_id(category_id)
    await try_edit_call(callback=call, text=f'Вы в меню редактора категории «{category}»',
                        markup=await admin_keyboards.admin_tovars_markup(category_id))


@dp.callback_query_handler(text_startswith='adminDelCategory_')
async def adminDelCategory_(call: types.CallbackQuery):
    await del_category(int(call.data.split('_')[1]))
    await try_edit_call(callback=call, text=f'Вы в меню редактора категорий',
                        markup=await admin_keyboards.admin_catalog_markup())


@dp.callback_query_handler(text_startswith='adminEditCategory_')
async def adminEditCategory_(call: types.CallbackQuery):
    await try_delete_call(call)
    await FSMAdminEdit.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer('Укажите новое название категории',
                                        reply_markup=admin_keyboards.cancel)
        data["category_id"] = int(call.data.split('_')[1])
        data["msg_list"] = [msg.message_id]
    await FSMAdminEdit.category_name.set()


@dp.message_handler(state=FSMAdminEdit.category_name)
async def FSMAdminEdit_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() != 'отмена':
            await edit_category_name(id=data["category_id"], category=message.text)

        msg = await message.answer("Обработка...", reply_markup=None)   # Для удаления клавы
        data["msg_list"].append(message.message_id)
        data["msg_list"].append(msg.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
        category = await category_name_by_id(data["category_id"])
        await message.answer(text=f'Вы в меню редактора категории «{category}»',
                             reply_markup=await admin_keyboards.admin_tovars_markup(data["category_id"]))
    await state.finish()


@dp.callback_query_handler(text_startswith='AddNewTovar_')
async def AddNewTovar_(call: types.CallbackQuery):
    await try_delete_call(call)
    await FSMAdmin.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer('Укажите название товара',
                                        reply_markup=admin_keyboards.cancel)
        data["msg_list"] = [msg.message_id]
        data["category_id"] = int(call.data.split('_')[1])
    await FSMAdmin.tovar_name.set()


@dp.message_handler(state=FSMAdmin.tovar_name)
async def AddNewTovar_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        if message.text.lower() == 'отмена':
            await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
            await state.finish()
            category = await category_name_by_id(data["category_id"])
            await message.answer(text=f'Вы в меню редактора категории «{category}»',
                                 reply_markup=await admin_keyboards.admin_tovars_markup(data["category_id"]))
        else:
            data["tovar_name"] = message.text
            msg = await message.answer("Укажите цену товара", reply_markup=None)
            data["msg_list"].append(msg.message_id)
            await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.tovar_price)
async def AddNewTovar_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        if message.text.lower() == 'отмена':
            await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
            await state.finish()
            category = await category_name_by_id(data["category_id"])
            await message.answer(text=f'Вы в меню редактора категории «{category}»',
                                 reply_markup=await admin_keyboards.admin_tovars_markup(data["category_id"]))

        elif message.text.isdigit():
            data["tovar_price"] = int(message.text)
            msg = await message.answer("Отправьте описание товара", reply_markup=admin_keyboards.withoutdesc)
            data["msg_list"].append(msg.message_id)
            await FSMAdmin.next()

        else:
            msg = await message.answer("Укажите цену товара", reply_markup=None)
            data["msg_list"].append(msg.message_id)
            await FSMAdmin.tovar_price.set()


@dp.message_handler(state=FSMAdmin.tovar_disc)
async def AddNewTovar_disc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        if message.text.lower() == 'отмена':
            await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
            await state.finish()

            category = await category_name_by_id(data["category_id"])
            await message.answer(text=f'Вы в меню редактора категории «{category}»',
                                 reply_markup=await admin_keyboards.admin_tovars_markup(data["category_id"]))
        else:
            data["tovar_disc"] = message.text if message.text != 'Без описания' else None
            msg = await message.answer("Отправьте фото товара", reply_markup=admin_keyboards.without_photo)
            data["msg_list"].append(msg.message_id)
            await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.tovar_photo)
async def AddNewTovar_without_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        if message.text.lower() == 'отмена':
            await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
            await state.finish()

            category = await category_name_by_id(data["category_id"])
            await message.answer(text=f'Вы в меню редактора категории «{category}»',
                                 reply_markup=await admin_keyboards.admin_tovars_markup(data["category_id"]))
        else:
            data["tovar_photo"] = None
            disc = f'\n\nОписание: <code>{data["tovar_disc"]}</code>' if data["tovar_disc"] else ''
            msg = await message.answer(text=f'{data["tovar_name"]}: \t{data["tovar_price"]} руб.{disc}')
            msg2 = await message.answer(f'Всё верно?', reply_markup=admin_keyboards.agreement)
            data["msg_list"].append(msg.message_id)
            data["msg_list"].append(msg2.message_id)
            await FSMAdmin.next()


@dp.message_handler(content_types=['photo'], state=FSMAdmin.tovar_photo)
async def AddNewTovar_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        data["tovar_photo"] = message.photo[0].file_id
        disc = f'\n\nОписание: <code>{data["tovar_disc"]}</code>' if data["tovar_disc"] else ''
        msg = await message.answer_photo(photo=data["tovar_photo"], caption=f'{data["tovar_name"]}:'
                                                                            f' \t{data["tovar_price"]} руб.{disc}')
        msg2 = await message.answer(f'Всё верно?', reply_markup=admin_keyboards.agreement)
        data["msg_list"].append(msg.message_id)
        data["msg_list"].append(msg2.message_id)
        await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.agreement)
async def FSMAdmin_agreement(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg = await message.answer("Обработка...", reply_markup=None)   # Для удаления клавы
        data["msg_list"].append(msg.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)

        if message.text == 'Да':
            tovar_id = await add_tovar(category=data["category_id"],
                                       name=data["tovar_name"],
                                       price=data["tovar_price"],
                                       disc=data["tovar_disc"],
                                       photo=data["tovar_photo"])
            await send_admin_tovar(chatId=message.chat.id, msgId=message.message_id, tovar_id=tovar_id)
        else:
            category = await category_name_by_id(data["category_id"])
            await message.answer(text=f'Вы в меню редактора категории «{category}»',
                                 reply_markup=await admin_keyboards.admin_tovars_markup(data["category_id"]))
    await state.finish()


async def send_admin_tovar(chatId, msgId, tovar_id):
    tovar_info = await tovar_by_id(tovar_id)
    disc = f'\n\nОписание: <code>{tovar_info["disc"]}</code>' if tovar_info["disc"] else ''
    text = f'{tovar_info["name"]}: \t{tovar_info["price"]}₽{disc}'
    photo = tovar_info["photo"]
    markup = await admin_keyboards.admin_tovar_markup(tovar_id)

    await try_delete_msg(chatId=chatId, msgId=msgId)
    try:
        await dp.bot.send_photo(chat_id=chatId, photo=photo, caption=text, reply_markup=markup)
    except:
        await dp.bot.send_message(chat_id=chatId, text=text, reply_markup=markup)


@dp.callback_query_handler(text_startswith='adminTovar_')
async def adminTovar_(call: types.CallbackQuery):
    await send_admin_tovar(chatId=call.message.chat.id, msgId=call.message.message_id,
                           tovar_id=int(call.data.split('_')[1]))


@dp.callback_query_handler(text_startswith='adminDeleteTovar_')
async def adminDelCategory_(call: types.CallbackQuery):
    await del_tovar(int(call.data.split('_')[2]))
    await adminCategory_(call)