##############
##Библиотеки##
##############
import sqlite3
import logging
import aiogram.utils.markdown as md
import keyboard as keyboard
import datetime
import calendar
import lxml
import json
import time
import random
import asyncio
import aioschedule
import pandas as pd
import schedule
import subprocess
import emoji
import os

from aiogram.types import InputFile
from aiogram import Bot, types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode, Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.helper import Helper, HelperMode, ListItem
from config import bot_token, admin_id, admin2_id
from datetime import date, timedelta
from bs4 import BeautifulSoup
from markdown import markdown
from pprint import pprint

##############
##Переменные##
##############
global key, chisl, x, y, cikl

chisl = ''
x = 0
y = 0
cikl = 0
key = 0

###############
##Логирование##
###############
logging.basicConfig(level=logging.INFO)

#############
##Состояния##
#############
class States(StatesGroup):
    group = State()
    setting = State()
    adm1 = State()
    adm1_set = State()
    sndmsg = State()
    fio = State()

###############
##Объект бота##
###############
bot = Bot(token=bot_token)

############################
##Диспетчер(Для хэндлеров)##
############################
dp = Dispatcher(bot, storage=MemoryStorage())

############################
##Даты и имена дней недели##
############################
today_week = datetime.datetime.today().isocalendar()[1]
today_day = datetime.datetime.today().weekday()
days_naming = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота","Воскресенье"]
days_naming_en = ["monday", "tuesday", "wednesday", "thursday", "friday","saturday", "sunday"]
today = date.today()
calendar.day_name[today.weekday()]
next_day = today_day + 1
if next_day == 7:
    next_day = 0

###################################################
##Парсинг уведомления с главной страницы колледжа##
###################################################
async def started():
    global message_for_see
    try:
        with open (f'/home/{os.getlogin()}/horde/info_{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.html') as file:
            src1 = file.read()

        soup1 = BeautifulSoup(src1, "lxml")

        all_p = soup1.find("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p")
        all_p1 = soup1.find("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p")
        all_p2_1 = soup1.find("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p")
        all_p2_2 = soup1.find("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p")
        all_p2 = soup1.find("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p")
        all_p2_3 = soup1.find("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p")
        all_p3 = soup1.find("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p")
        all_p4 = soup1.find("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p").find_next("p")
        message_for_see = f"{all_p.get_text()}\n{all_p1.get_text()}\n{all_p2_1.get_text()}\n{all_p2_2.get_text()}\n\n{all_p2_3.get_text()}\n{all_p3.get_text()}\n{all_p2.get_text()}\n{all_p4.get_text()}"
    except Exception:
        print('None')

#############################
##База данных пользователей##
#############################
conn = sqlite3.connect('users_database.db')
cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER, group_number TEXT, notify_times TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS prepods(user_id INTEGER, prep_name TEXT, notify_times TEXT)')

#############################
##База данных пользователей##
#############################
dbfile = InputFile("users_database.db", filename="users_database.db")

################
##Текущий день##
################
async def week():
    global key
    global cikl
    global cikl1
    global key1
    if (today_week % 2 == 0):
        chisl = 'Числитель'
    else:
        chisl = 'Знаменатель'
    if (chisl == 'Знаменатель' and today_day==0):
        cikl = 0
        cikl1 = 6
    elif (chisl == 'Знаменатель' and today_day==1):
        cikl = 6
        cikl1 = 12
    elif (chisl == 'Знаменатель' and today_day==2):  
        cikl = 12  
        cikl1 = 18
    elif (chisl == 'Знаменатель' and today_day==3):
        cikl = 18
        cikl1 = 24
    elif (chisl == 'Знаменатель' and today_day==4):
        cikl = 24
        cikl1 = 30
    elif (chisl == 'Знаменатель' and today_day==5):
        cikl = 30
        cikl1 = 100
    elif (chisl == 'Знаменатель' and today_day==6):   
        cikl = 100
        cikl1 = 36
    elif (chisl == 'Числитель' and today_day == 0):
        cikl = 36
        cikl1 =42
    elif (chisl == 'Числитель' and today_day==1):
        cikl = 42
        cikl1 = 48
    elif (chisl == 'Числитель' and today_day==2):  
        cikl = 48
        cikl1 = 54  
    elif (chisl == 'Числитель' and today_day==3):
        cikl = 54
        cikl1 = 60
    elif (chisl == 'Числитель' and today_day==4):
        cikl = 60
        cikl1 = 66
    elif (chisl == 'Числитель' and today_day==5):
        cikl = 66
        cikl1 = 100
    elif (chisl == 'Числитель' and today_day==6):   
        cikl = 100  
        cikl1 = 0
    key = cikl + 6
    key1 = cikl1 + 6

