

class SegnalazioneImage:
	
	__file = None
	
	def __init__(self, filename):
		self.__file = filename
		pass
		

	def getFilename(self):
		return self.__file


class Segnalazione:
	
	__info = {
		"id": None,
		"phone_number": None,
		"phone_user": None,
		"date": None,
		"time": None,
		"text": "",
		"images": [],
		"position": {
			"latitude": 0,
			"longitude": 0
		},
	}
	
	__status = None
	
	def __init__(self):
		pass
		
	def save(self):
		# save data to DB
		pass
		
	def getStatus(self):
		return self.__status
		
	def setStatus(self, status):
		self.__status = status

	def getInfo(self):
		return self.__info
		
	def setInfo(self, param, value):
		if param in self.__info.keys():
			self.__info[param] = value
		else:
			raise NameError("parametro non valido")
			
	def addImage(self, si: SegnalazioneImage):
		if not isinstance(si, SegnalazioneImage):
			raise NameError("si non e' un tipo SegnalazioneImage valido")
		self.__info["images"].append(si)
		pass	
			
	def getImages(self):
		return 	self.__info["images"]	
			
if __name__ == '__main__':
	s = Segnalazione()
	print(s.getInfo())
	s.setInfo("phone_number", "347401416")
	print(s.getInfo())
	try:
		s.addImage("ciao")
	except NameError as err:
		print("questo non va bene... : ", err)
	si = SegnalazioneImage("i.jpg")
	s.addImage(si)
	print(s.getImages())
	for i in s.getImages():
		print (i.getFilename())
	try:
		s.setInfo("colore", "red")
	except NameError as err:
		print("questo non va bene... : ", err)
