from loader import dp
from filters import IsAdmin
from keyboards.default import keyboard_menu
from keyboards.inline import inline_kb_menu
from aiogram import types
from aiogram.types import InputFile
from aiogram.utils.markdown import hlink
import pandas as pd
import io

from aiogram.dispatcher import FSMContext
from states.state import AdminSpam, FSMAdmin, FSMAdminDelete, FSMAdminEdit
from utils.db_api.db_asyncpg import *


async def tovar_info_text(title, price, description, page=1, pages=1, iscount=True, rating=None):
    msg_text = f'Товар [{page} из {pages}]' if iscount else ''

    rating_text = ''
    if rating:
        rating_text = f"Оценка клиентов: {rating} из 5.0"

    msg_text += f'\n\n<b>{title}</b>' \
                f'\n\n<b>Цена</b>: <code>{price} ₽</code>' \
                f'\n\n<b>Описание</b>:\n<code>{description}</code>' \
                f'\n\n{rating_text}'

    return msg_text


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


async def digit_check(digit):
    digit = digit.replace(',', '.')
    try:
        digit = float(digit)
        if digit >= 0:
            return True
        else:
            return False
    except ValueError:
        return False


@dp.message_handler(IsAdmin(), text='/admin')
async def adminPanel(messsage: types.Message):
    await messsage.answer(f'Здравствуйте, {messsage.from_user.full_name},  вы попали в админ панель!',
                          reply_markup=inline_kb_menu.admin)


@dp.callback_query_handler(IsAdmin(), text='manager_main_menu')
async def manager_call_menu(call: types.CallbackQuery):
    msg_text = f'Здравствуйте, {call.from_user.full_name}, вы попали в меню менеджера!'
    markup = inline_kb_menu.admin

    await try_edit_call(callback=call, text=msg_text, markup=markup)


@dp.callback_query_handler(IsAdmin(), text='admin_all_users_info')
async def admin_all_users_info(call: types.CallbackQuery):
    await try_delete_call(call=call)
    msg = await call.message.answer('Подождите, файл формируется...')

    users = await get_all_users_data()
    df = pd.DataFrame(users, columns=['№', "Telegram id", "ФИО", "Статус"])

    excel_file_stream = io.BytesIO()
    with pd.ExcelWriter(excel_file_stream, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Users Info')
        workbook = writer.book
        worksheet = writer.sheets['Users Info']

        for idx, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
            worksheet.set_column(idx, idx, max_len)
    excel_file_stream.seek(0)

    await call.message.answer_document(document=InputFile(excel_file_stream, filename='Список пользователей.xlsx'),
                                       reply_markup=inline_kb_menu.back_to_admin)
    await dp.bot.delete_message(chat_id=call.message.chat.id, message_id=msg.message_id)


@dp.callback_query_handler(IsAdmin(), text='admin_send_message')
async def admin_send_message(call: types.CallbackQuery):
    msg = await try_edit_call(callback=call, markup=keyboard_menu.cancel,
                              text=f'Введите сообщения для рассылки всем пользователям')
    await AdminSpam.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        data["msg_list"] = [msg.message_id]
        data["callback"] = call

    await AdminSpam.text.set()


@dp.message_handler(state=AdminSpam.text, content_types=types.ContentType.ANY)
async def AdminSpam_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        if message.text:
            if message.text.lower() == 'отмена':
                msg = await message.answer('Рассылка отменена!', reply_markup=None)
                data["msg_list"].append(msg.message_id)
                await manager_call_menu(call=data["callback"])
                await state.finish()
                await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)

            else:
                data["text"] = message.html_text
                msg = await message.answer(text=data["text"])
                msg2 = await message.answer("Всё верно?", reply_markup=keyboard_menu.agreement)   # Для удаления клавы
                data["msg_list"].append(msg.message_id)
                data["msg_list"].append(msg2.message_id)
                await AdminSpam.confirm.set()
        elif message.video:
            data["text"] = message.html_text
            data["video"] = message.video.file_id
            msg = await message.answer_video(caption=data["text"], video=data["video"])
            msg2 = await message.answer("Всё верно?", reply_markup=keyboard_menu.agreement)  # Для удаления клавы
            data["msg_list"].append(msg.message_id)
            data["msg_list"].append(msg2.message_id)
            await AdminSpam.confirm.set()

        elif message.photo:
            data["text"] = message.html_text
            data["photo"] = message.photo[0].file_id
            msg = await message.answer_photo(caption=data["text"], photo=data["photo"])
            msg2 = await message.answer("Всё верно?", reply_markup=keyboard_menu.agreement)  # Для удаления клавы
            data["msg_list"].append(msg.message_id)
            data["msg_list"].append(msg2.message_id)
            await AdminSpam.confirm.set()

        else:
            await message.answer('Пока что я не поддерживаю такое сообщение для рассылки, напишите Марселю.')


