import sys
import os
import pprint
import json
import time
import datetime

sys.path.insert(0, '../dbinterface/')
from classes import *

sys.path.insert(0, '../wsinterface/')
from image_classification import predict_image, create_prob_dict

# search issue in inbox

telegram_inbox = "../telegram/inbox/"
whatsapp_inbox = "../whatsapp/inbox/"

telegram_enabled = True
whatsapp_enabled = True

if telegram_enabled:
	# TELEGRAM ISSUES
	inbox = telegram_inbox
	issues_list = os.listdir(inbox)
	for d in issues_list:
		issuedir = inbox + d + '/'
		print ("analyzing {} ".format(issuedir))

		msg_dict_file = issuedir + 'msg.dict'
		if not os.path.exists(msg_dict_file):
			continue
		
		msgdict = eval(open(msg_dict_file, 'r').read())
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
		s.setInfo("text", msgdict.get('text', ''))
		s.setCategory(msgdict.get('category', ''))
		s.setClassificationDict(msgdict.get('text_category', {}))
		
		# add all issue images 
		for p in msgdict["photo"]:
			im = IssueImage(issuedir + p["file_id"] + ".jpg")
			im.setClassificationDict(p['photo_category'])
			s.addImage(im)
			
		s.save()

		pprint.pprint(s.info)

# WHATSAPP ISSUES

if whatsapp_enabled:
	inbox = whatsapp_inbox
	users_list = os.listdir(inbox)
	for u in users_list:
		userdir = inbox + u + '/'
		print ("USER {} : ".format(userdir))
		
		
		for d in os.listdir(userdir):
			issuedir = userdir + d + '/'
			print ("	ISSUE {} : ".format(issuedir))
		
			msg_dict_file = issuedir + 'msg.dict'
			if not os.path.exists(msg_dict_file):
				continue
			
			msgdict = eval(open(msg_dict_file, 'r').read())
			user_id = msgdict['user']
			ts = msgdict['ts']
			msg_id = msgdict.get('msg_id', 0)
			if not msg_id:
				print("Msg id not present! Skip message")
				continue

			#pprint.pprint(msgdict)

			s = Issue(msg_id, '')
			s.setInfo("firstname", msgdict.get('from', {}).get('first_name', ''))
			s.setInfo("lastname", msgdict.get('from', {}).get('last_name', ''))
			s.setInfo("username", msgdict.get('from', {}).get('username', ''))
			s.setInfo("user_id", user_id)
			s.setInfo("msg_id", msg_id)
			s.setInfo("date", ts.strftime("%Y-%m-%d"))
			s.setInfo("time", ts.strftime("%H:%M:%S"))
			s.setInfo("channel", 'whatsapp')
			s.setInfo("text", msgdict.get('text', ''))
			s.setCategory(msgdict.get('category', ''))
			s.setClassificationDict(msgdict.get('text_category', {}))

			# add all issue images 
			for p in msgdict.get("photo", []):
				print("		>>>> ", p)
				try:
					im = IssueImage(p.get('file_path', ''))
					im.setClassificationDict(p.get('photo_category', {}))
					s.addImage(im)
				except:
					print("	>> image list element format is not correct...")
			
			s.save()

			pprint.pprint(s.info)
