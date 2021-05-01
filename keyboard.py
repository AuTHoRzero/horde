import emoji
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

#Button need
reset1_button = KeyboardButton('Сменить ФИО')
reset_button = KeyboardButton('Сменить группу')
back_btn = KeyboardButton(f'{emoji.emojize(":arrow_left:", use_aliases=True)}Назад')
backkprof = KeyboardButton(f'{emoji.emojize(":briefcase:", use_aliases=True)}Назад к профилям')
back_settng = KeyboardButton(f'{emoji.emojize(":wrench:", use_aliases=True)}Назад в настройки')
btn_back_to_profile = ReplyKeyboardMarkup(resize_keyboard=True).add(backkprof)
btn_back = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(back_btn)
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
button_main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(schedule_button).row(setting_button, profile_button).add(help_button)
#Group 4
go_to_main_button = KeyboardButton('Перейти в главное меню')
button_go_main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(go_to_main_button)
#Group 5
today_button = KeyboardButton(f'{emoji.emojize(":page_facing_up:", use_aliases=True)}Расписание на сегодня')
next_day_button = KeyboardButton(f'{emoji.emojize(":page_with_curl:", use_aliases=True)}Расписание на завтра')
button_schedule_choise = ReplyKeyboardMarkup(resize_keyboard=True).row(today_button, next_day_button).add(back_btn)
#Group 6
day_notify = KeyboardButton('Пары на сегодня/завтра')
time_set_button = KeyboardButton(f'{emoji.emojize(":clock1:", use_aliases=True)}Время уведомлений')
notify_switch_button = KeyboardButton(f'{emoji.emojize(":ballot_box_with_check:", use_aliases=True)}Вкл/Выкл уведомлений')
button_notify = ReplyKeyboardMarkup(resize_keyboard=True).row(time_set_button, notify_switch_button).row(reset_button, reset1_button).add(day_notify).add(back_btn)
#Group 7
today = KeyboardButton('На сегодня')
next_day = KeyboardButton('На завтра')
btn_change_day = ReplyKeyboardMarkup(resize_keyboard=True).row(today, next_day).add(back_settng)
#Group 8
student = KeyboardButton(f'{emoji.emojize(":school_satchel:", use_aliases=True)}Студент')
prepod = KeyboardButton(f'{emoji.emojize(":mortar_board:", use_aliases=True)}Преподаватель')
button_stpr = ReplyKeyboardMarkup(resize_keyboard=True).row(student, prepod).add(back_btn)
