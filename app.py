from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
import asyncpg
from handlers import dp
import asyncio
from aiogram import executor


async def on_startup(dp):
    await on_startup_notify(dp)  # Уведомление админов о старте бота
    await set_default_commands(dp)  # Установка команд бота
    await create_db_pool(dp)  # Создание пула базы данных


async def create_db_pool(dp):
    dp['db_pool'] = await asyncpg.create_pool(
        user='mars',
        password='mars',
        host='45.130.42.176',
        database='shop',
        max_size=100,
    )


async def close_db_pool(dp):
    await dp['db_pool'].close()


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()
    await close_db_pool(dp)  # Закрытие пула базы данных


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db_pool(dp))
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
    loop.run_forever()