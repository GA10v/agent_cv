from aiogram import types
from aiogram import Dispatcher

from db import db_set_like
from db import db_get_vacancy
from db import db_join_user
from db import db_get_like

from utils.create_bot import bot
from utils import send_email

from keyboards import c_kb



async def client_start(message : types.Message):
    ''''''

    try:
        await bot.send_message(message.from_user.id, f'Привет, {message.from_user.full_name}! Я бот по поиску вакансий на сайте hh.ru.\n\n\
\\Run - выдает очередную вакансию;\n\
\\Like - сохраняет вакансию в список избранных;\n\
\\Send - отправит избраные вакансии тебе на почту.\n\n\
                Начнем поиск работы!', reply_markup=c_kb)
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


async def send(message : types.Message):
    await message.delete()
    await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, напиши свой email\n и я отправлю тебе ваансии ',reply_markup=c_kb)


async def send_mail(message : types.Message):
    await message.delete()
    msg = db_get_like(message)
    email = message.text
    send_email(email, msg)
    await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, проверяй почту! ',reply_markup=c_kb)
    

def register_message_handler_client(dp : Dispatcher):
    '''
    функция для регистрации handlers\n
    вместо декоратора "@dp.message_handler(commands=[commands])" 
    '''

    dp.register_message_handler(client_start, commands=['Start', 'Help', 'End'])
    dp.register_message_handler(get_vacancies, commands=['Run'])
    dp.register_message_handler(set_like, commands=['like'])
    dp.register_message_handler(send, commands=['send'])
    dp.register_message_handler(send_mail, lambda message: '@' in message.text)


