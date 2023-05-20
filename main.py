# -*- coding: utf-8 -*-
import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot('5979986889:AAHbxQv1xLf0QncYBQUh25Z4NTeAXNjOHPQ')


@bot.message_handler(commands=["start"])
def start(message):
    start_message = "Добро пожаловать в Itis-Requset Bot!\n"
    start_message += "Чтобы посмотреть доступные команды и узнать больше о боте нажми /help\n"
    bot.send_message(message.chat.id,start_message)


@bot.message_handler(commands=['help'])
def send_help(message):
    help_message = "Добро пожаловать в помощь!\n\n"
    help_message += "Доступные команды:\n"
    help_message += "/help - Отобразить доступные команды и контакты организаторов, немного о баллах\n"
    help_message += "/show - Показать доступные мероприятия\n"
    help_message += "/new - Создать новое событие\n"
    help_message += "/register - Зарегистрироваться (нужно для записи на мероприятие)\n\n"
    help_message += "Общая информация:\n"
    help_message += "— Каждый семестр студенты могут получить дополнительные \n"
    help_message += "баллы за участие в мероприятиях и событиях студенческой жизни.\n"
    help_message += "— Дополнительные баллы являются частью общего рейтинга на заселение у иногородних студентов. Помимо этого, их можно \n"
    help_message += "добавить к академическим баллам по некоторым предметам.\n"
    help_message += "— Все активности оцениваются в соответствии с регламентом дополнительных баллов:\n"
    help_message += "https://docs.google.com/document/d/1QTSgofEYUjkWy6ALJ.\n\n"
    help_message += "Если вам нужна помощь, пожалуйста, напишите организаторам мероприятия:\n"
    help_message += "Сергей Бабич : Председатель Студсовета - https://vk.com/kreomanser\n"
    help_message += "Александра Кузнецова : Профорг - https://vk.com/alekscscs\n"
    help_message += "Аня Будревич : Культорг - https://vk.com/ann_utochkka\n"
    help_message += "Кирилл Ефремов : Спорторг - https://vk.com/kirillefremov45\n"
    help_message += "Елизавета Мухортова : Руководитель Медиацентра - https://vk.com/lr_107\n"
    help_message += "Валентин Грачёв : Научорг - https://vk.com/valentin_grachyov\n"
    help_message += "Rumiya Salakhova :  Организатор Волонтеров - https://vk.com/angel277\n"
    help_message += "Дмитрий Сметанин : Руководитель Отдела Безопасности - https://vk.com/dmitriysmetanin\n"
    help_message += "Андрей Осин : Руководитель Антикоррупционного направления - https://vk.com/h8m3_3\n"

    bot.send_message(message.chat.id, help_message)


@bot.message_handler(commands=['register'])
def register_user(message):
    conn = sqlite3.connect('BotUsers.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER,
            full_name TEXT,
            group_number TEXT,
            telegram_link TEXT,
            is_admin INTEGER
        )
    ''')
    conn.commit()

    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        bot.reply_to(message, "Вы уже зарегистрировались!")
    else:
        bot.reply_to(message, "Введите своё ФИО:")
        bot.register_next_step_handler(message, process_full_name, user_id)


def process_full_name(message, chat_id):
    full_name = message.text.strip()

    bot.send_message(chat_id, "Введите номер группы:")
    bot.register_next_step_handler(message, process_group_number, chat_id, full_name)


def process_group_number(message, chat_id, full_name):
    group_number = message.text.strip()

    bot.send_message(chat_id, "Введите свой tg")
    bot.register_next_step_handler(message, process_telegram_link, chat_id, full_name, group_number)


def process_telegram_link(message, chat_id, full_name, group_number):

    conn = sqlite3.connect('BotUsers.db')
    cursor = conn.cursor()

    telegram_link = message.text.strip()
    user_id = message.from_user.id
    is_admin = 1 if user_id in [123456789] else 0  # Нужно заменить на ID админов

    cursor.execute('INSERT INTO users (user_id, full_name, group_number, telegram_link, is_admin) '
                   'VALUES ( ?, ?, ?, ?, ?)',
                   (user_id, full_name, group_number, telegram_link, is_admin))
    conn.commit()

    
    bot.reply_to(message, f"Регистрация завершена! Добро пожаловать, {full_name}!")

    if is_admin:
        bot.send_message(chat_id, "Вам предоставлены права администратора!")


bot.polling(none_stop=True, interval=0)
