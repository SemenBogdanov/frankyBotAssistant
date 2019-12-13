from zeep import Client
from zeep import xsd
from zeep.settings import Settings
import os

def getRpoInfo(Barcode):		
	url = 'https://tracking.russianpost.ru/rtm34?wsdl'
	settings=Settings(strict=False, xml_huge_tree=True)
	client = Client(url, settings=settings)

	barcode=str(Barcode)
	print("Вы ввели: " + barcode)
	
	my_login = os.environ.get('RPO_LOGIN') # логин
	my_password = os.environ.get('RPO_PASS') #пароль

	#pprint(my_login + ' ' + my_password)

	result=client.service.getOperationHistory(
	  OperationHistoryRequest={'Barcode' : barcode, 'MessageType' : 0},
	  AuthorizationHeader={'login': my_login, 'password' : my_password} )
	#pprint(result)
	
	myans=''

	for rec in result:
		myans += '\n' + (str(rec.OperationParameters.OperDate) + ', ' + rec.AddressParameters.OperationAddress.Description + ', ' + rec.OperationParameters.OperAttr.Name)
		
	return myans

def get_Rpo(call, bot):
	msg=bot.send_message(call.message.chat.id, "Введите номер отправления:")
	#bot.send_message(call.message.chat.id, bot)
	bot.register_next_step_handler(msg, lambda m: get_Rpo2(m, bot))

def get_Rpo2(msg):
	bot.send_message(msg.chat.id, 'Получен номер ' + str(msg.text))
	bot.send_message(msg.chat.id, 'Спрашиваю у почты...')
	try:
	    answer=getRpoInfo(msg.text)
	    bot.send_message(msg.chat.id, 'Вот что удалось найти:')
	    bot.send_message(msg.chat.id, answer)
	    return answer
	except Exception as e:
	    return ("Такого отправления в системе Почты России нет!")
	#bot.send_message(msg.chat.id, answer)
	
