from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.db_sqlite import DataBase
from data import config


bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

db_shop = DataBase('db/data_base')

dp = Dispatcher(bot, storage=MemoryStorage())