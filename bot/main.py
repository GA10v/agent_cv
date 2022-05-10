from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from utils.config import NAME
from db import db_start

from handlers import admin, client
from utils import get_today
from utils import dp


async def on_startup(_):
    '''
    параметры запуска бота
    '''

    print('[+] Bot is running!')
    await get_today(NAME)
    db_start()
    print('[+] Bot online!')


if __name__ == '__main__':

    client.register_message_handler_client(dp)
    admin.register_handler_admin(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

