from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import *
from bin.database import DataBase

storage = MemoryStorage()
bot = Bot(token = token)
dp = Dispatcher(bot, storage = storage)
db = DataBase(user, password, host, database)
pm = types.ParseMode.HTML