# -*- coding: utf-8 -*-
import telebot
from telebot import types

bot = telebot.TeleBot('5979986889:AAHbxQv1xLf0QncYBQUh25Z4NTeAXNjOHPQ')

@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Помощь")
    markup.add(btn1)
    bot.send_message(m.chat.id, 'Добро пожаловать в телеграм бот ITIS Request', reply_markup=markup)
    bot.send_message(m.chat.id, 'Здесь публикуются все объявления о наборе помощников для организаторов (культорг, спорторг, профорг, инфорг, соцорг, научорг, организатор волонтёров)')
    bot.send_message(m.chat.id, 'Немножечко о балловой системе \nОБЩАЯ ИНФОРМАЦИЯ: \n— Каждый семестр студенты могут получить дополнительные баллы за участие в мероприятиях и событиях студенческой жизни. \nДополнительные баллы являются частью общего рейтинга на заселение у иногородних студентов. Помимо этого, их можно добавить к академическим баллам по некоторым предметам. \n— Все активности оцениваются в соответствии с регламентом дополнительных баллов: https://docs.google.com/document/d/1QTSgofEYUjkWy6ALJ. \n— Свои текущие баллы можно посмотреть здесь: https://docs.google.com/spreadsheets/d/1qPCCiMbWs1EZa.')


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


bot.polling(none_stop=True, interval=0)
