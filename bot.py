import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import rpoInfo
import db
from pycbrf import ExchangeRates, Banks
import datetime
import requests
import json
import time

global functions, coffee

token = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(str(token))
ya_id = os.environ.get('Yandex_API_KEY')


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    # Проверка пользователя на знакомство
    res = db.checkUser(message.chat.id)
    if len(res) <= 0:
        answer = bot.send_message(message.chat.id, "Привет, давай знакомиться! Как тебя зовут?")
        bot.register_next_step_handler(answer, addUserToDb)
    else:
        bot.send_message(message.chat.id, 'Привет, мой друг ' + res[0][0] + '!')
        bot.send_message(message.chat.id, "Вот что я могу!", reply_markup=welcome_func())


def rates(call):
    dt = datetime.datetime.now().strftime("%Y-%m-%d")
    r = ExchangeRates(dt, locale_en=True)
    try:
        # print(r)
        answer = "По состоянию на " + dt + ": \n 1 USD = " + \
                 str(r['USD'].value) + " руб. \n " \
                 + "1 EUR = " + str(r['EUR'].value) + " руб."
        bot.send_message(call.message.chat.id, answer)
    except Exception as a:
        bot.send_message(call.message.chat.id, a)


def addUserToDb(answer):
    res = db.addUser(answer)
    if res:
        bot.send_message(answer.chat.id, "Теперь мы знакомы")
    else:
        bot.send_message(answer.chat.id, "Неудачная попытка тебя запомнить, нажми /start еще раз!")
        send_welcome(answer)


def recVoc(msg):
    # file=open('vocablulary.txt', a)
    bot.send_message(msg.chat.id, msg.text)


def programming_voc(call):
    bot.answer_callback_query(call.id, "запрограммировать словарь")
    msg = bot.send_message(call.message.chat.id, "Введите сообщение для записи:")
    bot.register_next_step_handler(msg, recVoc)


def getyandexweather(call):
    #url = 'https://api.weather.yandex.ru/v1/informers'
    url = 'https://api.weather.yandex.ru/v1/forecast/'
    h = {"X-Yandex-API-Key": ya_id}
    p = {"lat": "47.222078", "lon": "39.720349"}
    weather_json = requests.get(url, params=p, headers=h)
    weather = json.loads(weather_json.text)
    cur_now = time.ctime(weather['now'])
    cdt = time.strptime(cur_now, "%a %b %d %H:%M:%S %Y")
    td = str(cdt.tm_mday) + '.' + str(cdt.tm_mon) + '.' + str(cdt.tm_year)
    season_d = {"winter": "Зима", "summer": "Лето"}
    cond ={"clear":"ясно",
          "partly-cloudy": "малооблачно",
          "cloudy": "облачно с прояснениями",
          "overcast": "пасмурно",
          "partly-cloudy-and-light-rain": "небольшой дождь",
          "partly-cloudy-and-rain": "дождь",
          "overcast-and-rain": "сильный дождь",
          "overcast-thunderstorms-with-rain": "сильный дождь и гроза",
          "cloudy-and-light-rain": "небольшой дождь",
          "overcast-and-light-rain": "небольшой дождь",
          "cloudy-and-rain": "дождь",
          "overcast-and-wet-snow": "дождь со снегом",
          "partly-cloudy-and-light-snow": "небольшой снег",
          "partly-cloudy-and-snow": "снег",
          "overcast-and-snow": "снегопад",
          "cloudy-and-light-snow": "небольшой снег",
          "overcast-and-light-snow": "небольшой снег",
          "cloudy-and-snow": "Облачно и снег"}
    answerWeatherAbout = "Сегодня на " + td + ", по данным Яндекс.Погода в Ростове-на-Дону: \n" \
                        "Температура воздуха: " + str(weather['fact']['temp']) + " градусов и ощущается как " \
                        + str(weather['fact']['feels_like']) + ", давление " \
                        + str(weather['fact']['pressure_mm']) + " мм.рт.ст., влажность " \
                        + str(weather['fact']['humidity']) + "%. " \
                        + "Ветер " + str(weather['fact']['wind_dir']) + ", скорость " \
                        + str(weather['fact']['wind_speed']) + "м/с, с порывами до " \
                        + str(weather['fact']['wind_gust']) + "м/с. Условия: " \
                        + cond[str(weather['fact']['condition'])] + ". Сейчас " + season_d[str(weather['fact']['season'])] \
                        + "."
    bot.send_message(call.message.chat.id, answerWeatherAbout)

def get_coffee_place(call):
    bot.answer_callback_query(call.id, "Посоветовать кофейню!")


def welcome_func():
    markup = InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(InlineKeyboardButton("Посоветовать хорошую кофейню!",
                                    callback_data="get_coffee_place"))
    markup.add(InlineKeyboardButton("Погода", callback_data="get_weather"),
               InlineKeyboardButton("Курс валют", callback_data="course_exchange"))
    markup.add(InlineKeyboardButton("Добавить день рождение", callback_data="course_exchange"))
    markup.add(InlineKeyboardButton("Дни рождения сегодня", callback_data="course_exchange"))
    markup.add(InlineKeyboardButton("Дни рождения в ближайший месяц", callback_data="course_exchange"))
    markup.add(InlineKeyboardButton("Отслеживание ПочтаРоссии", callback_data="get_Rpo"))
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_weather":
        getyandexweather(call)
        bot.answer_callback_query(call.id, "Выбрана погода")
    elif call.data == "get_coffee_place":
        get_coffee_place(call)
    elif call.data == "course_exchange":
        rates(call)
    elif call.data == "programming_voc":
        programming_voc(call)
    elif call.data == "get_Rpo":
        try:
            bot.send_message(call.message.chat.id, "Попытка вызвать функцию отслеживания!")
            rpoInfo.get_Rpo(call, bot)
        except Exception as e:
            bot.send_message(call.message.chat.id, "Неуспешная попытка: " + str(e))


@bot.message_handler(content_types=['text'])
def function_name(message):
    bot.send_message(message.chat.id, "Вот что я могу!", reply_markup=welcome_func())


print("бот запущен!")

bot.polling()
