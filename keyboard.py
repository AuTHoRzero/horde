from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
    
student_button = KeyboardButton('Я студент')
teacher_button = KeyboardButton('Я преподаватель')
button_who = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(student_button).add(teacher_button)
register_button = KeyboardButton('Регистрация')
button_register = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(register_button)