####################
##Основные функции##
####################
@dp.message_handler(commands='start')
async def start(message : types.Message):
    cur.execute(f'INSERT OR REPLACE INTO users VALUES("{message.from_user.id}","0","0")')
    conn.commit()
    texter = 'Добро пожаловать в petroshedulebot, мои создатели:\nБерозко Роман\nАверин Андрей\n\nCтуденты группы 39-55'
    await bot.send_photo(message.from_user.id, 
        'https://www.directum.ru/application/images/catalog/34597121.PNG', 
        texter, 
        reply_markup=keyboard.button_register,
        )
    await message.answer(f'Сегодня: {today}\n{days_naming[today_day]}')


@dp.message_handler(text=['Регистрация'])
async def register(message: types.Message):
    await bot.send_message(message.from_user.id,'Кто ты?',
    reply_markup=keyboard.button_who,
    )


@dp.message_handler(text=[f'{emoji.emojize(":school_satchel:", use_aliases=True)}Я студент'])
async def student_register(message: types.Message):
    await States.group.set()
    await bot.send_message(message.from_user.id,
    'Напиши номер своей группы',
    )


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
        cur.execute(f'UPDATE users SET group_number = "{group}" WHERE user_id = "{message.from_user.id}"')
        conn.commit()
        await state.finish()


@dp.message_handler(text=[f'{emoji.emojize(":mortar_board:", use_aliases=True)}Я преподаватель'])
async def teacher_register(message: types.Message):
    cur.execute(f'INSERT OR REPLACE INTO prepods VALUES("{message.from_user.id}","0","0")')
    conn.commit()
    await States.fio.set()
    await bot.send_message(message.from_user.id, 'Укажите свои ФИО как в расписании\nПример: Фамилия И.О.')


@dp.message_handler(state=States.fio)
async def fio(message: types.Message, state: FSMContext):
    async with state.proxy() as names:
        global fiot
        names['fiot'] = message.text
        await bot.send_message(message.chat.id, 
        md.text(md.text('Ваше ФИО:', 
        md.bold(names['fiot']))), 
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup= keyboard.button_go_main
        )
        grouper = md.text(md.text(md.bold(names['fiot'])))
        names = markdown(grouper)
        fiot = ''.join(BeautifulSoup(names).findAll(text=True))
        print(fiot)
        cur.execute(f'UPDATE prepods SET prep_name = "{fiot}" WHERE user_id = "{message.from_user.id}"')
        conn.commit()
        await state.finish()


@dp.message_handler(text=[f'{emoji.emojize(":wrench:", use_aliases=True)}Настройки', f'{emoji.emojize(":wrench:", use_aliases=True)}Назад в настройки'])
async def setting(message: types.Message):
    await message.answer('Добро пожаловать в меню настроек', 
    reply_markup=keyboard.button_notify,
    )


@dp.message_handler(text=[f'{emoji.emojize(":card_index:", use_aliases=True)}Сменить группу'])
async def rewrite (message: types.Message):
    await States.group.set()
    await message.answer('Введите новый номер группы:')


@dp.message_handler(text=[f'{emoji.emojize(":name_badge:", use_aliases=True)}Сменить ФИО'])
async def rewrite_fio (message: types.Message):
    await States.fio.set()
    await message.answer('Введите новое ФИО\nПример: Фамилия И.О.')


@dp.message_handler(text=[f'{emoji.emojize(":clock1:", use_aliases=True)}Время уведомлений', 'Время уведомлений'])
async def time_quest (message: types.Message):
    await message.answer('После смены времени нужно будет снова включить уведомления\nВведите время в формате: 00:00')
    await States.setting.set()


@dp.message_handler(text=[f'{emoji.emojize(":ballot_box_with_check:", use_aliases=True)}Вкл/Выкл уведомлений'])
async def time_set (message: types.Message):
    cur.execute(f'SELECT * FROM users WHERE user_id = "{message.from_user.id}"')
    result = cur.fetchall()
    time = [list(result[0])[2]][0]
    global x
    global y
    x = x + 1
    if x == 2:
        x = 0
    if x == 0:
        await message.answer ('Уведомления отключены')
    if x == 1 and y == 1:
        await message.answer('Уведомления на пары след. дня включены')
        await scheduler(message, time)
    elif x == 1 and y == 0:
        await message.answer('Уведомления на пары текущего дня включены')
        await scheduler_td(message, time)
    

