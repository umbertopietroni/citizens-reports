class IssueImage:
	
	__file = None
	__content = None
	__classification_dict = {}
	__category = None
	
	def __init__(self, filename):
		self.__file = filename
		self.__content = open(filename, 'rb').read()
		#pass
		
	def getFilename(self):
		return self.__file

	def getContent(self):
		return self.__content

	def getCategory(self):
		return self.__category
		
	def setCategory(self, category):
		self.__category = category
		
	def getClassificationDict(self):
		return self.__classification_dict

	def setClassificationDict(self, classification_dict):
		self.__classification_dict = classification_dict
		
class Issue:
	
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
	
	__category = None
	__status = None
	__classification_dict = {}
	
	def __init__(self):
		pass
		
	def save(self):
		# save data to DB
		pass
		
	def getInfo(self):
		return self.__info
		
	def setInfo(self, param, value):
		if param in self.__info.keys():
			self.__info[param] = value
		else:
			raise NameError("parameter 'param' is not valid")
			
	def addImage(self, i: IssueImage):
		if not isinstance(i, IssueImage):
			raise NameError("'i' is not a valid IssueImage object")
		self.__info["images"].append(i)
		pass	
			
	def getImages(self):
		return 	self.__info["images"]
		
	def getStatus(self):
		return self.__status
		
	def setStatus(self, status):
		self.__status = status

	def getCategory(self):
		return self.__category
		
	def setCategory(self, category):
		self.__category = category

	def getClassificationDict(self):
		return self.__classification_dict

	def setClassificationDict(self, classification_dict):
		self.__classification_dict = classification_dict
		
