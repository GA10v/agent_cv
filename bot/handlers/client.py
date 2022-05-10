from aiogram import types
from aiogram import Dispatcher
from db import db_set_like
from db import db_get_vacancy
from utils.create_bot import bot
from db import db_join_user
from keyboards import c_kb


async def client_start(message : types.Message):
    ''''''

    try:
        await bot.send_message(message.from_user.id, f'Привет, {message.from_user.full_name}! Начнем поиск работы!', reply_markup=c_kb)
        await message.delete()
    except:
        await message.reply('Напишите боту в ЛС:\nhttps://t.me/HH_parser_for_CVbot')
    
    try:
       db_join_user(message)
       
    except Exception as e:
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, что-то пошло не так! {e}')
        raise e


async def get_vacancies(message : types.Message):
    ''''''

    await message.delete()
    await db_get_vacancy(message)

async def set_like(message : types.Message):
    ''''''

    await message.delete()
    await db_set_like(message)


def register_message_handler_client(dp : Dispatcher):
    '''
    функция для регистрации handlers\n
    вместо декоратора "@dp.message_handler(commands=[commands])" 
    '''

    dp.register_message_handler(client_start, commands=['Start', 'Help', 'End'])
    dp.register_message_handler(get_vacancies, commands=['Run'])
    dp.register_message_handler(set_like, commands=['like'])

