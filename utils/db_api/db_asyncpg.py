"""import asyncio
import asyncpg
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def categories_markup():
    conn = await asyncpg.connect(user='postgres', password='1969',
                                 database='shop_db')
    values = await conn.fetch(
        'SELECT * FROM categories'
    )
    markup = InlineKeyboardMarkup()
    for i in values:
        await markup.add(InlineKeyboardButton(text=f'{i["category_name"]}', callback_data=f'{i["category_id"]}'))

    await conn.close()

    return markup


"""