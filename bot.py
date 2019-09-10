import os
import telebot

token=os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(str(token))

greetings='''Привет! Ну что? Поехали по-тихонечку?!
меня зовут Фрэнк! Рад буду напоминать тебе о том, что ты всегда забывал. 
А когда мой разработчик добавит мне базу данных для памяти, я вообще буду крут!
Как тебя зовут?'''

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, greetings)

@bot.message_handler(content_types=['text'])
def function_name(message):
	bot.send_message(message.chat.id, "Наконец-то простое сообщение!")


bot.polling()
