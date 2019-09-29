from zeep import Client
from zeep import xsd
from zeep.settings import Settings



def getRpoInfo(Barcode):		
	url = 'https://tracking.russianpost.ru/rtm34?wsdl'
	settings=Settings(strict=False, xml_huge_tree=True)
	client = Client(url, settings=settings)

	barcode=str(Barcode)
	print("Вы ввели: " + barcode)

	my_login = 'WZEZAUZbZZZpeK' # логин
	my_password = 'Rpyh80CTsbrH' #пароль

	#pprint(my_login + ' ' + my_password)

	result=client.service.getOperationHistory(
	  OperationHistoryRequest={'Barcode' : barcode, 'MessageType' : 0},
	  AuthorizationHeader={'login': my_login, 'password' : my_password} )
	#pprint(result)
	
	myans=''

	for rec in result:
		myans += '\n' + (str(rec.OperationParameters.OperDate) + ', ' + rec.AddressParameters.OperationAddress.Description + ', ' + rec.OperationParameters.OperAttr.Name)
		
	return myans
	