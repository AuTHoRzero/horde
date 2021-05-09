##############
##Библиотеки##
##############
import datetime
from requests_ntlm2 import HttpNtlmAuth
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
import requests
import os 

#################################
##Время и переменные для поиска##
#################################
days_naming = ["Понедельник","Вторник","Среда","Четверг","Пятница","Суббота", " "]
today_day = datetime.datetime.today().weekday()
next_day = today_day + 1
if next_day == 7:
    next_day = 0
today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)
day_before = today - datetime.timedelta(days=1)
a = f'Замена на {tomorrow.strftime("%d")}.{tomorrow.strftime("%m")}.{tomorrow.year}г., {days_naming[next_day]}'
b = f'Замена на {today.strftime("%d")}.{today.strftime("%m")}.{today.year}г., {days_naming[today_day]}'

print(f'{a}\n{b}')
###################
##Создание файлов##
###################
inf = open(f'/home/{os.getlogin()}/horde/info_{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.html', "w")
f = open(f'/home/{os.getlogin()}/horde/{tomorrow.strftime("%d")}.{tomorrow.strftime("%m")}.{tomorrow.year}.html',"w")
f1 = open(f'/home/{os.getlogin()}/horde/{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.html', "w")
f2 = open(f'/home/{os.getlogin()}/horde/stud_{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.xlsx', "wb")
f3 = open(f'/home/{os.getlogin()}/horde/prep_{today.strftime("%d")}.{today.strftime("%m")}.{today.year}.xlsx', "wb")

#######################################################################
##Авторизация в аккаунте Firefox (нужно чтоб пройти ntlm авторизацию)##
#######################################################################
profile = webdriver.FirefoxProfile('/home/author/.mozilla/firefox/jb93v9bl.default-esr')
option = webdriver.FirefoxOptions()
option.add_argument("user-agent=Mozila/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
driver = webdriver.Firefox(profile, options=option)
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

####################################
##Авторизация на сайте петровского##
####################################
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
    inf_page = driver.page_source
    inf.write(inf_page)
    time.sleep(1)
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
    zamen_tod = driver.find_element_by_partial_link_text(b)
    href1 = zamen_tod.get_attribute('href')
    time.sleep(2)
    driver.get(href1)
    time.sleep(3)
    html1 = driver.page_source
    f1.write(html1)
except Exception:
    print('step 5')

##################
##excel студенты##
##################
try:
    driver.get('https://portal.petrocollege.ru/Lists/2014')
    time.sleep(2)
    shach_stud = driver.find_element_by_xpath('/html/body/form/div[3]/div/div[3]/div/div[1]/div/div/div[1]/span/div[1]/div/div/div/table/tbody/tr/td/table/tbody/tr[1]/td[2]/div/a')
    href2 = shach_stud.get_attribute('href')
    driver.get(href2)
    time.sleep(4)
    urltoexcel = driver.find_element_by_xpath('/html/body/form/div[3]/div/div[3]/div/div[1]/div/div/div[1]/span/div[1]/table/tbody/tr/td/div/div/div/div/table/tbody/tr/td[1]/span/table[1]/tbody/tr[3]/td[2]/table/tbody/tr/td/span/a')
    urltoexcel.click
    href3 = urltoexcel.get_attribute('href')
#    driver.get(href3)
    auth = HttpNtlmAuth('10190128', 'nhPpYu90Ag')
    file_xlsx = requests.get(href3, auth=auth)
    time.sleep(10)
    f2.write(file_xlsx.content)
    f2.close
    time.sleep(5)
except Exception:
    print ('step 6')

#################
##excel преподы##
#################
try:
    driver.get('https://portal.petrocollege.ru/Lists/2014')
    time.sleep(2)
    time.sleep(3)
    prep_link = driver.find_element_by_xpath('/html/body/form/div[3]/div/div[3]/div/div[1]/div/div/div[1]/span/div[1]/div/div/div/table/tbody/tr/td/table/tbody/tr[3]/td[2]/div/a')
    href4 = prep_link.get_attribute('href')
    time.sleep(1)
    driver.get(href4)
    time.sleep(2)
    prepod_shach = driver.find_element_by_xpath('/html/body/form/div[3]/div/div[3]/div/div[1]/div/div/div[1]/span/div[1]/table/tbody/tr/td/div/div/div/div/table/tbody/tr/td[1]/span/table[1]/tbody/tr[3]/td[2]/table/tbody/tr/td/span/a')
    href5 = prepod_shach.get_attribute('href')
    file_xlsx1 = requests.get(href5, auth=auth)
    time.sleep(5)
    f3.write(file_xlsx1.content)
    f3.close
except Exception:
    print('step 7')

#######################
##Выключение браузера##
#######################
driver.close()

##########################
##Удаление старых файлов##
##########################
try:
     os.remove(f'{day_before.strftime("%d")}.{day_before.strftime("%m")}.{day_before.year}.html')
except Exception:
    print('No zamen past')
try:
     os.remove(f'stud_{day_before.strftime("%d")}.{day_before.strftime("%m")}.{day_before.year}.xlsx')
except Exception:
    print('No stud past')
try:
     os.remove(f'prep_{day_before.strftime("%d")}.{day_before.strftime("%m")}.{day_before.year}.xlsx')
except Exception:
    print('No prep past')
try:
     os.remove(f'info_{day_before.strftime("%d")}.{day_before.strftime("%m")}.{day_before.year}.html')
except Exception:
    print('No info past')