@dp.message_handler(state=States.setting)
async def times_setting_set (message: types.Message, state = FSMContext):
    async with state.proxy() as times:
        global x
        x = 0
        times['times_set'] = message.text
        await bot.send_message(message.chat.id, 
        md.text(md.text('Установленное время:', 
        md.bold(times['times_set']))), 
        parse_mode=ParseMode.MARKDOWN_V2,
        reply_markup= keyboard.button_notify
        )
        timers = md.text(md.text(md.bold(times['times_set'])))
        rework = markdown(timers)
        setted_time = ''.join(BeautifulSoup(rework).findAll(text=True))
        cur.execute(f'UPDATE users SET notify_times = "{setted_time}" WHERE user_id = "{message.from_user.id}"')
        cur.execute(f'UPDATE prepods SET notify_times = "{setted_time}" WHERE user_id = "{message.from_user.id}"')
        conn.commit()
        await state.finish()


@dp.message_handler(text=[f'{emoji.emojize(":book:", use_aliases=True)}Пары на сегодня/завтра'])
async def change_day(message: types.Message):
    await message.answer('На какой день вы хотите получать расписание в установленное время?',
    reply_markup=keyboard.btn_change_day,
    )


@dp.message_handler(text=[f'{emoji.emojize(":notebook:", use_aliases=True)}На сегодня'])
async def pare_today(message: types.Message):
    global y
    y = 0
    await message.answer('Вы будете получать уведомление на текущий день')


@dp.message_handler(text=[f'{emoji.emojize(":notebook_with_decorative_cover:", use_aliases=True)}На завтра'])
async def pare_next_day(message: types.Message):
    global y
    y = 1
    await message.answer('Вы будете получать уведомление на следующий день')


@dp.message_handler(text=[f'{emoji.emojize(":clipboard:", use_aliases=True)}Получить расписание'])
async def schedule_menu(message: types.Message):
    await message.answer('Выберите на какой день получить расписание', 
    reply_markup=keyboard.button_schedule_choise,
    )


@dp.message_handler(text=[f'{emoji.emojize(":page_facing_up:", use_aliases=True)}Расписание на сегодня'])
async def schedule_today(message: types.Message):
    await week()
    global cikl
    global key
    if(cikl==100):
        await message.answer('Нет расписания на воскресенье')
    else:
        try:
            para_num = 1
            conn = sqlite3.connect('users_database.db')
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM users WHERE user_id = "{message.from_user.id}"')
            result = cur.fetchall()
            stud = pd.read_excel(f'stud_{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.xlsx')
            s1 =(stud[f'{[list(result[0])[1]][0]}'].tolist())
            group_num = [list(result[0])[1]][0]
            text = ''
            while cikl < key:
                skip = str(s1[cikl])
                if (skip == 'nan'):
                    text = f'{text}\n\n{para_num} пара:\n  -'
                    cikl = cikl + 1
                    para_num = para_num + 1
                else:
                    text = f'{text}\n\n{para_num} пара:\n  {s1[cikl]}'
                    cikl = cikl + 1
                    para_num = para_num + 1
            await message.answer(text)
            try:
                conn = sqlite3.connect('zamen.db')
                cur = conn.cursor()
                cur.execute(f'SELECT * FROM raspis WHERE groups LIKE "%{group_num}%"')
                res1 = cur.fetchall()
                b1 = " "
                schet = 0
                for row in res1:
                    schet = schet + 1
                    a1 = f"Группа: {row[0]}"
                    a2 = f'Номер пары: {row[1]}'
                    a3 = f'Пара по расписанию: {row[2]}'
                    a4 = f'Пара по замене: {row[3]}'
                    b1 = b1 + f'Замена:{schet}\n{a1}\n{a2}\n{a3}\n{a4}\n\n'
            except Exception:
                print('Bad zamen today student')
            await message.answer(b1)


        except Exception:
            try:
                para_num = 1
                conn = sqlite3.connect('users_database.db')
                cur = conn.cursor()
                cur.execute(f'SELECT * FROM prepods WHERE user_id = "{message.from_user.id}"')
                result = cur.fetchall()
                stud = pd.read_excel(f'prep_{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.xlsx')
                s1 =(stud[f'{[list(result[0])[1]][0]}'].tolist())
                prepodavat = [list(result[0])[1]][0]
                text = ''
                skip = ''
                while cikl < key:
                    skip = str(s1[cikl])
                    if (skip == 'nan'):
                        text = f'{text}\n\n{para_num} пара:\n  -'
                        cikl = cikl + 1
                        para_num = para_num + 1
                    else:
                        text = f'{text}\n\n{para_num} пара:\n  {s1[cikl]}'
                        cikl = cikl + 1
                        para_num = para_num + 1
                await message.answer(text)
                try:
                    conn = sqlite3.connect('zamen.db')
                    cur = conn.cursor()
                    cur.execute(f'SELECT * FROM raspis WHERE para_zam LIKE "%{prepodavat}%"')
                    res1 = cur.fetchall()
                    b1 = " "
                    schet = 0
                    for row in res1:
                        schet = schet + 1
                        a1 = f"Группа: {row[0]}"
                        a2 = f'Номер пары: {row[1]}'
                        a3 = f'Пара по расписанию: {row[2]}'
                        a4 = f'Пара по замене: {row[3]}'
                        b1 = b1 + f'Замена:{schet}\n{a1}\n{a2}\n{a3}\n{a4}\n\n'
                except Exception:
                    print('Bad zamen today prepodavat')
                await message.answer(b1)
            except Exception:
                await message.answer('Если вы не получили расписание проверьте профиль')


