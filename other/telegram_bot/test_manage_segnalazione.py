import sys
import os
import pprint
import json
import time

from classes import *

user_id = int(sys.argv[1])
msg_id = int(sys.argv[2])

"""
Input : user_id, msg_id
Ex: python3 test_manage_segnalazione.py 4486779 249

"""

# print(user_id, msg_id)

# search issue in inbox

issues_list = os.listdir('inbox')
#print(issues_list)
for d in issues_list:
	curdir = 'inbox/' + d + '/'
	msgdict = eval(open(curdir + 'msg.dict', 'r').read())
	if msgdict['chat']['id'] == user_id and msgdict['message_id'] == msg_id:
#		pprint.pprint(msgdict)

		user_id = msgdict['chat']['id']
		msg_id = msgdict['message_id']

		s = Issue(msg_id, '')
			
		s.setInfo("firstname", msgdict.get('from', {}).get('first_name', ''))
		s.setInfo("lastname", msgdict.get('from', {}).get('last_name', ''))
		s.setInfo("username", msgdict.get('from', {}).get('username', ''))
		s.setInfo("user_id", user_id)
		s.setInfo("msg_id", msg_id)
		s.setInfo("date", time.strftime("%Y-%m-%d", time.localtime(msgdict["date"])))
		s.setInfo("time", time.strftime("%H:%M:%S", time.localtime(msgdict["date"])))
		s.setInfo("channel", 'telegram')
		s.setInfo("text", msgdict['text'])
		s.setCategory(msgdict['category'])
		s.setClassificationDict(msgdict.get('text_category', {}))
		
		#print(s.channel)
		
		for p in msgdict["photo"]:
			
			im = IssueImage(curdir + p["file_id"] + ".jpg")
			im.setClassificationDict(p['photo_category'])
			#pprint.pprint(p)
			s.addImage(im)
			
		
#		print(s.getInfo("channel"))
#		print(s.getInfo("msg_id"))
#		print(s.getInfo())
#		print(s.getClassificationDict())

		s.save()

