import telebot
import os

token=os.environ.get('Bottoken')
bot = telebot.TeleBot(str(token))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет! Стартанули!")

@bot.message_handler(context_type=[text])
def function_name(message):
	bot.send_message(message.chat.id,"Наконец-то простое сообщение!")
	
bot.polling()