@dp.message_handler(text=[f'{emoji.emojize(":page_with_curl:", use_aliases=True)}Расписание на завтра'])
async def schedule_next_day(message: types.Message):
    await week()
    global cikl1
    global key1
    if(cikl1==100):
        await message.answer('Нет расписания на воскресенье')
    else:
        try:
            para_num = 1
            conn = sqlite3.connect('users_database.db')
            cur = conn.cursor()
            cur.execute(f'SELECT * FROM users WHERE user_id = "{message.from_user.id}"')
            result = cur.fetchall()
            stud = pd.read_excel(f'stud_{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.xlsx')
            s1 =(stud[f'{[list(result[0])[1]][0]}'].tolist())
            group_num = [list(result[0])[1]][0]
            skip = ''
            text = ''
            while cikl1 < key1:
                skip = str(s1[cikl1])
                if (skip == 'nan'):
                    text = f'{text}\n\n{para_num} пара:\n  -'
                    cikl1 = cikl1 + 1
                    para_num = para_num + 1
                else:
                    text = f'{text}\n\n{para_num} пара:\n  {s1[cikl1]}'
                    cikl1 = cikl1 + 1
                    para_num = para_num + 1
            await message.answer(text)
            try:
                conn = sqlite3.connect('zamen_next.db')
                cur = conn.cursor()
                cur.execute(f'SELECT * FROM raspis WHERE groups LIKE "%{group_num}%"')
                res1 = cur.fetchall()
                b1 = " "
                schet = 0
                for row in res1:
                    schet = schet + 1
                    a1 = f"Группа: {row[0]}"
                    a2 = f'Номер пары: {row[1]}'
                    a3 = f'Пара по расписанию: {row[2]}'
                    a4 = f'Пара по замене: {row[3]}'
                    b1 = b1 + f'Замена:{schet}\n{a1}\n{a2}\n{a3}\n{a4}\n\n'
            except Exception:
                print('Bad zamen next day student')
            await message.answer(b1)

        except Exception:
            try:
                para_num = 1
                conn = sqlite3.connect('users_database.db')
                cur = conn.cursor()
                cur.execute(f'SELECT * FROM prepods WHERE user_id = "{message.from_user.id}"')
                result = cur.fetchall()
                stud = pd.read_excel(f'prep_{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.xlsx')
                s1 =(stud[f'{[list(result[0])[1]][0]}'].tolist())
                prepodavat = [list(result[0])[1]][0]
                skip = ''
                text = ''
                while cikl1 < key1:
                    skip = str(s1[cikl1])
                    if (skip == 'nan'):
                        text = f'{text}\n\n{para_num} пара:\n  -'
                        cikl1 = cikl1 + 1
                        para_num = para_num + 1  
                    else:
                        text = f'{text}\n\n{para_num} пара:\n  {s1[cikl1]}'
                        cikl1 = cikl1 + 1
                        para_num = para_num + 1
                await message.answer(text)
                try:
                    conn = sqlite3.connect('zamen_next.db')
                    cur = conn.cursor()
                    cur.execute(f'SELECT * FROM raspis WHERE para_zam LIKE "%{prepodavat}%"')
                    res1 = cur.fetchall()
                    b1 = " "
                    schet = 0
                    for row in res1:
                        schet = schet + 1
                        a1 = f"Группа: {row[0]}"
                        a2 = f'Номер пары: {row[1]}'
                        a3 = f'Пара по расписанию: {row[2]}'
                        a4 = f'Пара по замене: {row[3]}'
                        b1 = b1 + f'Замена:{schet}\n{a1}\n{a2}\n{a3}\n{a4}\n\n'
                except Exception:
                    print('Bad zamen today prepodavat')
                await message.answer(b1)
            except Exception:
                await message.answer('Если вы не получили расписание проверьте профиль')


