from aiogram import types
from loader import dp
from keyboards.inline import inline_kb_menu
from utils.db_api.db_asyncpg import *
from aiogram.utils.deep_linking import get_start_link
from handlers.users.inline_menu import send_basket
from handlers.users.commands import start_menu


@dp.message_handler(text=['🗂️ Каталог', 'каталог', "Назад в каталог"])
async def show_catalog(message: types.Message):
    await message.answer(f'Вы перешли в каталог, выберите категорию нужного вам товара.',
                         reply_markup=await inline_kb_menu.categories_markup())


@dp.message_handler(text=['🛍️ Корзина', 'корзина'])
async def show_basket(message: types.Message):
    await send_basket(chat_id=message.chat.id, user_id=message.chat.id)


@dp.message_handler(text=['⭐ Избранное', 'избранное'])
async def show_favourite(message: types.Message):
    await message.answer('Ваш список избранного:',
                         reply_markup=await inline_kb_menu.favourite_markup(message.from_user.id))


@dp.message_handler(text=['📲️Контакты', 'контакты'])
async def show_contact(message: types.Message):
    await dp.bot.send_location(message.chat.id, latitude=55.78556, longitude=49.12472)

    await message.answer(text=f'SHOPBOT - удобный телеграмм магазин\n\n📲️ Telegram: @marssak'
                              f'\n\nℹ️г. Казань, метро Площадь Габдуллы Тукая',
                         reply_markup=inline_kb_menu.back_to_menu)
    """await message.answer(f'Иногда лучшая помощь человеку - это просто не мешать. ☝️',
                         reply_markup=inline_kb_menu.back_to_menu)"""


@dp.message_handler(text=['👤 Профиль', 'профиль'])
async def show_profile(message: types.Message):
    profile = await user_info_by_id(message.from_user.id)

    link = await get_start_link(message.from_user.id)
    await message.answer(f'ℹ️ Профиль\n└ Ваше имя: {profile["fio"]}'
                         f'\n\n🤝 Партнёрская программа:'
                         f'\n├  Бонусный счёт: <code>{profile["bonus"]}₽</code>'
                         f'\n└  Лично приглашенных: <code>{profile["referral_count"]}</code>'
                         f'\n\n⤵️Ваша персональная ссылка: '
                         f'\n└ <code>{link}</code>',
                         reply_markup=inline_kb_menu.back_to_menu,
                         parse_mode='HTML')


@dp.message_handler()
async def main(message: types.Message):
    await start_menu(message)