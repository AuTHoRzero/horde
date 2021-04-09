#libraries
import sqlite3
import logging
import aiogram.utils.markdown as md
import keyboard as keyboard
import datetime
import calendar
import lxml
import requests
import json
import time
import random
import asyncio
import aioschedule

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.helper import Helper, HelperMode, ListItem
from config import bot_token, api_key
from datetime import date
from bs4 import BeautifulSoup
from markdown import markdown
#Logging
logging.basicConfig(level=logging.INFO)
#States
class States(StatesGroup):
    group = State()
    on_off = State()
    main = State()
    setting = State()
    profile = State()
#Bot object
bot= Bot(token=bot_token)
#Bot dispetcher
dp = Dispatcher(bot, storage=MemoryStorage())
#Weekday and date
today_day = datetime.datetime.today().weekday()
days_naming = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
days_naming_en = ["monday", "tuesday", "wednesday", "thursday", "friday","saturday", "sunday"]
today = date.today()
calendar.day_name[today.weekday()]
next_day = today_day + 1
#users database
conn = sqlite3.connect('users_database.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER, group_number TEXT, notify_times TEXT)')
#Function
@dp.message_handler(commands='start')
async def start(message : types.Message):
    await message.answer(
        'Добро пожаловать в petroshedulebot, мои создатели:\nАверин Андрей\nПрохоров Евгений\nБерозко Роман\n\nCтуденты группы 39-55',
        reply_markup=keyboard.button_register
        )
    await message.answer(f'Сегодня: {today}\n{days_naming[today_day]}')
    print (next_day)


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
        await bot.send_message(message.chat.id, 
        md.text(md.text('Ваша группа:', 
        md.bold(data['group']))), 
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup= keyboard.button_go_main
        )
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

@dp.message_handler(text=['Настройки'])
async def setting(message: types.Message):
    await message.answer('Добро пожаловать в меню настроек', 
    reply_markup=keyboard.button_notify,
    )


@dp.message_handler(text=['Сменить группу'])
async def rewrite (message: types.Message):
    con = sqlite3.connect('users_database.db')
    cur = con.cursor()
    cur.execute(f'DELETE from users WHERE user_id = "{message.from_user.id}"')
    con.commit()
    cur.close()
    await message.answer('Готово')
    await States.group.set()
    await message.answer('Введите новый номер группы')
    


@dp.message_handler(text=['Время уведомлений'])
async def time_quest (message: types.Message):
    await message.answer('Функция в разработке')
    await States.setting.set()



@dp.message_handler(text=['Вкл/Выкл уведомлений'])
async def time_set (message: types.Message):
   await States.on_off.set()
   await message.answer('Состояние успешно изменено, текущее состояние:\n')


@dp.message_handler(state=States.setting)
async def times_setting_set (message: types.Message, state = FSMContext):
    async with state.proxy() as times:
        times['times_set'] = message.text
        await bot.send_message(message.chat.id, 
        md.text(md.text('Установленное время:', 
        md.bold(times['times_set']))), 
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup= keyboard.button_go_main
        )
        timers = md.text(md.text(md.bold(times['times_set'])))
        rework = markdown(timers)
        setted_time = ''.join(BeautifulSoup(rework).findAll(text=True))
        connect = sqlite3.connect('users_database.db')
        cur = connect.cursor()
        cur.execute(f'INSERT INTO users VALUES WHERE user_id = "{message.from_user.id}"("{setted_time}")')
        connect.commit()
        cut.close()


@dp.message_handler(text=['Получить расписание'])
async def schedule_menu(message: types.Message):
    await message.answer('Выберите на какой день получить расписание', 
    reply_markup=keyboard.button_schedule_choise,
    )


