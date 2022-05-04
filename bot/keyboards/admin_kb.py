from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b3 = KeyboardButton('/Get_parced')
b4 = KeyboardButton('/Update')
b5 = KeyboardButton('/End')

a_kb = ReplyKeyboardMarkup(resize_keyboard=True)

a_kb.add(b3).add(b4).add(b5)