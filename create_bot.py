from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import token
from aiogram import Bot




storage = MemoryStorage()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)