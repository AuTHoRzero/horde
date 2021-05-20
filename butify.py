##############
##Библиотеки##
##############
from bs4 import BeautifulSoup
import requests
from requests_ntlm2 import HttpNtlmAuth
from pprint import pprint
import pandas as pd
import sqlite3
import datetime
import os

#########
##Время##
#########
today_day = datetime.datetime.today().weekday()
next_day = today_day + 1
if next_day == 7:
    next_day = 0
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
day_before = today - datetime.timedelta(days=1)

#############################
##Стираем устаревшие замены##
#############################
try:
    os.remove('zamen.db')
except Exception:
    print ('no zamen')
try:
    os.remove('zamen1.db')
except Exception:
    print('no zamen1')
try:
    os.remove('zamen_next.db')
except Exception:
    print('no next zamen')
try:
    os.remove('zamen_next1.db')
except Exception:
    print('no next zamen1')

#####################
##Замены на сегодня##
#####################
try:
    with open (f'{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, "xml")

    conn = sqlite3.connect('zamen.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS raspis(groups TEXT, para_n TEXT, para_rasp TEXT, para_zam TEXT)')
    try:

        table = soup.find("table", class_= 'ms-rteTable-default')
        for rw in table.find_all("tbody"):
            rows = rw.find_all('tr')
            for row in rows:
                first = row.find_all('td')
                num_gr = first[0].get_text()
                num_les = first[1].get_text()
                less_do = first[2].get_text()
                less_af = first[3].get_text()
#                print(f'{num_gr} {num_les} {less_do} {less_af}')
                cur.execute(f'INSERT OR REPLACE INTO raspis VALUES("{num_gr}","{num_les}","{less_do}","{less_af}")')
                conn.commit()
    except Exception as ext:
        print(f'1.1\n{ext}')
    conn = sqlite3.connect('zamen1.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS raspis(groups TEXT, para_n TEXT, para_rasp TEXT, para_zam TEXT)')
    try:
        table = soup.find("table", class_= 'ms-rteTable-default').find_next("table", class_= 'ms-rteTable-default')
        for rw in table.find_all("tbody"):
            rows = rw.find_all('tr')
            for row in rows:
                first = row.find_all('td')
                num_gr = first[0].get_text()
                num_les = first[1].get_text()
                less_do = first[2].get_text()
                less_af = first[3].get_text()
#                print(f'{num_gr} {num_les} {less_do} {less_af}')
                cur.execute(f'INSERT OR REPLACE INTO raspis VALUES("{num_gr}","{num_les}","{less_do}","{less_af}")')
                conn.commit()
    except Exception as ext:
        print(f'1.2\n{ext}')
except Exception:
    print('no today zamen')

####################
##Замены на завтра##
####################
try: 
    with open (f'{tomorrow.strftime("%d")}.{tomorrow.strftime("%m")}.{tomorrow.year}.html') as file:
        src = file.read()

    soup = BeautifulSoup(src, "xml")

    conn = sqlite3.connect('zamen_next.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS raspis(groups TEXT, para_n TEXT, para_rasp TEXT, para_zam TEXT)')

    try:
        table = soup.find("table", class_= 'ms-rteTable-default')
        for rw in table.find_all("tbody"):
            rows = rw.find_all('tr')
            for row in rows:
                try:
                    first = row.find_all('td')
                    num_gr = first[0].get_text()
                    num_les = first[1].get_text()
                    less_do = first[2].get_text()
                    less_af = first[3].get_text()
#                print(f'{num_gr} {num_les} {less_do} {less_af}')
                    cur.execute(f'INSERT OR REPLACE INTO raspis VALUES("{num_gr}","{num_les}","{less_do}","{less_af}")')
                    conn.commit()
                except Exception:
                    pass
    except Exception as ext:
        print(f"2.1\n{ext}")

    conn = sqlite3.connect('zamen_next1.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS raspis(groups TEXT, para_n TEXT, para_rasp TEXT, para_zam TEXT)')

    try:
        table = soup.find("table", class_= 'ms-rteTable-default').find_next("table", class_= 'ms-rteTable-default')
        for rw in table.find_all("tbody"):
            rows = rw.find_all('tr')
            for row in rows:
                first = row.find_all('td')
                num_gr = first[0].get_text()
                num_les = first[1].get_text()
                less_do = first[2].get_text()
                less_af = first[3].get_text()
#                print(f'{num_gr} {num_les} {less_do} {less_af}')
                cur.execute(f'INSERT OR REPLACE INTO raspis VALUES("{num_gr}","{num_les}","{less_do}","{less_af}")')
                conn.commit()
    except Exception as ext:
        print(f"2.2\n{ext}")
except Exception as ext:
    print(f'No next zamen\n{ext}')

try:
    os.remove(f'/home/{os.getlogin()}/horde/{tomorrow.strftime("%d")}.{tomorrow.strftime("%m")}.{tomorrow.year}.html')
except Exception:
    print('Cant delete')
try:
    os.remove(f'/home/{os.getlogin()}/horde/{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.html')
except Exception:
    print('Cant delete 2')