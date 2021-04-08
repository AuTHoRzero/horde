#libraries
import sqlite3
import logging
import aiogram.utils.markdown as md
import keyboard as keyboard
import datetime
import calendar
import lxml
import aioschedule
import asyncio

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.helper import Helper, HelperMode, ListItem
from config import bot_token
from datetime import date
from bs4 import BeautifulSoup
from markdown import markdown
#States
class States(StatesGroup):
    group = State()
#Bot object
bot= Bot(token=bot_token)
#Bot dispetcher
dp = Dispatcher(bot, storage=MemoryStorage())
#Buttons
#Weekday and date
today_day = datetime.datetime.today().weekday()
days_naming = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
today = date.today()
calendar.day_name[today.weekday()]
#users database
conn = sqlite3.connect('users_database.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER, group_number TEXT)')
#Function
@dp.message_handler(commands='start')
async def start(message : types.Message):
    await message.answer(
        'Добро пожаловать в petroshedulebot, мои создатели:\nАверин Андрей\nПрохоров Евгений\nБерозко Роман\n\nCтуденты группы 39-55',
        reply_markup=keyboard.button_register
        )
    await message.answer(f'Сегодня: {today}\n{days_naming[today_day]}')


@dp.message_handler(text=['Регистрация'])
async def register(message: types.Message):
    await bot.send_message(message.from_user.id,'Кто ты?', reply_markup=keyboard.button_who)


@dp.message_handler(text=['Я студент'])
async def student_register(message: types.Message):
    await States.group.set()
    await bot.send_message(message.from_user.id, 'Напиши номер своей группы')


@dp.message_handler(state=States.group)
async def group_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        global group
        data['group'] = message.text
        await bot.send_message(message.chat.id, md.text(md.text('Сышишь, другалёк, ты в группе', md.bold(data['group']))), parse_mode=ParseMode.MARKDOWN_V2)
        grouper = md.text(md.text(md.bold(data['group'])))
        data = markdown(grouper)
        group = ''.join(BeautifulSoup(data).findAll(text=True))
        print(group)
        conn = sqlite3.connect('users_database.db')
        cur = conn.cursor()
        cur.execute(f'INSERT INTO users VALUES("{message.from_user.id}","{group}")')
        conn.commit()

    await state.finish()


@dp.message_handler(text=['Я преподаватель'])
async def teacher_register(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        'Данная функция находится в разработке, пожалуйста попробуйте позднее',
        )


@dp.message_handler(commands=['profile'])
async def get_profile(message: types.Message):
    conn = sqlite3.connect('users_database.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM users WHERE user_id = "{message.from_user.id}"')
    result = cur.fetchall()
    await bot.send_message(message.from_user.id, f'ID = {list(result[0])[0]}\nGroup = {[list(result[0])[1]][0]}')


if __name__=='__main__':
    executor.start_polling(dp, skip_updates=False)
    
