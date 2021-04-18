#!/usr/bin/sudo python
import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from requests_ntlm2 import HttpNtlmAuth
import time

f = open('/home/author/horde/24.txt',"w")
#Для замен
days_naming = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота"]
today_day = datetime.datetime.today().weekday()
next_day = today_day + 1
if next_day == 7:
    next_day = 0
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
a = f'Замена на {tomorrow.strftime("%d")}.{tomorrow.strftime("%m")}.{tomorrow.year}г., {days_naming[next_day]}'

#Авторизация в аккаунте Firefox (нужно чтоб пройти ntlm авторизацию)
option = webdriver.FirefoxOptions()
option.add_argument("user-agent=Mozila/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
driver = webdriver.Firefox(options=option)
action = ActionChains(driver)
try:
    driver.get('https://accounts.firefox.com/?context=fx_desktop_v3&entrypoint=fxa_discoverability_native&action=email&service=sync')
    time.sleep(1)
    em_inp = driver.find_element_by_name("email")
    em_inp.send_keys('berozko.roman@yandex.ru')
    time.sleep(.5)
    cont_btn = driver.find_element_by_id('submit-btn').click()
    time.sleep(1)
    pas = driver.find_element_by_id("password")
    pas.send_keys("78697869r")
    time.sleep(.4)
    ent_btn = driver.find_element_by_id("submit-btn").click()
    time.sleep(18)
except Exception:
    print('bad login')

#Авторизация на сайте петровского
try:
    driver.get("https://portal.petrocollege.ru")
    WebDriverWait(driver,10).until(EC.alert_is_present(),"wait for alert pop out")
    alert_window=driver.switch_to_alert()
    time.sleep(1)
    alert_window.accept()
    time.sleep(5)
except Exception:
    print ('bad college')
#Переход на страницу с расписанием
try:
    driver.get('https://portal.petrocollege.ru/Pages/responsiveSh-aspx.aspx')
    time.sleep(3)
#    pre_kab = Select(driver.find_element_by_id('ctl00_ctl47_g_463119f4_303b_4073_861b_b8e973140866_selectaction'))
#    time.sleep(1)
#    pre_kab.select_by_visible_text('По группе')
except Exception:
    print ('3')

try:
    zamen = driver.find_element_by_link_text(a)
    href = zamen.get_attribute('href')
    time.sleep(4)
    driver.get(href)
    time.sleep(5)
    html = driver.page_source
    time.sleep(2)
    print(html)
except Exception:
    print ('4')

f.write(html)
