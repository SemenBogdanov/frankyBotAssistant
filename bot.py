import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

global functions, coffee
functions = ("функции","функция", "функций","функц")

token=os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(str(token))

greetings='''Привет! Ну что? Поехали по-тихонечку?!
меня зовут Фрэнк! Рад буду напоминать тебе о том, что ты всегда забывал. 
А когда мой разработчик добавит мне базу данных для памяти, я вообще буду крут!
Как тебя зовут?'''

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, greetings)

def welcome_func(chat_id):
	markup=InlineKeyboardMarkup()
	markup.row_width=4
	markup.add(InlineKeyboardButton("Посоветовать хорошую кофейню", callback_data="get_coffee_place"))
	markup.add(InlineKeyboardButton("Погода", callback_data="get_weather"),
		InlineKeyboardButton("Курс валют", callback_data="course_exchange"))
	markup.add(InlineKeyboardButton("Запрограммировать словарь", callback_data="programming_voc"))
	return markup



@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "get_weather":
        bot.answer_callback_query(call.id, "выбрана погода")
    elif call.data == "get_coffee_place":
        bot.answer_callback_query(call.id, "ДаркСайд")
    elif call.data == "course_exchange":
        bot.answer_callback_query(call.id, "выбран курс валют")
    elif call.data == "programming_voc":
        bot.answer_callback_query(call.id, "запрограммировать словарь")  

@bot.message_handler(content_types=['text'])
def function_name(message):
	for i in range(len(functions)):
		if functions[i] in message.text:
			bot.send_message(message.chat.id, "Вот что я могу!", reply_markup=welcome_func(message.chat.id))
			return;
		else :
			continue	
	i+=1
	bot.send_message(message.chat.id, "Попробуй спросить меня о функциях!")


bot.polling()
