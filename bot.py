import telebot
import os

token=os.environ.get("Bot-token")
bot = telebot.TeleBot(str(token))

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")

#@bot.message_handler(func=lambda message: True)
#def echo_all(message):
#	bot.reply_to(message, message.text)

@bot.message_handler(func=lambda a:True)
def function_name(message):
	task=bot.get_me().id
	bot.send_message(task,"Наконец-то простое сообщение!")
	bot.reply_to(message, task)


bot.polling()