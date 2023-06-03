# -*- coding: utf-8 -*-
import sqlite3
import telebot
from telebot import types

bot = telebot.TeleBot('5979986889:AAF9ClFzv_F4k7M1Z_34vbqFmzsvAOV0psk')

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
    help_message += "/new - Создать новое событие (только для админов)\n"
    help_message += "/delete - Удалить событие (только для админов)\n"
    help_message += "/register - Зарегистрироваться (нужно для записи на мероприятие)\n"
    help_message += "/myevents - Посмотреть события, на которые я записался\n"
    help_message += "/showeventmembers - Посмотреть список участников мероприятия (только для админов)\n\n"
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
        bot.register_next_step_handler(message, process_full_name, conn, user_id)


def process_full_name(message, conn, user_id):
    full_name = message.text.strip()

    bot.send_message(message.chat.id, "Введите номер группы:")
    bot.register_next_step_handler(message, process_group_number, conn, user_id, full_name)


def process_group_number(message, conn, user_id, full_name):
    group_number = message.text.strip()

    bot.send_message(message.chat.id, "Введите свой tg")
    bot.register_next_step_handler(message, process_telegram_link, conn, user_id, full_name, group_number)


def process_telegram_link(message, conn, user_id, full_name, group_number):
    conn = sqlite3.connect('BotUsers.db', check_same_thread=False)
    cursor = conn.cursor()

    telegram_link = message.text.strip()

    is_admin = 1 if user_id in [5024477516] else 0  # Нужно потом заменить на id админов

    cursor.execute('INSERT INTO users (user_id, full_name, group_number, telegram_link, is_admin) '
                   'VALUES (?, ?, ?, ?, ?)',
                   (user_id, full_name, group_number, telegram_link, is_admin))
    conn.commit()

    bot.reply_to(message, f"Регистрация завершена! Добро пожаловать, {full_name}!")

    if is_admin:
        bot.send_message(message.chat.id, "Вам предоставлены права администратора!")


connection = sqlite3.connect('BotUsers.db', check_same_thread=False)
cursorr = connection.cursor()
#connection = sqlite3.connect('Events.db', check_same_thread=False)
#cursorr = connection.cursor()

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


cursorr.execute('''CREATE TABLE IF NOT EXISTS registrations
                (user_id INTEGER NOT NULL,
                 event_id INTEGER NOT NULL,
                 FOREIGN KEY(user_id) REFERENCES users(id),
                 FOREIGN KEY(event_id) REFERENCES events(id),
                 PRIMARY KEY (user_id, event_id))''')

connection.commit()

@bot.message_handler(commands=['new'])
def create_event(message):
    conn = sqlite3.connect('BotUsers.db', check_same_thread=False)
    cursor = conn.cursor()

    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE user_id=? AND is_admin=1', (user_id,))
    admin_user = cursor.fetchone()

    if admin_user:
        bot.reply_to(message, "Пожалуйста, опишите своё мероприятие:")
        bot.register_next_step_handler(message, process_event_details)
    else:
        bot.reply_to(message, "Вы не обладаете правами администратора")


def process_event_details(message):
    event_name = message.text.strip()

    bot.send_message(message.chat.id, "Название события:")
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
        conn = sqlite3.connect('BotUsers.db', check_same_thread=False)
        cursor = conn.cursor()
        #conn = sqlite3.connect('Events.db', check_same_thread=False)
        #cursor = conn.cursor()

        cursor.execute('INSERT INTO events (name, description, location, time, date, seats, points) '
                       'VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (event_name, event_description, event_location, event_time, event_date, event_seats,
                        event_points))
        conn.commit()

        bot.send_message(message.chat.id, "Событие создано!")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, вводите корректное количество баллов.")

# Delete ///////////////////////////////////////////////////////////////////////////////////////////////////
@bot.message_handler(commands=['delete'])
def delete_event(message):
    conn = sqlite3.connect('BotUsers.db', check_same_thread=False)
    cursor = conn.cursor()

    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE user_id=? AND is_admin=1', (user_id,))
    admin_user = cursor.fetchone()

    if admin_user:
        bot.reply_to(message, "Введите ID мероприятия, которое вы хотите удалить:")
        bot.register_next_step_handler(message, process_event_deletion)
    else:
        bot.reply_to(message, "Вы не обладаете правами администратора")


def process_event_deletion(message):
    event_id = message.text.strip()

    #connect= sqlite3.connect('Events.db', check_same_thread=False)
    #curs = connect.cursor()

    connect = sqlite3.connect('BotUsers.db', check_same_thread=False)
    curs = connect.cursor()

    curs.execute('SELECT * FROM events WHERE id=?', (event_id,))
    event = curs.fetchone()

    if event:
        curs.execute('DELETE FROM events WHERE id=?', (event_id,))
        connect.commit()

        bot.send_message(message.chat.id, f"Мероприятие с № {event_id} успешно удалено!")
    else:
        bot.send_message(message.chat.id, f"Мероприятия с № {event_id} не существует!")

    #conn.close()
    connect.close()
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

