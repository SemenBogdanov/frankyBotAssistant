import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import rpoInfo
import db
from pycbrf import ExchangeRates, Banks
import datetime

global functions, coffee
functions = ("функции","функция", "функций","функц")

token=os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(str(token))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	#Проверка пользователя на знакомство
	res=db.checkUser(message.chat.id)
	if len(res)<= 0:
		answer=bot.send_message(message.chat.id, "Привет, давай знакомиться! Как тебя зовут?")
		bot.register_next_step_handler(answer, addUserToDb)
	else:
		bot.send_message(message.chat.id, 'Привет, мой друг '+res[0][0]+'!')
		bot.send_message(message.chat.id, "Вот что я могу!", reply_markup=welcome_func())

def rates(call):
	dt=datetime.datetime.now().strftime("%Y-%m-%d")
	r=ExchangeRates(dt, locale_en=True)
	try:
		#print(r)
		answer="По состоянию на " + dt + ", 1 USD = " + str(r['USD'].value) + " руб. \nПо состоянию на " + dt + ", 1 EUR = " + str(r['EUR'].value) + " руб.""
		bot.send_message(call.message.chat.id, answer)
	except a as Exception:
		bot.send_message(call.message.chat.id, a)

def addUserToDb(answer):
	res=db.addUser(answer)
	if res:
		bot.send_message(answer.chat.id, "Теперь мы знакомы")
	else:
		bot.send_message(answer.chat.id, "Неудачная попытка тебя запомнить, нажми /start еще раз!")
		send_welcome(answer)

def recVoc(msg):
	#file=open('vocablulary.txt', a)
	bot.send_message(msg.chat.id, msg.text)

def programming_voc(call):
	bot.answer_callback_query(call.id, "запрограммировать словарь") 
	msg=bot.send_message(call.message.chat.id, "Введите сообщение для записи:")
	bot.register_next_step_handler(msg, recVoc)
	#

def get_coffee_place(call):
	bot.answer_callback_query(call.id, "Посоветовать кофейню!")
	'''не работает
	file=open('descCoffee.txt')
	cid=call.message.chat.id
	t=file.read()
	bot.send_message(cid, t)
	bot.send_message(cid, "Может что-нибудь ещё?", reply_markup=welcome_func())
	file.close()
	#return t
	pass
	'''

def welcome_func():
	markup=InlineKeyboardMarkup()
	markup.row_width=3
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
			rpoInfo.get_Rpo(call,bot)
		except Exception as e:
			bot.send_message(call.message.chat.id, "Неуспешная попытка: " + str(e))

@bot.message_handler(content_types=['text'])
def function_name(message):
	bot.send_message(message.chat.id, "Вот что я могу!", reply_markup=welcome_func())

print("бот запущен!")

bot.polling() 
