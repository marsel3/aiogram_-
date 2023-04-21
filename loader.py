from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.db_sqlite import User, DataBase
from utils.db_api.db_adminka import DataBase
from data import config


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

db_users = User('db/users.db')
#db_tovars = DataBase('db/tovars.db')
db_tovars = DataBase('adminka/db.sqlite3')

dp = Dispatcher(bot, storage=MemoryStorage())