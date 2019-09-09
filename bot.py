import os
import telebot

token=os.environ.get('Bot-token')
bot = telebot.TeleBot(str(token))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Привет! Стартанули!")

@bot.message_handler(content_types=['text'])
def function_name(message):
	bot.send_message(message.chat.id, "Наконец-то простое сообщение!")


bot.polling()