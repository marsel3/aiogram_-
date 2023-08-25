from aiogram import types
from loader import dp
from keyboards.inline import inline_kb_menu
from utils.db_api.db_asyncpg import *


@dp.message_handler(text=['🗂️ Каталог', 'каталог', "Назад в каталог"])
async def show_catalog(message: types.Message):
    #await message.delete()
    await message.answer(f'Вы перешли в каталог, выберите категорию нужного вам товара.',
                         reply_markup=await inline_kb_menu.categories_markup())


@dp.message_handler(text=['🛍️ Корзина', 'корзина'])
async def show_basket(message: types.Message):
    # await message.delete()
    await send_basket(chat_id=message.chat.id, user_id=message.chat.id)


async def send_basket(chat_id, user_id):
    basket = await basket_list(user_id)
    markup = await inline_kb_menu.basket_markup(basket)

    string = f'<b>Корзина.</b>'
    summ = 0
    count = 1
    if len(basket) > 0:
        for tovar in basket:
            string += f'\n\n{count}. «{tovar["name"]}» ' \
                      f'\n\t\t\tЦена: {tovar["price"]} × {tovar["count"]}  =  {tovar["price"] * tovar["count"]} рублей'
            summ += tovar["price"] * tovar["count"]
            count += 1
        string += '\n__________________' + '_' * len(str(summ))
    string += f'\nИтого: {summ} рублей'

    await dp.bot.send_message(chat_id=chat_id, text=string, reply_markup=markup, parse_mode="HTML")


@dp.message_handler(text=['⭐ Избранное', 'избранное'])
async def show_favourite(message: types.Message):
    await message.answer('Ваш список избранного:',
                         reply_markup=await inline_kb_menu.favourite_markup(message.from_user.id))


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
    """await message.answer(f'Иногда лучшая помощь человеку - это просто не мешать. ☝️',
                         reply_markup=inline_kb_menu.back_to_menu)"""


@dp.message_handler(text=['👤 Профиль', 'профиль'])
async def show_profile(message: types.Message):
    # await message.delete()
    await message.answer(f'Профиль\nВаше Имя: {message.from_user.full_name}'
                         f'\n\nВаша статистика'
                         f'\nОбщая сумма покупок: {0}₽'
                         f'\n\nПроцент скидки: {0} %',
                         reply_markup=inline_kb_menu.back_to_menu)

