from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from db.base1 import sql_start1

from handlers import admin, client
from utils import start_parsing

from utils.create_bot import bot, dp


async def on_startup(_):
    '''
    параметры запуска бота
    '''

    print('[+] Bot is running!')
    await start_parsing()
    print('[+] Bot online!')
    sql_start1()


if __name__ == '__main__':

    client.register_message_handler_client(dp)
    admin.register_handler_admin(dp)

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