@dp.message_handler(state=AdminSpam.confirm)
async def AdminSpam_confirm(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        if message.text.lower() == 'да':
            await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
            await state.finish()

            users = await active_users_list()
            msg = await message.answer('Бот начал рассылку!')
            for user in users:
                try:
                    if "video" in data:
                        if data["text"]:
                            await dp.bot.send_video(chat_id=user["user_id"], video=data["video"], caption=data["text"])
                        else:
                            await dp.bot.send_video(chat_id=user["user_id"], video=data["video"])
                    elif "photo" in data:
                        if data["text"]:
                            await dp.bot.send_photo(chat_id=user["user_id"], photo=data["photo"], caption=data["text"])
                        else:
                            await dp.bot.send_photo(chat_id=user["user_id"], photo=data["photo"])
                    else:
                        await dp.bot.send_message(chat_id=user["user_id"], text=data["text"])

                except:
                    pass
            await message.answer('Рассылка завершена!', reply_markup=None)
        else:
            await message.answer('Рассылка отменена!', reply_markup=None)

    data["msg_list"].append(msg.message_id)
    await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
    await manager_call_menu(data["callback"])
    await state.finish()


@dp.callback_query_handler(text='admin_all_categories')
async def admin_all_categories(call: types.CallbackQuery):
    await try_edit_call(callback=call, text='Вы в меню редактора категорий',
                        markup=await inline_kb_menu.admin_categories_markup())


@dp.callback_query_handler(text='AddNewCategory')
async def add_new_category(call: types.CallbackQuery):
    await try_delete_call(call)
    await FSMAdmin.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer('Укажите название новой категории',
                                        reply_markup=keyboard_menu.cancel)
        data["msg_list"] = [msg.message_id]
        data["callback"] = call
    await FSMAdmin.category.set()


@dp.message_handler(state=FSMAdmin.category)
async def FSMAdmin_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() != 'отмена':
            try:
                await add_category(category=message.text)
            except:
                await message.answer('Упс.. Что-то пошло не так!')
        msg = await message.answer("Обработка...", reply_markup=None)   # Для удаления клавы
        data["msg_list"].append(message.message_id)
        data["msg_list"].append(msg.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
        await admin_all_categories(call=data["callback"])
    await state.finish()


@dp.callback_query_handler(text_startswith='admin-category_')
async def adminCategory(call: types.CallbackQuery):
    category_id = int(call.data.split('_')[2])
    category = await category_name_by_id(category_id)
    await try_edit_call(callback=call, text=f'Вы в меню редактора категории «{category}»',
                        markup=await inline_kb_menu.admin_tovar_list_markup(category_id=category_id))


@dp.callback_query_handler(IsAdmin(), text_startswith='DeleteCategory_')
async def delete_category(call: types.CallbackQuery):
    category = int(call.data.split('_')[2])
    categoryName = await category_name_by_id(id=category)

    await try_delete_call(call)
    await FSMAdminDelete.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer(f'Вы уверены, что хотите удалить категорию <code>{categoryName}</code>',
                                        reply_markup=keyboard_menu.agreement)
        data["msg_list"] = [msg.message_id]
        data["category"] = category
        data["callback"] = call

    await FSMAdminDelete.category.set()


@dp.message_handler(state=FSMAdminDelete.category)
async def FSMAdminDelete_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == 'да':
            try:
                await delete_category_by_id(id=data["category"])
                await admin_all_categories(call=data["callback"])
            except:
                await message.answer('Что-то пошло не так... ')
                await adminCategory(call=data["callback"])
        else:
            await adminCategory(call=data["callback"])

        msg = await message.answer("Обработка...", reply_markup=None)   # Для удаления клавы
        data["msg_list"].append(message.message_id)
        data["msg_list"].append(msg.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
    await state.finish()


@dp.callback_query_handler(IsAdmin(), text_startswith='AddNewTovar_')
async def AddNewTovar_(call: types.CallbackQuery):
    msg = await call.message.answer('Укажите название товара', reply_markup=keyboard_menu.cancel)

    await try_delete_call(call)
    await FSMAdmin.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        data["msg_list"] = [msg.message_id]
        data["category"] = int(call.data.split('_')[2])
        data["callback"] = call

    await FSMAdmin.product.set()


@dp.message_handler(state=FSMAdmin.product)
async def AddNewTovar_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
        data["msg_list"] = []

        if message.text.lower() == 'отмена':
            await state.finish()
            await adminCategory(call=data["callback"])
        else:
            data["product"] = message.text
            msg = await message.answer("Укажите цену товара", reply_markup=keyboard_menu.cancel)
            data["msg_list"].append(msg.message_id)
            await FSMAdmin.product_price.set()


@dp.message_handler(state=FSMAdmin.product_price)
async def AddNewTovar_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
        data["msg_list"] = []

        if message.text.lower() == 'отмена':
            await state.finish()
            await adminCategory(call=data["callback"])

        elif await digit_check(message.text):
            data["product_price"] = float(message.text.replace(',', '.'))
            msg = await message.answer("Отправьте описание товара", reply_markup=keyboard_menu.cancel)
            data["msg_list"].append(msg.message_id)
            await FSMAdmin.product_desc.set()

        else:
            msg = await message.answer("Укажите цену товара", reply_markup=keyboard_menu.cancel)
            data["msg_list"].append(msg.message_id)
            await FSMAdmin.product_price.set()


@dp.message_handler(state=FSMAdmin.product_desc)
async def AddNewTovar_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
        data["msg_list"] = []

        if message.text.lower() == 'отмена':
            await state.finish()
            await adminCategory(call=data["callback"])

        else:
            data["product_desc"] = message.text
            msg = await message.answer("Отправьте фото(или ссылку на фото)", reply_markup=keyboard_menu.cancel)
            data["msg_list"].append(msg.message_id)
            await FSMAdmin.product_photo.set()


@dp.message_handler(state=FSMAdmin.product_photo, content_types=types.ContentType.ANY)
async def AddNewTovar_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["msg_list"].append(message.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
        data["msg_list"] = []

        if message.photo:
            data["product_photo"] = message.photo[0].file_id
        elif message.text and message.text.lower() != 'отмена':
            data["product_photo"] = message.text
        else:
            await state.finish()
            await adminCategory(call=data["callback"])
            return

        msg_text = await tovar_info_text(title=data["product"], price=data["product_price"],
                                         description=data["product_desc"], iscount=False)
        try:
            msg = await message.answer_photo(photo=data["product_photo"], caption=msg_text)
        except:

            msg = await message.answer(text=msg_text)
        msg2 = await message.answer(text='Всё верно?', reply_markup=keyboard_menu.agreement)
        data["msg_list"].append(msg.message_id)
        data["msg_list"].append(msg2.message_id)
    await FSMAdmin.agreement.set()


@dp.message_handler(state=FSMAdmin.agreement)
async def FSMAdmin_agreement(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        msg = await message.answer("Обработка...", reply_markup=None)   # Для удаления клавы
        data["msg_list"].append(msg.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
        data["msg_list"] = []

        if message.text.lower() == 'да':
            try:
                await add_tovar(category=data["category"], tovar=data["product"], price=data["product_price"],
                                description=data["product_desc"], photo=data["product_photo"])
            except:
                await message.answer('Что-то пошло не так')
    await adminCategory(call=data["callback"])
    await state.finish()


@dp.callback_query_handler(text_startswith='admin-tovar-info_')
async def admin_tovar_info_menu(call: types.CallbackQuery):
    page = int(call.data.split('_')[1])
    category_id = int(call.data.split('_')[2])
    tovar_id = int(call.data.split('_')[3])

    tovar_info = await tovar_info_by_id(id=tovar_id)
    if tovar_info:
        msg_text = await tovar_info_text(title=tovar_info["tovar"], price=tovar_info["price"],
                                         description=tovar_info["description"], iscount=False)
        photo = tovar_info["photo"]
        markup = await inline_kb_menu.admin_tovar_info_markup(category=category_id, page=page, tovar_id=tovar_id)

        try:
            await try_delete_call(call)
            await call.message.answer_photo(photo=photo, caption=msg_text, reply_markup=markup)
        except:
            await try_edit_call(callback=call, text=msg_text, markup=markup)
    else:
        await call.answer('Товар больше не доступен!')


@dp.callback_query_handler(IsAdmin(), text_startswith='DeleteTovarById_')
async def DeleteTovarById(call: types.CallbackQuery):
    product_id = int(call.data.split('_')[3])
    tovarTitle = await product_title_by_id(id=product_id)

    await try_delete_call(call)
    await FSMAdminDelete.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer(f'Вы уверены, что хотите удалить товар <code>{tovarTitle}</code>',
                                        reply_markup=keyboard_menu.agreement)
        data["msg_list"] = [msg.message_id]
        data["product_id"] = product_id
        data["callback"] = call

    await FSMAdminDelete.product.set()


@dp.message_handler(state=FSMAdminDelete.product)
async def FSMAdminDelete_tovar_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() == 'да':
            try:
                await delete_tovar_by_id(id=data["product_id"])
                await adminCategory(call=data["callback"])

            except:
                await message.answer('Что-то пошло не так... ')
                await admin_tovar_info_menu(call=data["callback"])

        else:
            await admin_tovar_info_menu(call=data["callback"])

        msg = await message.answer("Обработка...", reply_markup=None)   # Для удаления клавы
        data["msg_list"].append(message.message_id)
        data["msg_list"].append(msg.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
    await state.finish()


@dp.callback_query_handler(IsAdmin(), text_startswith='EditTovarPhoto_')
async def EditTovarPhoto(call: types.CallbackQuery):
    product_id = int(call.data.split('_')[3])
    tovarTitle = await product_title_by_id(id=product_id)

    await try_delete_call(call)
    await FSMAdminEdit.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer(f'Приложите новое фото(или ссылку на фото) для товара <code>{tovarTitle}</code>',
                                        reply_markup=keyboard_menu.cancel)
        data["msg_list"] = [msg.message_id]
        data["product_id"] = product_id
        data["callback"] = call
    await FSMAdminEdit.product_photo.set()


@dp.message_handler(state=FSMAdminEdit.product_photo, content_types=types.ContentType.ANY)
async def FSMAdminEdit_tovar_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.photo:
            try:
                await edit_tovar_photo(id=data["product_id"], photo=message.photo[0].file_id)
            except:
                await message.answer('Что-то пошло не так... ')
        elif message.text and message.text.lower() != 'отмена':
            try:
                await edit_tovar_photo(id=data["product_id"], photo=message.text)
            except:
                await message.answer('Что-то пошло не так... ')

        msg = await message.answer("Обработка...", reply_markup=None)  # Для удаления клавы
        data["msg_list"].append(message.message_id)
        data["msg_list"].append(msg.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
    await state.finish()
    await admin_tovar_info_menu(call=data["callback"])


@dp.callback_query_handler(IsAdmin(), text_startswith='EditTovarTitle_')
async def EditTovarTitle(call: types.CallbackQuery):
    product_id = int(call.data.split('_')[3])
    tovarTitle = await product_title_by_id(id=product_id)

    await try_delete_call(call)
    await FSMAdminEdit.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer(f'Укажите новое название товара <code>{tovarTitle}</code>',
                                        reply_markup=keyboard_menu.cancel)
        data["msg_list"] = [msg.message_id]
        data["product_id"] = product_id
        data["callback"] = call
    await FSMAdminEdit.product.set()


@dp.message_handler(state=FSMAdminEdit.product)
async def FSMAdminEdit_tovar_title(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() != 'отмена':
            try:
                await edit_tovar_title(id=data["product_id"], title=message.text)
            except:
                await message.answer('Что-то пошло не так... ')

        msg = await message.answer("Обработка...", reply_markup=None)   # Для удаления клавы
        data["msg_list"].append(message.message_id)
        data["msg_list"].append(msg.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
    await state.finish()
    await admin_tovar_info_menu(call=data["callback"])


@dp.callback_query_handler(IsAdmin(), text_startswith='EditTovarPrice_')
async def EditTovarPrice(call: types.CallbackQuery):
    product_id = int(call.data.split('_')[3])
    tovarTitle = await product_title_by_id(id=product_id)

    await try_delete_call(call)
    await FSMAdminEdit.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer(f'Укажите новую цену для товара <code>{tovarTitle}</code>',
                                        reply_markup=keyboard_menu.cancel)
        data["msg_list"] = [msg.message_id]
        data["product_id"] = product_id
        data["callback"] = call
    await FSMAdminEdit.product_price.set()


@dp.message_handler(state=FSMAdminEdit.product_price)
async def FSMAdminEdit_tovar_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if await digit_check(message.text):
            try:
                await edit_tovar_price(id=data["product_id"], price=float(message.text.replace(',', '.')))
            except:
                await message.answer('Что-то пошло не так... ')

        msg = await message.answer("Обработка...", reply_markup=None)  # Для удаления клавы
        data["msg_list"].append(message.message_id)
        data["msg_list"].append(msg.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
    await state.finish()
    await admin_tovar_info_menu(call=data["callback"])


@dp.callback_query_handler(IsAdmin(), text_startswith='EditTovarDesc_')
async def EditTovarDesc(call: types.CallbackQuery):
    product_id = int(call.data.split('_')[3])
    tovarTitle = await product_title_by_id(id=product_id)

    await try_delete_call(call)
    await FSMAdminEdit.msg_list.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        msg = await call.message.answer(f'Укажите новое описание для товара <code>{tovarTitle}</code>',
                                        reply_markup=keyboard_menu.cancel)
        data["msg_list"] = [msg.message_id]
        data["product_id"] = product_id
        data["callback"] = call
    await FSMAdminEdit.product_desc.set()


@dp.message_handler(state=FSMAdminEdit.product_desc)
async def FSMAdminEdit_tovar_desc(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text.lower() != 'отмена':
            try:
                await edit_tovar_description(id=data["product_id"], description=message.text)
            except:
                await message.answer('Что-то пошло не так... ')

        msg = await message.answer("Обработка...", reply_markup=None)  # Для удаления клавы
        data["msg_list"].append(message.message_id)
        data["msg_list"].append(msg.message_id)
        await delete_messages(messages=data["msg_list"], chat_id=message.chat.id)
    await state.finish()
    await admin_tovar_info_menu(call=data["callback"])

