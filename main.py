# -*- coding: utf-8 -*-
import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot('5979986889:AAHbxQv1xLf0QncYBQUh25Z4NTeAXNjOHPQ')


@bot.message_handler(commands=["start"])
def start(message):
    start_message = "Добро пожаловать в Itis-Requset Bot!\n"
    start_message += "Чтобы посмотреть доступные команды и узнать больше о боте нажми /help\n"
    bot.send_message(message.chat.id, start_message)


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
    conn = sqlite3.connect('BotUsers.db', check_same_thread=False)
    cursor = conn.cursor()

    # Create a table to store user information
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

    # Check if the user is already registered
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    existing_user = cursor.fetchone()

    if existing_user:
        bot.reply_to(message, "Вы уже зарегистрировались!")
    else:
        # Prompt the user to provide their full name
        bot.reply_to(message, "Введите своё ФИО:")
        bot.register_next_step_handler(message, process_full_name, conn, user_id)


def process_full_name(message, conn, user_id):
    # Store the full name in a variable, accounting for possible commas
    full_name = message.text.strip()

    # Prompt the user to provide their group number
    bot.send_message(message.chat.id, "Введите номер группы:")
    bot.register_next_step_handler(message, process_group_number, conn, user_id, full_name)


def process_group_number(message, conn, user_id, full_name):
    # Store the group number in a variable, accounting for possible commas
    group_number = message.text.strip()

    # Prompt the user to provide their Telegram link
    bot.send_message(message.chat.id, "Введите свой tg")
    bot.register_next_step_handler(message, process_telegram_link, conn, user_id, full_name, group_number)


def process_telegram_link(message, conn, user_id, full_name, group_number):
    conn = sqlite3.connect('BotUsers.db', check_same_thread=False)
    cursor = conn.cursor()
    # Store the Telegram link in a variable, accounting for possible commas
    telegram_link = message.text.strip()

    # Check if the user should be assigned admin privileges
    is_admin = 1 if user_id in [5024477516] else 0  # Replace with your desired user IDs

    # Insert user information into the database
    cursor.execute('INSERT INTO users (user_id, full_name, group_number, telegram_link, is_admin) '
                   'VALUES (?, ?, ?, ?, ?)',
                   (user_id, full_name, group_number, telegram_link, is_admin))
    conn.commit()

    # Send a confirmation message
    bot.reply_to(message, f"Регистрация завершена! Добро пожаловать, {full_name}!")

    # Если админ, то отправляем
    if is_admin:
        bot.send_message(message.chat.id, "Вам предоставлены права администратора!")


connection = sqlite3.connect('Events.db')
cursorr = connection.cursor()

# Create a table to store event information
cursorr.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        location TEXT,
        time TEXT,
        date TEXT,
        seats INTEGER,
        points INTEGER
    )
''')
connection.commit()


@bot.message_handler(commands=['new'])
def create_event(message):
    conn = sqlite3.connect('BotUsers.db')
    cursor = conn.cursor()
    # Check if the user is an administrator
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE user_id=? AND is_admin=1', (user_id,))
    admin_user = cursor.fetchone()

    #if admin_user:
        # Prompt the administrator to provide event details
    bot.reply_to(message, "Пожалуйста, опишите своё мероприятие:")
    bot.register_next_step_handler(message, process_event_details)
    #else:
    #bot.reply_to(message, "Вы не обладаете правами администратора")


def process_event_details(message):
    # Store event details in variables
    event_name = message.text.strip()

    bot.send_message(message.chat.id, "Наазвание события:")
    bot.register_next_step_handler(message, process_event_description, event_name)


def process_event_description(message, event_name):
    event_description = message.text.strip()

    bot.send_message(message.chat.id, "Место проведения:")
    bot.register_next_step_handler(message, process_event_location, event_name, event_description)


def process_event_location(message, event_name, event_description):
    event_location = message.text.strip()

    bot.send_message(message.chat.id, "Время проведения:")
    bot.register_next_step_handler(message, process_event_time, event_name, event_description, event_location)


def process_event_time(message, event_name, event_description, event_location):
    event_time = message.text.strip()

    bot.send_message(message.chat.id, "Дата проведения:")
    bot.register_next_step_handler(message, process_event_date, event_name, event_description, event_location, event_time)


def process_event_date(message, event_name, event_description, event_location, event_time):
    event_date = message.text.strip()

    bot.send_message(message.chat.id, "Количество доступных мест:")
    bot.register_next_step_handler(message, process_event_seats, event_name, event_description, event_location, event_time,
                                   event_date)


def process_event_seats(message, event_name, event_description, event_location, event_time, event_date):
    try:
        event_seats = int(message.text.strip())

        bot.send_message(message.chat.id, "Количество баллов зв мероприятие:")
        bot.register_next_step_handler(message, process_event_points, event_name, event_description, event_location,
                                       event_time, event_date, event_seats)
    except ValueError:
        bot.send_message(message.chat.id, "Неправильный ввод, пожалуйста указывайте корректное число.")


def process_event_points(message, event_name, event_description, event_location, event_time, event_date, event_seats):
    try:
        event_points = int(message.text.strip())
        conn = sqlite3.connect('Events.db')
        cursor = conn.cursor()
        # Insert event details into the database
        cursor.execute('INSERT INTO events (name, description, location, time, date, seats, points) '
                       'VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (event_name, event_description, event_location, event_time, event_date, event_seats,
                        event_points))
        conn.commit()

        bot.send_message(message.chat.id, "Событие создано!")
    except ValueError:
        bot.send_message(message.chat.id, "Invalid input. Please enter a valid number of points.")

@bot.message_handler(commands=['show'])
def show_events(message):
    # Create a new connection and cursor for each thread
    conn = sqlite3.connect('BotUsers.db')
    cursor = conn.cursor()

    # Retrieve the available events from the database
    cursorr.execute('SELECT * FROM events')
    events = cursorr.fetchall()

    if events:
        event_message = "Available events:\n\n"
        for event in events:
            event_message += f"Name: {event[1]}\n"
            event_message += f"Description: {event[2]}\n"
            event_message += f"Location: {event[3]}\n"
            event_message += f"Time: {event[4]}\n"
            event_message += f"Date: {event[5]}\n"
            event_message += f"Seats: {event[6]}\n"
            event_message += f"Points: {event[7]}\n"
            event_message += "------------------------\n"
    else:
        event_message = "No events available."

    bot.send_message(message.chat.id, event_message)

    # Close the connection
    conn.close()


bot.polling(none_stop=True, interval=0)
