import sys
import os
import pprint
import json
import time

sys.path.insert(0, '../dbinterface/')
from classes import *

if len(sys.argv) < 3:
	exit("""
Input : user_id, msg_id
Ex: python3 test_manage_segnalazione.py 4486779 249
			""")
user_id = int(sys.argv[1])
msg_id = int(sys.argv[2])

# print(user_id, msg_id)

# search issue in inbox

telegram_inbox = "../telegram/inbox/"
whatsapp_inbox = "../whatsapp/inbox/"

inbox = telegram_inbox

issues_list = os.listdir(inbox)
#print(issues_list)
for d in issues_list:
	curdir = inbox + d + '/'
	
	msg_dict_file = curdir + 'msg.dict'
	if not os.path.exists(msg_dict_file):
		continue
	
	msgdict = eval(open(msg_dict_file, 'r').read())
	if msgdict['chat']['id'] == user_id and msgdict['message_id'] == msg_id:
		#pprint.pprint(msgdict)

		user_id = msgdict['chat']['id']
		msg_id = msgdict['message_id']

		# create new Issue
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
		
		# add all issue images 
		for p in msgdict["photo"]:
			im = IssueImage(curdir + p["file_id"] + ".jpg")
			im.setClassificationDict(p['photo_category'])
			s.addImage(im)
			
		s.save()

		pprint.pprint(s.info)
