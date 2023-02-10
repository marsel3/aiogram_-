from filters import IsAdmin
from aiogram import types

from loader import dp, db_tovars
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from states.state import FSMAdmin
from utils.db_api import db_admin


@dp.message_handler(IsAdmin(), text='/admin')
async def admin(messsage: types.Message):
    await messsage.answer(f'Здравствуйте, {messsage.from_user.full_name},  вы попали в админ панель!',
                          reply_markup=db_admin.admin_panel)


@dp.callback_query_handler(text='admin_category')
async def admin_catalog(call: CallbackQuery):
    await call.message.edit_text('Вы в меню редактора категории', reply_markup=db_admin.admin_catalog_markup())


@dp.callback_query_handler(text="add_new_category")
async def show_catalog(call: CallbackQuery):
    await call.message.answer('Введите название категории')
    await FSMAdmin.category_id.set()


@dp.message_handler(state=FSMAdmin.category_id)
async def state2(message: types.Message):
    text = message.text
    try:
        db_tovars.category_add(text)
        await message.answer(f'Категория "{text}" создана!', reply_markup=db_admin.admin_catalog_markup())
    except:
        await message.answer(f'Что-то пошло не так! возможно такая категория уже есть...')


@dp.callback_query_handler(text_startswith='admin_category_')
async def admin_category_(call: CallbackQuery):
    category_id = call.data[15:]
    await call.message.answer(f'Вы в категории {db_tovars.category_name(category_id)}',
                              reply_markup=db_admin.admin_tovars_markup(category_id))


@dp.callback_query_handler(text_startswith="admin_tovar_")  #допилить
async def show_catalog(call: CallbackQuery):
    tovar_id = call.data[12:]

    text, photo = db_admin.admin_card(tovar_id)
    markup = db_admin.set_tovar_card(tovar_id)
    if photo != 'None':
        await dp.bot.send_photo(chat_id=call.message.chat.id, caption=text,
                                photo=photo, reply_markup=markup)
    else:
        await call.message.answer(text, reply_markup=markup)


@dp.callback_query_handler(text_startswith='edit_category_')
async def edit_category_(call: CallbackQuery):
    category_id = call.data[14:]
    await call.message.answer(f'пока не работает')


@dp.callback_query_handler(text_startswith='delete_category_')
async def delete_category_(call: CallbackQuery):
    category_id = call.data[16:]
    category_name = db_tovars.category_name(category_id)
    db_tovars.category_delete(category_id)
    await call.message.answer(f'Вы удалили категорию "{category_name}"',
                              reply_markup=db_admin.admin_catalog_markup())


@dp.callback_query_handler(text_startswith='add_new_tovar_')
async def add_new_tovar(call: CallbackQuery):
    category_id = call.data[14:]

    await FSMAdmin.category_id.set()
    state = dp.get_current().current_state()
    async with state.proxy() as data:
        data["category_id"] = category_id

    await call.message.answer('Введите название товара')
    await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.tovar_name)
async def state2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tovar_name'] = message.text
    await FSMAdmin.next()
    await message.answer(f'Введите цену товара "{message.text}":')


@dp.message_handler(state=FSMAdmin.tovar_price)
async def state3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tovar_price'] = message.text
        await message.answer(f'Напишите описание товара "{data["tovar_name"]}":')
    await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.tovar_disc)
async def state2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tovar_disc'] = message.text
        await message.answer(f'Теперь кидай фото товара "{data["tovar_name"]}":',
                             reply_markup=db_admin.without_photo)
    await FSMAdmin.next()


@dp.message_handler(content_types=['photo'], state=FSMAdmin.tovar_photo)
async def state2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tovar_photo'] = message.photo[0].file_id

    async with state.proxy() as data:
        await message.answer_photo(caption=f'{data["tovar_name"]}: \t{data["tovar_price"]} руб. \n\n{data["tovar_disc"]}',
                                   photo=data["tovar_photo"])
    await message.answer(f'Всё верно?', reply_markup=db_admin.agreement)

    await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.tovar_photo)
async def state2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tovar_photo'] = 'None'

    async with state.proxy() as data:
        await message.answer(text=f'{data["tovar_name"]}: \t{data["tovar_price"]} руб. \n\n{data["tovar_disc"]}')

    await message.answer(f'Всё верно?', reply_markup=db_admin.agreement)
    await FSMAdmin.next()


@dp.message_handler(state=FSMAdmin.agreement)
async def state2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        category = data["category_id"]
    if message.text == 'Да':
        async with state.proxy() as data:
            db_tovars.tovar_add(data["category_id"], data['tovar_name'], data['tovar_price'], data['tovar_disc'], data['tovar_photo'])
        await message.answer('Товар добавлен в базу!',
                             reply_markup=db_admin.admin_main)
    else:
        await message.answer('Товар не был добавлен',
                             reply_markup=db_admin.admin_main)

    await message.answer(text=f'Вы в категории "{db_tovars.category_name(category)}"',
                         reply_markup=db_admin.admin_tovars_markup(category))
    await state.finish()
