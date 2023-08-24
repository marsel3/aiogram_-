from aiogram import types
from loader import dp, db_users
from keyboards.inline import inline_kb_menu


@dp.message_handler(text=['🗂️ Каталог', 'каталог', "Назад в каталог"])
async def show_catalog(message: types.Message):
    #await message.delete()
    await message.answer(f'Вы перешли в каталог, выберите категорию нужного вам товара.',
                         reply_markup=inline_kb_menu.catalog_markup())


@dp.message_handler(text=['🛍️ Корзина', 'корзина'])
async def show_basket(message: types.Message):
    # await message.delete()
    markup, string = inline_kb_menu.basket_markup(message.from_user.id)
    await message.answer(string, reply_markup=markup)


@dp.message_handler(text=['⭐ Избранное', 'избранное'])
async def show_favourite(message: types.Message):
    await message.answer('Ваш список избранного:',
                         reply_markup=inline_kb_menu.favourite_markup(message.from_user.id))


#@dp.message_handler(text=['📲️Помощь', 'помощь'])
@dp.message_handler(text=['📲️Контакты', 'контакты'])
async def show_contact(message: types.Message):
    # await message.delete()
    await dp.bot.send_location(message.chat.id,
                               latitude=55.78556,
                               longitude=49.12472)
    await message.answer(f'SHOPBOT - удобный телеграмм магазин'
                         f'\n\n📲️ Telegram: @marssak'
                         f'\n\nℹ️г. Казань, метро Площадь Габдуллы Тукая',
                               reply_markup=inline_kb_menu.back_to_menu)
"""    await message.answer(f'Иногда лучшая помощь человеку - это просто не мешать. ☝️',
                         reply_markup=inline_kb_menu.back_to_menu)"""


@dp.message_handler(text=['👤 Профиль', 'профиль'])
async def show_profile(message: types.Message):
    #await message.delete()
    print(message.from_user.id)
    amount = db_users.total_amount(message.from_user.id)
    sale = 0
    await message.answer(f'Профиль\nВаше Имя: {message.from_user.full_name}'
                         f'\n\nВаша статистика'
                         f'\nОбщая сумма покупок: {amount}₽'
                         f'\n\nПроцент скидки: {sale} %',
                         reply_markup=inline_kb_menu.back_to_menu)

