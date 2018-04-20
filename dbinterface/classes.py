from db_interface import *
from server_connection import *
#from Database import *
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
	
	#__file = None
	#__content = None
	#__classification_dict = {}
	#__category = None
	#__confidence = None
	
	def __init__(self, filename):
		self.__file = filename
		self.__content = open(filename, 'rb').read()
		self.__classification_dict = {}
		self.__category = None
		self.__confidence = None
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
		
	def printImage():
		print( self.__file, self.__classification_dict, self.__category);

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
	

	
	def __init__(self, msg_id):
		self.__info = {}
		self.__info["msg_id"]=msg_id
		self.__info["phone_number"]=''
		self.__info["user_id"]=None
		self.__info["channel"]=''
		self.__info["username"]=''
		self.__info["firstname"]=''
		self.__info["lastname"]=''
		self.__info["datetime"] = None
		#self.__info["date"]=None
		#self.__info["time"]=None
		self.__info["text"]=""
		self.__info["images"]=[]
		self.__info["position"] = {}
		self.__info["position"]["latitude"] = 0
		self.__info["position"]["longitude"] = 0
		
		self.__category = None
		self.__status = None
		self.__classification_dict = {}

		
	def save(self):
		if self.__info["channel"]=="telegram":
			saveIssue(self)
		elif self.__info["channel"]=="whatsapp":
			postServer(self)
			
		
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

	def setClassificationDict(self, class_dict):
		self.__classification_dict = class_dict
	
	def printIssue(self):
		print(self.__info, self.__classification_dict)

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

