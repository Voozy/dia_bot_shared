import config
import telebot

from SugarSql import SugarInsert
from SugarSql import SugarSelect

from telebot import types
from datetime import datetime

bot = telebot.TeleBot(config.token)
user_dict = {}


#=============================================
#КЛАВИАТУРА ОСНОВНОГО МЕНЮ
#=============================================

def _mainMenu(msg, menu_message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_enter = types.KeyboardButton(text="Внести запись")
    button_report = types.KeyboardButton(text="Создать отчет")
    button_last = types.KeyboardButton(text="Последняя запись")
    keyboard.add(button_enter, button_report, button_last)
    bot.send_message(msg.chat.id, menu_message, reply_markup=keyboard)
    #message.from_user.id

#=============================================
#1-ое Меню ввода данных, которое видит пользователь после нажатия "Внести запись"
# ВВОДИМ ДАТУ.
# тут будет две ветки - Текущая дата и время или Пользовательский ввод даты и времени
#=============================================
def _inpMenu1(message, menu_message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_curr_dt = types.KeyboardButton(text="Текущая дата и время")
    button_man_dt = types.KeyboardButton(text="Указать дату и время (ПОКА НЕ ПАШЕТ")
    button_reset = types.KeyboardButton(text="Сброс и возврат")
    keyboard.add(button_curr_dt, button_man_dt, button_reset)
    bot.send_message(message.chat.id, menu_message, reply_markup=keyboard)

#=============================================
#меню возврата
#=============================================
def _resetMenu(message, menu_message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_reset = types.KeyboardButton(text="Сброс и возврат")
    keyboard.add(button_reset)
    bot.send_message(message.chat.id, menu_message, reply_markup=keyboard)

#=============================================
'''пробую сохранять показания крови через класс, что кажется мне очень громоздким...'''
'''может создавать класс по сиквенсу и ему уже присваивать атрибуты? а потом инсертить все вместе? '''
#=============================================
class GetData:
    def __init__(self, user_id):
        self.user_id = user_id
        self.blood = None
        self.time = None
        self.date = None
        self.he = None
        self.insulin = None


#==========================================================
'''===================== MAIN =========================='''
#==========================================================


#основное меню, которое бот показывает при первом знакомстве.

@bot.message_handler(commands=['start'])
def start_message(message):
    menu_message = 'Привет, это бот, помогающий вести дневник самоконтроля.'
    _mainMenu(message, menu_message)


#DB создана 02/10/2019 на сервере скриптом Sugar_DB.py
@bot.message_handler(commands=['test'])
def test_message(message):
    menu_message = message.date
    user = GetData(message.from_user.id)
    bot.send_message(message.chat.id, user.user_id)
    bot.send_message(message.chat.id, datetime.fromtimestamp(menu_message).strftime('%d.%m.%Y'))
    bot.send_message(message.chat.id, datetime.fromtimestamp(menu_message).strftime('%H:%M'))



'''

После нажатия кнопки меню автоматически отправляется сообщение боту от пользователя
В зависимости от сообщения (ЧИТАЙ ОТ ВЫБРАННОГО ПУНКТА МЕНЮ) срабатывает определенный IF

'''
@bot.message_handler(content_types=["text"])
def input_record(message):
    if message.text == 'Внести запись':
        menu_message = 'Дата и время'
        _inpMenu1(message, menu_message)
    elif message.text == 'Текущая дата и время':
# Не нравится мне этот IF ELIF.. Надо как-нибудь запилить через БД типа на каком уровне меню пользователь
        inp_msg = 'Текущая дата и время'
        _resetMenu(message, inp_msg)
        inp_msg = bot.send_message(message.chat.id,'Введи значение глюкозы в виде числа.')
#next_step_handler запускает указанную функцию и ждет пользовательского ввода
        bot.register_next_step_handler(inp_msg, _glinput)
    elif message.text == 'Создать отчет':
#Можно сделать проверку, если записей в БД нет, то выводи об этом сообщение. Без try бот вообще падал на этом месте
        try:
            SugarSelect(message.from_user.id)
            file = open(str(message.from_user.id) + '.txt', 'rb')
            bot.send_document(message.chat.id, file)

            #bot.send_message(message.chat.id, SugarSelect())
        except Exception as e:
            bot.reply_to(message, 'oooops')

    else:
        menu_message = 'Основное меню'
        _mainMenu(message, menu_message)

# сначала вводим показания глюкозы'''
def _glinput(message):
    blood = message.text
    chat_id = message.chat.id

# тут же делаем кнопку возврата в основное меню '''
    if message.text == 'Сброс и возврат':
        menu_message = 'Основное меню'
        _mainMenu(message, menu_message)

# проверяем, что введено число '''
    elif not blood.replace(',','',1).replace('.','',1).isdigit():
        inp_msg = bot.send_message(message.chat.id, 'Введи число через точку!')
        bot.register_next_step_handler(inp_msg, _glinput)
    else:
        user = GetData(message.from_user.id)
        user_dict[chat_id] = user
        user.blood = blood
# сохраняем показатели глюкозы и юзер айди в класс и переходим к инсулину
        inp_msg = bot.send_message(message.chat.id, 'Укажи кол-во инсулина, если собираешься его вводить')
        bot.register_next_step_handler(inp_msg, _insulininput)


def _insulininput(message):
    insulin = message.text
    chat_id = message.chat.id
    if message.text == 'Сброс и возврат':
        menu_message = 'Основное меню'
        _mainMenu(message, menu_message)
    elif not insulin.replace(',','',1).replace('.','',1).isdigit():
        inp_msg = bot.send_message(message.chat.id, 'Введи число через точку!')
        bot.register_next_step_handler(inp_msg, _insulininput)
    else:
        user = user_dict[chat_id]
        user.insulin = insulin
 # сохраняем показатели инсулина и переходим к ХЕ
        inp_msg = bot.send_message(message.chat.id, 'Введи количество углеводов или ХЕ')
        bot.register_next_step_handler(inp_msg, _heinput)


def _heinput(message):
    he = message.text
    chat_id = message.chat.id
    if message.text == 'Сброс и возврат':
        menu_message = 'Основное меню'
        _mainMenu(message, menu_message)
    elif not he.replace(',','',1).replace('.','',1).isdigit():
        inp_msg = bot.send_message(message.chat.id, 'Введи число через точку!')
        bot.register_next_step_handler(inp_msg, _heinput)
    else:
        user = user_dict[chat_id]
        user.he = he
# сохраняем ХЕ/углеводы, так же записываем дату, время
        user.date = datetime.fromtimestamp(message.date).strftime('%d.%m.%Y')
        user.time = datetime.fromtimestamp(message.date).strftime('%H:%M')

#присваиваем данные переменным, которые потом будут использоваться в инсерте в БД
# не вижу смысл тут делать класс, можно просто переменными обойтись
        user_id = user.user_id
        date = user.date
        time = user.time
        sugar = round(float(user.blood)*1.12,2)
        insulin = user.insulin
        he = user.he
# Запускаем функцию по инсерту в БД, уведомляем пользователя, что все прошло успешно и возвращаемся в основное меню
        SugarInsert(user_id, date, time, sugar, insulin, he)
        bot.send_message(message.chat.id, 'Saved')
        menu_message = 'Основное меню'
        _mainMenu(message, menu_message)


bot.polling()