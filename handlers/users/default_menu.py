from aiogram import types
from aiogram.types import CallbackQuery

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
    await message.answer(f'\n— Сколько у нас денег?'
                         f'\n— Три доллара.'
                         f'\n— Блин, Картман, ты ж говорил, у нас куча денег!'
                         f'\n— Да. Но я не учел тот факт, что слаб в математике.',
                         reply_markup=inline_kb_menu.back_to_menu)


@dp.message_handler(text=['⭐ Избранное', 'избранное'])
async def main(message: types.Message):
    # await message.delete()

    await message.answer(f'Я твердо решил забыть о прошлом. Поэтому, если я должен вам денег — мне очень жаль.',
                         reply_markup=inline_kb_menu.back_to_menu)


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

