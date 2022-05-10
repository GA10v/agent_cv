# from aiogram.dispatcher import FSMContext # для передачи в handler аннотацию типа
# from aiogram.dispatcher.filters.state import State, StatesGroup 
# from aiogram import Dispatcher, types
# from db import sql_update
# from utils.create_bot import bot
# from utils import start_parsing
# from db import sql_update
# from keyboards import a_kb
# import asyncio


# ID = None

# class FSMAdmin(StatesGroup):
#     '''класс состояний бота при работе в машине-состояния'''
#     parsing = State() # Запуск парсинга
#     update = State() # Запуск обновления БД

# # начало диалога парсинга сайтов вакансий
# @dp.message_handler(Commands='Парсить', state=None)
# async def cm_start(message : types.Message):
#     await FSMAdmin.parsing.set()
#     await message.reply('Начинаю поиск вакансий')

# async def admin_start(message : types.Message):
#     ''''''

#     global ID
#     ID = message.from_user.id

#     try:
#         await bot.send_message(message.from_user.id, f'{message.from_user.first_name}! ты в админке', reply_markup=a_kb)
#         await message.delete()
#     except:
#         await message.reply('error')


# async def get_parsed(message : types.Message):
#     '''
#     админ функция бота, запускает парсинг
#     '''

#     if message.from_user.id == ID: # проверка на право администратора
#         try:
#             await message.delete()
#             await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, приступаю, свистну когда закончу')
#             await start_parsing()
#             await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, закончил',reply_markup=a_kb)
#         except Exception as e:
#             await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, что-то пошло не так! {e}', reply_markup=a_kb)


# async def get_update(message : types.Message):
#     '''
#     админ функция бота, обновляет БД
#     '''

#     if message.from_user.id == ID:
#         try:
#             await message.delete()
#             await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, обновляю БД, свистну когда закончу', reply_markup=a_kb)
#             await sql_update()
#         except Exception as e:
#             await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, что-то пошло не так! {e}', reply_markup=a_kb)
#         finally:
#             await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, я закончил',reply_markup=a_kb)


# def register_handler_admin(dp : Dispatcher):
#     '''
#     функция для регистрации handlers\n
#     вместо декоратора "@dp.message_handler(commands=[commands])" 
#     '''

#     dp.register_message_handler(get_parsed, commands=['get_parced'])
#     dp.register_message_handler(get_update, commands=['update'])
#     dp.register_message_handler(admin_start, commands=['admin'], is_chat_admin=True) # последний аргумент проверяет права администратора в общем чате
