from db_interface import *
from functools import wraps
import pprint

def add_properties(fnz):
	@wraps(fnz)
	def f(pard, *args, **kwargs):
		classname = f.__name__
		for k in f.__dict__["_{}__info".format(classname)]:
#			print(k)
			prop = (lambda self: print(k))
#			print(prop, dir(prop))
			setattr (f, k, property(prop))
		return fnz(pard, *args, **kwargs)
	return f

class IssueImage:
	
	__file = None
	__content = None
	__classification_dict = {}
	__category = None
	__confidence = None
	
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
		
	def getConfidence(self):
		return self.__confidence
		
#	def setCategory(self, category):
#		# category is autmatically detected by confidence dict in setClassificationDict method
#		self.__category = category
		
	def getClassificationDict(self):
		return self.__classification_dict

	def setClassificationDict(self, classification_dict):
		self.__classification_dict = classification_dict
		self.__category = list(classification_dict.keys())[list(classification_dict.values()).index(max(classification_dict.values()))]
		self.__confidence = max(classification_dict.values())

	@property
	def info(self):
		return {
			"filename": self.getFilename(),
			"category": self.getCategory(),
			"confidence": self.getConfidence(),
			"classification_dict": self.__classification_dict
		}
		

#@add_properties	
class Issue:
	
	__info = {
		"id": None,
		"phone_number": '',
		"user_id": None,
		"msg_id": None,
		"channel": '',
		"username": '',
		"firstname":'',
		"lastname":'',
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
	
	def __init__(self, msg_id, username):
		self.__info["id"]=msg_id
		self.__info["phone_user"]=username
		
	def save(self):
		saveIssue(self)
		
	def getInfo(self, param=''):
		if param:
			if param in self.__info.keys():
				return self.__info[param]
			else:
				raise NameError("parameter '{}' is not valid".format(param))
		else:
			return self.__info
		
	def setInfo(self, param, value):
		if param in self.__info.keys():
			self.__info[param] = value
		else:
			raise NameError("parameter '{}' is not valid".format(param))
			
	def addImage(self, i: IssueImage):
		if not isinstance(i, IssueImage):
			raise NameError("'i' is not a valid IssueImage object")
		self.__info["images"].append(i)
		pass	
			
	def getImages(self):
		return 	self.__info["images"]
		
	def getUserId(self):	
		return 	self.__info["user_id"]
		
	def getMsgId(self):	
		return 	self.__info["msg_id"]
		
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
	
	def printIssue(self):
		print(self.__info, self.__category)

	def getLatitude(self):
		return self.__info["position"]["latitude"]
		
	def setLatitude(self, lat):
		self.__info["position"]["latitude"] = lat

	def getLongitude(self):
		return self.__info["position"]["longitude"]
		
	def setLongitude(self, lon):
		self.__info["position"]["longitude"] = lon
		
	@staticmethod
	def getIssueByMsgIdUserId(user_id, msg_id):
		return None
		
	@property
	def info(self):
		tmp = self.getInfo()
		imgs = tmp.get('images', [])
		tmp['images_detail'] = [i.info for i in tmp.get('images', [])]		
		return tmp