@bot.message_handler(commands=['show'])
def show_events(message):
    conn = sqlite3.connect('BotUsers.db', check_same_thread=False)
    cursor = conn.cursor()

    cursorr.execute('SELECT * FROM events')
    events = cursorr.fetchall()

    if events:
        event_message = "Доступные мероприятия:\n\n"
        for event in events:
            event_message = f"№: {event[0]}\n"
            event_message += f"Название: {event[1]}\n"
            event_message += f"Описание: {event[2]}\n"
            event_message += f"Место: {event[3]}\n"
            event_message += f"Время: {event[4]}\n"
            event_message += f"Дата: {event[5]}\n"
            event_message += f"Места: {event[6]}\n"
            event_message += f"Баллы: {event[7]}\n"
            event_message += "--------------------\n"

            cursor.execute('SELECT COUNT(*) FROM registrations WHERE event_id=?', (event[0],))
            registered_count = cursor.fetchone()[0]

            available_seats = event[6] - registered_count

            event_message += f"Доступные места: {available_seats}\n"

            apply_button = types.InlineKeyboardButton("Запиаться", callback_data=f"apply_{event[0]}")
            unsubscribe_button = types.InlineKeyboardButton("Отписаться", callback_data=f"unsubscribe_{event[0]}")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(apply_button, unsubscribe_button)

            bot.send_message(message.chat.id, event_message, reply_markup=keyboard)
    else:
        event_message = "Нет доступных событий."
        bot.send_message(message.chat.id, event_message)

    conn.close()


@bot.callback_query_handler(func=lambda call: call.data.startswith('apply_'))
def process_apply_callback(call):
    event_id = call.data.split('_')[1]
    user_id = call.from_user.id

    conn = sqlite3.connect('BotUsers.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS registrations
                    (user_id INTEGER NOT NULL,
                     event_id INTEGER NOT NULL,
                     FOREIGN KEY(user_id) REFERENCES users(id),
                     FOREIGN KEY(event_id) REFERENCES events(id),
                     PRIMARY KEY (user_id, event_id))''')

    cursor.execute('SELECT * FROM registrations WHERE user_id=? AND event_id=?', (user_id, event_id))
    existing_registration = cursor.fetchone()

    if existing_registration:
        bot.answer_callback_query(call.id, "Вы уже зарегистрированы на это мероприятие", show_alert=True)
    else:
        cursor.execute('INSERT INTO registrations (user_id, event_id) VALUES (?, ?)', (user_id, event_id))
        conn.commit()
        bot.answer_callback_query(call.id, "Вы успешно зарегистрированы на мероприятие", show_alert=True)

    conn.close()


@bot.callback_query_handler(func=lambda call: call.data.startswith('unsubscribe_'))
def process_unsubscribe_callback(call):
    event_id = call.data.split('_')[1]
    user_id = call.from_user.id

    conn = sqlite3.connect('BotUsers.db', check_same_thread=False)
    cursor = conn.cursor()

    cursor.execute('DELETE FROM registrations WHERE user_id=? AND event_id=?', (user_id, event_id))
    conn.commit()

    bot.answer_callback_query(call.id, "Вы успешно отписались от мероприятия", show_alert=True)

    conn.close()


# showEvents/////////////////////////////////////////////////////////////////////////////
@bot.message_handler(commands=['showeventmembers'])
def show_event_members(message):
    conn = sqlite3.connect('BotUsers.db', check_same_thread=False)
    cursor = conn.cursor()

    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE user_id=? AND is_admin=1', (user_id,))
    admin_user = cursor.fetchone()

    if admin_user:
        bot.reply_to(message, "Введите номер мероприятия:")
        bot.register_next_step_handler(message, process_event_members)
    else:
        bot.reply_to(message, "Вы не обладаете правами администратора")


def process_event_members(message):
    try:
        event_id = int(message.text.strip())
        conn = sqlite3.connect('BotUsers.db', check_same_thread=False)
        cursor = conn.cursor()

        cursorr.execute('SELECT * FROM events WHERE id=?', (event_id,))
        event = cursorr.fetchone()

        if event:
            cursor.execute('''
                SELECT u.full_name, u.group_number, u.telegram_link
                FROM users u
                JOIN registrations r ON u.user_id = r.user_id
                WHERE r.event_id = ?
            ''', (event_id,))
            members = cursor.fetchall()

            if members:
                members_message = f"Участники мероприятия \"{event[1]}\":\n\n"
                for member in members:
                    members_message += f"ФИО: {member[0]}\n"
                    members_message += f"Группа: {member[1]}\n"
                    members_message += f"Telegram: {member[2]}\n\n"
                    members_message += " \n\n"
                bot.send_message(message.chat.id, members_message)
            else:
                bot.send_message(message.chat.id, "На данное мероприятие нет зарегистрированных участников.")
        else:
            bot.send_message(message.chat.id, "Мероприятие с указанным ID не найдено.")
    except ValueError:
        bot.send_message(message.chat.id, "Неправильный ввод, пожалуйста, введите корректный ID мероприятия.")

@bot.message_handler(commands=['myevents'])
def show_user_events(message):
    conn = sqlite3.connect('BotUsers.db', check_same_thread=False)
    cursor = conn.cursor()

    user_id = message.from_user.id
    cursor.execute('SELECT events.id, events.name, events.location, events.time, events.date FROM events JOIN registrations ON events.id = registrations.event_id WHERE registrations.user_id=?', (user_id,))
    events = cursor.fetchall()

    if events:
        event_message = "События, на которые вы записаны:\n\n"
        for event in events:
            event_message += f"Название: {event[1]}\n"
            event_message += f"Место: {event[2]}\n"
            event_message += f"Время: {event[3]}\n"
            event_message += f"Дата: {event[4]}\n"
            event_message += "--------------------\n"

        bot.send_message(message.chat.id, event_message)
    else:
        event_message = "Вы не записаны на ни одно событие."
        bot.send_message(message.chat.id, event_message)

    conn.close()

bot.add_message_handler(show_event_members)


bot.polling(none_stop=True, interval=0)
