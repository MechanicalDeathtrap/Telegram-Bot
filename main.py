# -*- coding: utf-8 -*-
import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot('5979986889:AAHbxQv1xLf0QncYBQUh25Z4NTeAXNjOHPQ')
# не нравится
userName = None
userGroup = None
userTg = None

@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Помощь")
    btn2 = types.KeyboardButton("Зарегистрироваться")
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(m.chat.id, 'Добро пожаловать в телеграм бот ITIS Request', reply_markup=markup)
    bot.send_message(m.chat.id, 'Здесь публикуются все объявления о наборе помощников для организаторов '
                                '(культорг, спорторг, профорг, инфорг, соцорг, научорг, организатор волонтёров)')
    bot.send_message(m.chat.id, 'Немножечко о балловой системе '
                                '\nОБЩАЯ ИНФОРМАЦИЯ: '
                                '\n— Каждый семестр студенты могут получить дополнительные баллы за участие '
                                'в мероприятиях и событиях студенческой жизни. '
                                '\nДополнительные баллы являются частью общего рейтинга на заселение у иногородних '
                                'студентов. Помимо этого, их можно добавить к академическим баллам по некоторым предметам. '
                                '\n— Все активности оцениваются в соответствии с регламентом дополнительных баллов:'
                                ' https://docs.google.com/document/d/1QTSgofEYUjkWy6ALJ. '
                                '\n— Свои текущие баллы можно посмотреть здесь:'
                                ' https://docs.google.com/spreadsheets/d/1qPCCiMbWs1EZa.')


@bot.message_handler(content_types=['text'])
def get_text_messages(m):
    if m.text == 'Помощь':
        bot.send_message(m.chat.id, 'Если вам нужна помощь, пожалуйста, напишите организаторам мероприятия:')
        bot.send_message(m.chat.id, 'Сергей Бабич : Председатель Студсовета - https://vk.com/kreomanser')
        bot.send_message(m.chat.id, 'Александра : Кузнецова Профорг - https://vk.com/alekscscs')
        bot.send_message(m.chat.id, 'Аня Будревич : Культорг - https://vk.com/ann_utochkka')
        bot.send_message(m.chat.id, 'Кирилл Ефремов : Спорторг - https://vk.com/kirillefremov45')
        bot.send_message(m.chat.id, 'Елизавета Мухортова : Руководитель Медиацентра - https://vk.com/lr_107')
        bot.send_message(m.chat.id, 'Валентин Грачёв : Научорг - https://vk.com/valentin_grachyov')
        bot.send_message(m.chat.id, 'Rumiya Salakhova :  Организатор Волонтеров - https://vk.com/angel277')
        bot.send_message(m.chat.id, 'Дмитрий Сметанин : Руководитель Отдела Безопасности - https://vk.com/dmitriysmetanin')
        bot.send_message(m.chat.id, 'Андрей Осин : Руководитель Антикоррупционного направления - https://vk.com/h8m3_3')

    if m.text == 'Зарегистрироваться':
        # создание файла бдшки
        connection = sqlite3.connect('Users.sql')

        # через курсор выполняем команды бдшки
        cursor = connection.cursor()

        # подготавливаем команду для создания таблицы бд с полями group name telegLink если она ещё не существует
        cursor.execute('CREATE TABLE IF NOT EXISTS users '
                       '(id int auto_increment primary key,'
                       ' name varchar(60),'
                       ' uGroup varchar(6),'
                       ' tLink varchar(20))')

        # создаём таблицу и добавляем ее в файл с бд
        connection.commit()

        # закрывем соединение
        cursor.close()
        connection.close()

        bot.send_message(m.chat.id, 'Привет! Для регистрации введи своё ФИО ')
        bot.register_next_step_handler(m, user_name)


def user_name(m):
    global userName
    userName = m.text.strip()
    bot.send_message(m.chat.id, 'Ещё номер группы ) ')
    bot.register_next_step_handler(m, user_group)

def user_group(m):
    global userGroup
    userGroup = m.text.strip()
    bot.send_message(m.chat.id, 'Ну и напоследок твой tg ')
    bot.register_next_step_handler(m, user_tg)

def user_tg(m):
    global userTg
    userTg = m.text.strip()

    connection = sqlite3.connect('Users.sql')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO users (name , uGroup , tLink) '
                   'VALUES ("%s" , "%s", "%s" )' % (userName, userGroup, userTg))
    connection.commit()
    cursor.close()
    connection.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardMarkup("Users", callback_data = 'list'))

    bot.send_message(m.chat.id, f" Поздравляю ,{userName}, вы зарегистрированы!)", reply_markup= markup )

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    connection = sqlite3.connect('Users.sql')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    info =''
    for item in users:
        info+= f"Name :{item[1]}, group:{item[2]}, tg:{item[3]}\n"

    cursor.close()
    connection.close()
    bot.send_message(call.m.chat.id, info)

bot.polling(none_stop=True, interval=0)