@dp.message_handler(text=['Перейти в главное меню', 'Вернутся в главное меню', f'{emoji.emojize(":arrow_left:", use_aliases=True)}Назад', 'Назад'])
async def main_menu (message: types.Message):
    global x
    if x == 0:
        sost = f"Выкл{emoji.emojize(':ballot_box_with_check:', use_aliases=True)}"
    if x == 1:
        sost = f"Вкл{emoji.emojize(':white_check_mark:', use_aliases=True)}"
    await bot.send_message(message.from_user.id, 
        f'Добро пожаловать в главное меню.\nЗдесь вы можете настроить уведомления\nА также получить расписание вручную\n\nСостояние уведомлений: {sost}\n\n{emoji.emojize(":exclamation:", use_aliases=True)}ЧТОБЫ ПОЛУЧАТЬ РАСПИСАНИЕ НА ПРЕПОДАВАТЕЛЯ У ВАС НЕ ДОЛЖЕН БЫТЬ УСТАНОВЛЕН НОМЕР ГРУППЫ{emoji.emojize(":exclamation:", use_aliases=True)}', 
        reply_markup=keyboard.button_main,
        )


@dp.message_handler(text=[f'{emoji.emojize(":briefcase:", use_aliases=True)}Мой профиль'])
async def get_profile(message: types.Message):
    await message.answer('Какой профиль вам нужен?', reply_markup=keyboard.button_stpr)


@dp.message_handler(text=[f'{emoji.emojize(":school_satchel:", use_aliases=True)}Студент'])
async def student (message: types.Message):
    try:
        conn = sqlite3.connect('users_database.db')
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM users WHERE user_id = "{message.from_user.id}"')
        result = cur.fetchall()
        await bot.send_message(message.from_user.id, f'Студент:\nID = {list(result[0])[0]}\nGroup = {[list(result[0])[1]][0]}\nTime = {[list(result[0])[2]][0]}')
    except Exception:
        await message.answer('Пользователь не найден, пожалуйста пройдите регистрацию снова написав /start')


@dp.message_handler(text=[f'{emoji.emojize(":mortar_board:", use_aliases=True)}Преподаватель'])
async def profile1 (message:types.Message):
    try:
        conn = sqlite3.connect('users_database.db')
        cur = conn.cursor()
        cur.execute(f'SELECT * FROM prepods WHERE user_id = "{message.from_user.id}"')
        result1 = cur.fetchall()
        await bot.send_message(message.from_user.id, f'Преподаватель:\nID = {list(result1[0])[0]}\nФИО = {[list(result1[0])[1]][0]}\nTime = {[list(result1[0])[2]][0]}')
    except Exception:
        await message.answer('Пользователь не найден, пожалуйста пройдите регистрацию снова написав /start')


@dp.message_handler(text=f'{emoji.emojize(":email:", use_aliases=True)}Помощь')
async def user_help (message: types.Message):
    photo = ['https://sun9-45.userapi.com/impg/L_ZjDqZoxr0-Ps0fQi0-c48PjJ-UWJk64exZqw/HrcqjPtfIjE.jpg?size=840x737&quality=96&sign=e78ad3ba428e817729e80c0f02d249df&type=album', 
    'https://sun9-30.userapi.com/impg/S-bSLtCaDlC1bcUwMCDlCAyzerrNVqFgw5Ygpg/BoLXpwQ1HcY.jpg?size=608x770&quality=96&sign=e101f67bcaa95f1aec2d52a651d24cef&type=album', 
    'https://sun9-64.userapi.com/impg/v9TI88OR_8UV_CJ2u2FRJlSjFiRhpoh_lFKSFg/jPCHxw5V4WQ.jpg?size=1125x1077&quality=96&sign=b62f3c74fd48e7831d66add4eb792715&type=album',
    ]
    await bot.send_photo(message.from_user.id, photo[random.randint(0,2)])
    await message.answer('Отправить сообщение разработчикам: /msgtadm\nПройти регистрацию с самого начала /start\n\n©Author', reply_markup = keyboard.btn_back)
    