@dp.message_handler(text=['Расписание на сегодня'])
async def schedule_today(message: types.Message):
    await message.answer(f'Сегодня: {days_naming[today_day]}')
    con = sqlite3.connect('users_database.db')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM users WHERE user_id = "{message.from_user.id}"')
    res = cur.fetchall()
    response = requests.get(f'https://petrocol.ru/schedule/{[list(res[0])[1]][0]}?json=1&key={api_key}')
    all_schedule = json.loads(response.text)
    try:
        schedule = all_schedule["schedule"][days_naming_en[today_day]]
    except:
        await message.answer('Нет данных о парах на сегодня, попробуйте посмотреть на сайте:\nhttps://portal.petrocollege.ru/Pages/responsiveSh-aspx.aspx')
    else:
        for i in range(len(schedule)+1):
            try:
                lesson_json = schedule[str(i+1)][0]
                lesson = lesson_json['lesson']
                teacher = lesson_json['teacher']
                classroom = lesson_json['classroom']
                period = f'Пара {i+1}:\n {lesson}, {teacher}, {classroom}\n'
                reply_message = f'{period}'
                await bot.send_message(message.from_user.id, reply_message)
            except:
                pass



@dp.message_handler(text=['Расписание на завтра'])
async def schedule_next_day(message: types.Message):
    await message.answer(f'Завтра: {days_naming[next_day]}')
    con = sqlite3.connect('users_database.db')
    cur = con.cursor()
    cur.execute(f'SELECT * FROM users WHERE user_id = "{message.from_user.id}"')
    res = cur.fetchall()
    response = requests.get(f'https://petrocol.ru/schedule/{[list(res[0])[1]][0]}?json=1&key={api_key}')
    all_schedule = json.loads(response.text)
    try:
        schedule = all_schedule["schedule"][days_naming_en[next_day]]
    except:
        await message.answer('Нет данных о парах на завтра, попробуйте посмотреть на сайте:\nhttps://portal.petrocollege.ru/Pages/responsiveSh-aspx.aspx')
    else:
        for i in range(len(schedule)+1):
            try:
                global reply_message_1
                lesson_json = schedule[str(i+1)][0]
                lesson = lesson_json['lesson']
                teacher = lesson_json['teacher']
                classroom = lesson_json['classroom']
                period = f'Пара {i+1}:\n {lesson}, {teacher}, {classroom}\n'
                reply_message_1 = f'{period}'
                await bot.send_message(message.from_user.id, reply_message_1)
            except:
                pass
#                await message.answer('Нет данных о парах на завтра, попробуйте посмотреть на сайте:\nhttps://portal.petrocollege.ru/Pages/responsiveSh-aspx.aspx')
#        await bot.send_message(message.from_user.id, reply_message_1)       


@dp.message_handler(text=['Перейти в главное меню', 'Вернутся в главное меню', 'Назад'])
async def main_menu (message: types.Message):
    await bot.send_message(message.from_user.id, 
        'Добро пожаловать в главное меню, здесь вы можете настроить автоматическое получение получение расписания или получить его вручную', 
        reply_markup=keyboard.button_main,
        )


@dp.message_handler(text=['Мой профиль'])
async def get_profile(message: types.Message):
    conn = sqlite3.connect('users_database.db')
    cur = conn.cursor()
    cur.execute(f'SELECT * FROM users WHERE user_id = "{message.from_user.id}"')
    result = cur.fetchall()
    await bot.send_message(message.from_user.id, f'ID = {list(result[0])[0]}\nGroup = {[list(result[0])[1]][0]}', reply_markup=keyboard.btn_back)


@dp.message_handler(text=['Помощь'])
async def user_help (message: types.Message):
    photo = ['https://sun9-45.userapi.com/impg/L_ZjDqZoxr0-Ps0fQi0-c48PjJ-UWJk64exZqw/HrcqjPtfIjE.jpg?size=840x737&quality=96&sign=e78ad3ba428e817729e80c0f02d249df&type=album', 
    'https://sun9-30.userapi.com/impg/S-bSLtCaDlC1bcUwMCDlCAyzerrNVqFgw5Ygpg/BoLXpwQ1HcY.jpg?size=608x770&quality=96&sign=e101f67bcaa95f1aec2d52a651d24cef&type=album', 
    'https://sun9-64.userapi.com/impg/v9TI88OR_8UV_CJ2u2FRJlSjFiRhpoh_lFKSFg/jPCHxw5V4WQ.jpg?size=1125x1077&quality=96&sign=b62f3c74fd48e7831d66add4eb792715&type=album',
    ]
    await message.answer('Не готово...', reply_markup = keyboard.btn_back)
    await bot.send_photo(message.from_user.id, photo[random.randint(0,2)])


if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True,)
    
