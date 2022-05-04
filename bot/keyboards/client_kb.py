from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


b1 = KeyboardButton('/Run')
b2 = KeyboardButton('/Start')

c_kb = ReplyKeyboardMarkup(resize_keyboard=True)

c_kb.add(b1).add(b2)
