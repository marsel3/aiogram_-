from aiogram import types
from aiogram.types import CallbackQuery
from states import State
from loader import dp, db_tovars, db_users
from keyboards.inline import inline_kb_menu


@dp.message_handler(text=['🗂️ Каталог', 'каталог', "Назад в каталог"])
async def main(message: types.Message):
    #await message.delete()
    await message.answer(f'Вы перешли в каталог, выберите категорию нужного вам товара.',
                         reply_markup=inline_kb_menu.catalog_markup())

@dp.message_handler(text=['🛍️ Корзина', 'корзина'])
async def main(message: types.Message):
    # await message.delete()
    markup, string = inline_kb_menu.basket_markup(message.from_user.id)
    await message.answer(string, reply_markup=markup)


@dp.message_handler(text=['⭐ Избранное', 'избранное'])
async def main(message: types.Message):
    await message.answer('Ваш список избранного:',
                         reply_markup=inline_kb_menu.favourite_markup(message.from_user.id))


@dp.message_handler(text=['📲️Помощь', 'помощь'])
async def main(message: types.Message):
    #await message.delete()
    await message.answer(f'Иногда лучшая помощь человеку - это просто не мешать. ☝️',
                         reply_markup=inline_kb_menu.back_to_menu)


@dp.message_handler(text=['👤 Профиль', 'профиль'])
async def main(message: types.Message):
    #await message.delete()
    await message.answer(f'𝐍𝐨𝐰 𝐥𝐨𝐚𝐝𝐢𝐧𝐠. . .',
                         reply_markup=inline_kb_menu.back_to_menu)

