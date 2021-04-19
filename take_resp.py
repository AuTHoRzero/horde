import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import os 

#Для замен
days_naming = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота"]
today_day = datetime.datetime.today().weekday()
next_day = today_day + 1
if next_day == 7:
    next_day = 0
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
a = f'Замена на {tomorrow.strftime("%d")}.{tomorrow.strftime("%m")}.{tomorrow.year}г., {days_naming[next_day]}'
b = f'Замена на {today.strftime("%d")}.{today.strftime("%m")}.{today.year}г., {days_naming[today_day]}'

#Создание файлов
f1 = open(f'/home/user/horde/{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.txt', "w")
f = open(f'/home/user/horde/{tomorrow.strftime("%d")}.{tomorrow.strftime("%m")}.{tomorrow.year}.txt',"w")

#Авторизация в аккаунте Firefox (нужно чтоб пройти ntlm авторизацию)
option = webdriver.FirefoxOptions()
option.add_argument("user-agent=Mozila/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
driver = webdriver.Firefox(options=option)
action = ActionChains(driver)
try:
    driver.get('https://accounts.firefox.com/?context=fx_desktop_v3&entrypoint=fxa_discoverability_native&action=email&service=sync')
    time.sleep(1)
    em_inp = driver.find_element_by_name("email")
    em_inp.send_keys('')
    time.sleep(.5)
    cont_btn = driver.find_element_by_id('submit-btn').click()
    time.sleep(1)
    pas = driver.find_element_by_id("password")
    pas.send_keys("")
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
except Exception:
    print ('step 3')

try:
    zamen = driver.find_element_by_link_text(a)
    href = zamen.get_attribute('href')
    time.sleep(4)
    driver.get(href)
    time.sleep(5)
    html = driver.page_source
    time.sleep(2)
#    print(html)
    f.write(html)
    time.sleep(2)
except Exception:
    print ('step 4')

try:
    driver.get('https://portal.petrocollege.ru/Pages/responsiveSh-aspx.aspx')
    time.sleep(2)
    zamen_tod = driver.find_element_by_link_text(b)
    href1 = zamen_tod.get_attribute('href')
    time.sleep(2)
    driver.get(href1)
    time.sleep(3)
    html1 = driver.page_source
    f1.write(html1)
except Exception:
    print('step 5')

try:
    driver.get('https://portal.petrocollege.ru/Pages/responsiveSh-aspx.aspx')
    time.sleep(2)
    shach_stud = driver.find_element_by_link_text('Шахматка групп (полная)')
    href2 = shach_stud.get_attribute('href')
    driver.get(href2)
    time.sleep(4)
    urltoexcel = driver.find_element_by_id('{415fde80-df25-40c0-b26a-235b63facdf1}').find_element_by_tag_name('a')
    href3 = urltoexcel.get_attribute('href')
    driver.get(href3)
    time.sleep(20)
except Exception:
    print ('step 6')

driver.close()
os.rename(f'{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.txt', f'{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.html') 
os.rename(f'{tomorrow.strftime("%d")}.{tomorrow.strftime("%m")}.{tomorrow.year}.txt', f'{tomorrow.strftime("%d")}.{tomorrow.strftime("%m")}.{tomorrow.year}.html')
