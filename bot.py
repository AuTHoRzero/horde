#libraries
import sqlite3
import logging
from aiogram.dispatcher.filters import Text
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from config import bot_token
from aiogram.utils.helper import Helper, HelperMode, ListItem
import keyboard as keyboard
import datetime
import calendar
from datetime import date
#Bot object
bot= Bot(token=bot_token)
#Bot dispetcher
dp = Dispatcher(bot)
#Buttons
#datetime
today = date.today()
calendar.day_name[today.weekday()]
#users database
conn = sqlite3.connect('users_database.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER)')
#Function
@dp.message_handler(commands='start')
async def start(message : types.Message):
    await message.answer('Добро пожаловать в petroshedulebot, мои создатели: \nАверин Андрей\nПрохоров Евгений\nБерозко Роман\n\nCтуденты группы 39-55', reply_markup=keyboard.button_who)
    await message.answer(today)
    try:
        conn = sqlite3.connect('users_database.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}")')
        conn.commit()
    except Exception as e:
        print(e)
        conn = sqlite3.connect('users_database.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}")')
        conn.commit()
@dp.message_handler(commands=['profile'])
async def get_profile(msg: types.Message):
    conn = sqlite3.connect('users_database.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM users WHERE user_id = "{msg.from_user.id}"')
    result = cur.fetchall()
    await bot.send_message(msg.from_user.id, f'ID = {list(result[0])[0]}')
if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)
    
