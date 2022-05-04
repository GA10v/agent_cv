from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils import config


storage = MemoryStorage() # позволяет хранить данные в оперативной памяти

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)