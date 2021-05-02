import emoji
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

#Button need
reset1_button = KeyboardButton(f'{emoji.emojize(":name_badge:", use_aliases=True)}Сменить ФИО')
reset_button = KeyboardButton(f'{emoji.emojize(":card_index:", use_aliases=True)}Сменить группу')
back_btn = KeyboardButton(f'{emoji.emojize(":arrow_left:", use_aliases=True)}Назад')
backkprof = KeyboardButton(f'{emoji.emojize(":briefcase:", use_aliases=True)}Назад к профилям')
back_settng = KeyboardButton(f'{emoji.emojize(":wrench:", use_aliases=True)}Назад в настройки')
btn_back_to_profile = ReplyKeyboardMarkup(resize_keyboard=True).add(backkprof)
btn_back = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(back_btn)
warn = KeyboardButton(f'{emoji.emojize(":exclamation:", use_aliases=True)}Внимание')
#Group 1    
student_button = KeyboardButton(f'{emoji.emojize(":school_satchel:", use_aliases=True)}Я студент')
teacher_button = KeyboardButton(f'{emoji.emojize(":mortar_board:", use_aliases=True)}Я преподаватель')
button_who = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(student_button).add(teacher_button)
#Group 2
register_button = KeyboardButton('Регистрация')
button_register = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(register_button)
#Group 3
profile_button = KeyboardButton(f'{emoji.emojize(":briefcase:", use_aliases=True)}Мой профиль')
help_button = KeyboardButton(f'{emoji.emojize(":email:", use_aliases=True)}Помощь')
setting_button = KeyboardButton(f'{emoji.emojize(":wrench:", use_aliases=True)}Настройки')
schedule_button = KeyboardButton(f'{emoji.emojize(":clipboard:", use_aliases=True)}Получить расписание')
button_main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(schedule_button, warn).row(setting_button, profile_button).add(help_button)
#Group 4
go_to_main_button = KeyboardButton('Перейти в главное меню')
button_go_main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(go_to_main_button)
#Group 5
today_button = KeyboardButton(f'{emoji.emojize(":page_facing_up:", use_aliases=True)}Расписание на сегодня')
next_day_button = KeyboardButton(f'{emoji.emojize(":page_with_curl:", use_aliases=True)}Расписание на завтра')
button_schedule_choise = ReplyKeyboardMarkup(resize_keyboard=True).row(today_button, next_day_button).add(back_btn)
#Group 6
day_notify = KeyboardButton(f'{emoji.emojize(":book:", use_aliases=True)}Пары на сегодня/завтра')
time_set_button = KeyboardButton(f'{emoji.emojize(":clock1:", use_aliases=True)}Время уведомлений')
notify_switch_button = KeyboardButton(f'{emoji.emojize(":ballot_box_with_check:", use_aliases=True)}Вкл/Выкл уведомлений')
button_notify = ReplyKeyboardMarkup(resize_keyboard=True).row(time_set_button, notify_switch_button).row(reset_button, reset1_button).add(day_notify).add(back_btn)
#Group 7
today = KeyboardButton(f'{emoji.emojize(":notebook:", use_aliases=True)}На сегодня')
next_day = KeyboardButton(f'{emoji.emojize(":notebook_with_decorative_cover:", use_aliases=True)}На завтра')
btn_change_day = ReplyKeyboardMarkup(resize_keyboard=True).row(today, next_day).add(back_settng)
#Group 8
student = KeyboardButton(f'{emoji.emojize(":school_satchel:", use_aliases=True)}Студент')
prepod = KeyboardButton(f'{emoji.emojize(":mortar_board:", use_aliases=True)}Преподаватель')
button_stpr = ReplyKeyboardMarkup(resize_keyboard=True).row(student, prepod).add(back_btn)

#fun
hi = KeyboardButton('Привет)')
hi_btn = ReplyKeyboardMarkup(resize_keyboard=True).add(hi)

hi1 = KeyboardButton('Спасибо')
hi2 = KeyboardButton('Нет')
hi_btn1 = ReplyKeyboardMarkup(resize_keyboard=True).row(hi1, hi2)

hi3 = KeyboardButton('1')
hi4 = KeyboardButton('2')
hi_btn2 = ReplyKeyboardMarkup(resize_keyboard=True).row(hi3, hi4)

hi5 = KeyboardButton('Дальше')
hi_btn3 = ReplyKeyboardMarkup(resize_keyboard=True).add(hi5)

hi6 = KeyboardButton('Пагнали')
hi7 = KeyboardButton('Конец(')
hi_btn4 = ReplyKeyboardMarkup(resize_keyboard=True).add(hi6).add(hi7)