#dop commands
@dp.message_handler(commands=['msgtadm'])
async def msgtoadmins(message: types.Message):
    await message.answer('!!!Нужно обязательно указать ник телеграм!!!\nВаше сообщение:')
    await States.sndmsg.set()


@dp.message_handler(state=States.sndmsg)
async def msgtoadminist(message: types.Message, state= FSMContext):
    try:
        async with state.proxy() as msg:
            msg['bef'] = message.text
            bef = md.text(md.text(md.bold(msg['bef'])))
            reworkbef = markdown(bef)
            tgo = ''.join(BeautifulSoup(reworkbef).findAll(text=True))
            await bot.send_message(admin_id, f'{message.from_user.username}\nНаписал:\n{tgo}')
            await bot.send_message(admin2_id, f'{message.from_user.username}\nНаписал:\n{tgo}')
            await state.finish()
    except Exception:
        await message.answer('Сообщение не доставлено одному из администраторов но вам в скором времени ответят')
        await state.finish()


@dp.message_handler(text=f'{emoji.emojize(":exclamation:", use_aliases=True)}Внимание')
async def waern (message: types.Message):
    await started()
    global message_for_see
    await message.answer(message_for_see, reply_markup=keyboard.btn_back)


@dp.message_handler(text="Изменения")
async def changes (message: types.Message):
    sender = InputFile('/home/author/horde/table.txt', 'zameni_today.txt')
    await bot.send_document(message.from_user.id, sender)

#####################
##Админские функции##
#####################
@dp.message_handler(commands=['adm1_set'])
async def Adm1_set(message: types.message, state=FSMContext):
    await States.adm1_set.set()
    await message.answer('Message:')


@dp.message_handler(state=States.adm1_set)
async def Adm1_setting(message: types.message, state=FSMContext):
    try:
        if admin_id == f'{message.from_user.id}' or admin2_id == f'{message.from_user.id}':
            async with state.proxy() as usr:
                global reworks
                usr['bef'] = message.text
                bef = md.text(md.text(md.bold(usr['bef'])))
                reworkbef = markdown(bef)
                reworks = ''.join(BeautifulSoup(reworkbef).findAll(text=True))
                await bot.send_message(message.from_user.id, reworks)
                await state.finish()
        else:
            await message.answer('This command admin only') 
    except Exception:
        print('Bad1')


@dp.message_handler(commands=['adm1'])
async def Adm1(message: types.message, state=FSMContext):
    await States.adm1.set()
    await message.answer('user_id:')
 

@dp.message_handler(state=States.adm1)
async def Adm1_st(message: types.message, state=FSMContext):
    try:
        if admin_id == f'{message.from_user.id}' or admin2_id == f'{message.from_user.id}':
            async with state.proxy() as usr:
                global reworks
                usr['us_id'] = message.text
                bef = md.text(md.text(md.bold(usr['us_id'])))
                rew = markdown(bef)
                rework1 = ''.join(BeautifulSoup(rew).findAll(text=True))
                await bot.send_message(rework1,reworks)
                await state.finish()
        else:
            await message.answer('This command admin only')    
    except Exception:
        print ("bad")


@dp.message_handler(commands=['start_f'])
async def start_f (message: types.Message):
    while True:
        await search()
        await asyncio.sleep(300)
        await buti()
        await asyncio.sleep(3600)
        

@dp.message_handler(commands=['adm_usr_list'])
async def userlist (message: types.Message):
    if admin_id == f'{message.from_user.id}' or admin2_id == f'{message.from_user.id}':
        await bot.send_document(message.from_user.id, dbfile)

####################################
##Расписание уведомлений и запуска##
####################################
async def scheduler(message: types.Message, time):
    global x
    try:
        aioschedule.every().day.at(time).do(schedule_next_day, message)
        while x == 1:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
    except Exception:
        print ('Trouble with schedule')

async def scheduler_td(message: types.Message, time):
    global x
    try:
        aioschedule.every().day.at(time).do(schedule_today, message)
        while x == 1:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
    except Exception:
        print ('Trouble with schedule')


@dp.message_handler(commands=['test'])
async def test(message:types.Message):
    print("test")

###############
##Сабпроцессы##
###############
async def search():
    subprocess.Popen(['python3', 'take_resp.py'])

async def buti():
    subprocess.Popen(['python3', 'butify.py'])


if __name__=='__main__':
    executor.start_polling(dp, skip_updates=True)
