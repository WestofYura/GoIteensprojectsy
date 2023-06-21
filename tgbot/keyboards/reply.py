from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = [
    KeyboardButton('/convert'),
    KeyboardButton('/help'),
    KeyboardButton('/start')
]
keyboard.add(*buttons)