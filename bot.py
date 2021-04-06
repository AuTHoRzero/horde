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
import schedule
import time

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
cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER, group_number TEXT)')
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
    await message.answer('В данном меню вы можете настроить ежедневные уведомления о парах на сегодняшний день', 
    reply_markup=keyboard.button_notify,
    )


@dp.message_handler(text=['Установить время, когда приходят уведомления'])
async def time_quest (message: types.Message):
    await message.answer('Установите время в формате: 0:00')
    schedule.every().day.at("20:48").do(schedule_today)


@dp.message_handler(text=['Включение/Выключение уведомлений'])
async def time_set (message: types.Message):
   await States.on_off.set()
   await message.answer('Состояние успешно изменено, текущее состояние:\n')


#@dp.message_handler(state=States.on_off)
#async def on_off_change (message: types.Message):
#    await message.answer('Hi')


@dp.message_handler(text=['Получить расписание'])
async def schedule_menu(message: types.Message):
    await message.answer('Выберите на какой день получить расписание', 
    reply_markup=keyboard.button_schedule_choise,
    )


@dp.message_handler(text=['Расписание на сегодня'])
async def schedule_today(message: types.Message):
    await message.answer(f'День недели: {days_naming[today_day]}')
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
        for i in range(len(schedule)):
            lesson_json = schedule[str(i+1)][0]
            lesson = lesson_json['lesson']
            teacher = lesson_json['teacher']
            classroom = lesson_json['classroom']
            period = f'Пара {i+1}:\n {lesson}, {teacher}, {classroom}\n'
            reply_message = f'{period}'
            await bot.send_message(message.from_user.id, reply_message)


@dp.message_handler(text=['Расписание на завтра'])
async def schedule_next_day(message: types.Message):
    await message.answer(f'День недели: {days_naming[today_day]}')
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
        for i in range(len(schedule)):
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
    await message.answer('ТУТ НИЧЕГО НЕТ, ПОМОЩИ ТОЖЕ НЕТ.', reply_markup = keyboard.btn_back)


if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)
    
