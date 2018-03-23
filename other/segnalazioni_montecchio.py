#!/usr/bin/env python
# -*- coding: utf-8 -*
import telepot
import random
import time
import os
import pprint
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.loop import MessageLoop
import traceback

bad_words = ["fanculo", "vaffa", "vaffanculo", "stronzo", "stronzi", "cazzo", "fottiti", "fottuto", "merda"]

users_category_choice = {}


"""
## SCHEMA IMMAGINE

{u'caption': u'TESTO DELLA FOTO',			### opzionale 
 u'chat': {u'first_name': u'Giulio',
           u'id': 4486779,
           u'last_name': u'Angiani',
           u'type': u'private'},
 u'date': 1514890736,
 u'from': {u'first_name': u'Giulio',
           u'id': 4486779,
           u'is_bot': False,
           u'language_code': u'it',
           u'last_name': u'Angiani'},
 u'message_id': 281,
 u'photo': [{u'file_id': u'AgADBAADV6oxGy0BWFLOV5N99oe5sJo0JhoABJtfbSh7Km9yHtUBAAEC',
             u'file_path': u'photos/file_0.jpg',
             u'file_size': 1134,
             u'height': 90,
             u'width': 87},
            {u'file_id': u'AgADBAADV6oxGy0BWFLOV5N99oe5sJo0JhoABOVmGnF9pPiaH9UBAAEC',
             u'file_size': 16707,
             u'height': 320,
             u'width': 311},
            {u'file_id': u'AgADBAADV6oxGy0BWFLOV5N99oe5sJo0JhoABEZgAzISevaqHdUBAAEC',
             u'file_size': 27271,
             u'height': 439,
             u'width': 427}]}


"""

REPLY_BUTTONS_TEXT = [
						[("Ambiente", "ambiente"), ("Sicurezza", "sicurezza"), ("Traffico", "traffico"),],
						[("Sosta vietata", "sosta"), ("Buca pericolosa", "buca"), ("Altro", "altro"),]
					]



def cleanChars(s):
	for ch in """"?!!"£$%&/()ç°§[]{}""":
		try:
			s = s.replace(ch, ' ' + ch + ' ')
		except:
			pass
	return s


def menu_function(text, chat_id):
	response = "Comando non riconosciuto "
	categories = "Clicca per\n"
	categories_test = ""
	category_list = []
	global users_category_choice
	
	for row in REPLY_BUTTONS_TEXT:
		for col in row:
			categories += "/" + col[1] + "  "
			categories_test += "'" + col[0] + "' "
			category_list.append("/"+col[1])
	#categories = ""
	
	#categories e categories_test sono stringhe che uso nel messaggio di inizio
	#category_list è usato per controllare se test è uno delle categorie
	
	if text in ('/start', '/help', '/menu_principale'):
		
		
		response = """Comune di Montecchio Emilia\nServizio per le segnalazioni del cittadino
[Servizio in fase di sperimentazione]
%(categories)s

Scrivi un messaggio con la tua segnalazione
e allega se vuoi una immagine.
Puoi anche condividere la tua posizione
per una geolocalizzazione piu' precisa.

Se non lo fai ora, dopo la tua segnalazione il servizio ti chiedera'
di scegliere una categoria fra
%(categories_test)s

In base a questa informazione la tua segnalazione
sara' smistata all'ufficio di competenza

Grazie della collaborazione
""" % vars()
	
	

	if text in category_list:
		users_category_choice[chat_id] = text
		response = """OK! Hai scelto la categoria %s
        Ora inserisci la tua segnalazione e inviala.
        Grazie
""" % text[1:]

	#print ("DENTRO", users_category_choice)

	bot.sendMessage(chat_id, response, reply_markup=None)
	return 
		
	

#def on_callback_query(msg):
#	query_id, chat_id, query_data = telepot.glance(msg, flavor='callback_query')
#	if query_data=='sosta':
#		bot.sendMessage(chat_id, "Sosta!")
#	elif query_data=='time':
#		ts = time.time()
#		bot.answerCallbackQuery(query_id, text=datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')) #messaggio a comparsa
#	else:
#		response = """Categoria ricevuta!""" + '\xF0\x9F\x91\x8D'	# pollice su
#		bot.sendMessage(chat_id, response)

def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	global users_category_choice
	print (users_category_choice)
	pprint.pprint(msg)
	try:
				
		received_text = cleanChars(msg.get("text", ""))
		photo = msg.get("photo", [])
		document = msg.get("document", [])
		userinfo = msg["from"]
	#	print "USER", userinfo
		
		if msg.get("text", "") and msg.get("text", "")[0] == '/':
			return menu_function(msg.get("text", ""), chat_id)
		
		ts = time.strftime("%Y-%m-%d--%H-%M-%S", time.localtime(time.time())) + "__" + str(time.time())
		msg_dir = "inbox/" + ts
	#	print ("msg_dir => ", msg_dir)
		try:
			os.makedirs(msg_dir)
		except:
			pass


		if photo:
			photo_id = photo[-1]["file_id"] # dimensione maggiore
	#		print ("photo_id => ", photo_id)
			bot.download_file(photo_id, msg_dir + "/" + photo_id + ".jpg")
			
		if document:
			document_id = document["file_id"] # dimensione maggiore
			fname = document["file_name"] # dimensione maggiore
	#		print ("document_id => ", document_id)
			bot.download_file(document_id, msg_dir + "/" + fname)
		
	#	global bot
	#	print(dir(bot))

		if users_category_choice.get(chat_id, "") != "":
			msg["category"] = users_category_choice[chat_id]

		# save msg
		pprint.pprint(msg, open(msg_dir + '/msg.dict', 'w'))

	#	print("MSG", chat_id, users_category_choice)
		
		if users_category_choice.get(chat_id, "") == "":
			#test_callback
			for row in REPLY_BUTTONS_TEXT:
				for col in row:
					if received_text == col[0]:
			
						
						response = """Categoria """ + str(received_text) + """ ricevuta!\nGrazie!""" #\xF0\x9F\x91\x8D"""	# pollice su
						#print ("response = " + response)
						#bot.sendMessage(chat_id, response.decode("ascii", "ignore"), reply_markup=None)
						bot.sendMessage(chat_id, response, reply_markup=None, reply_to_message_id=msg["message_id"])

						return 
		else:
			users_category_choice[chat_id] = ""
			#bot.sendMessage(chat_id, "La tua segnalazione e' stata presa in carico, Grazie!", reply_markup=None)
			
			bot.sendMessage (chat_id,
				"""Grazie %s \nMessaggio ricevuto!\n%s\n\n/menu_principale """ % (str(userinfo["first_name"]), '\xF0\x9F\x91\x8D'),
				reply_markup=None)
			
			return
					

		response = """Grazie %s \nMessaggio ricevuto!\n%s\n\n/menu_principale """ % (str(userinfo["first_name"]), '\xF0\x9F\x91\x8D')	# pollice su


		bot.sendMessage(chat_id, response)
		
		# keyboard_btns contiene i bottoni con cui utente seleziona le categorie
		# REPLY_BUTTONS_TEXT
		
	
		keyboard_btns = []
		for row in REPLY_BUTTONS_TEXT:
			L = []
			for col in row:
#				L.append(KeyboardButton(text=col[0], callback_data=col[1]))
				L.append(KeyboardButton(text=col[0]))
			keyboard_btns.append(L)
				
		bot.sendMessage(chat_id, 'A quale categoria appartiene la tua segnalazione?',
                            reply_markup=ReplyKeyboardMarkup(
                                keyboard=keyboard_btns, one_time_keyboard=True
                            ))

	except:
		bot.sendMessage(chat_id, "Ooops! Qualcosa e' andato storto! Riprova, Grazie!")
		bot.sendSticker(chat_id, "CAADAgADzwUAAmMr4gmeXsfnL_icMwI")
		print (traceback.format_exc())

if 0:
	userinfo = {u'first_name': u'Giulio',
			   u'id': 4486779,
			   u'is_bot': False,
			   u'language_code': u'it',
			   u'last_name': u'Angiani'}
	response = """Grazie %s \nMessaggio ricevuto!\n\n/menu_principale """ % str(userinfo["first_name"]) + '\xF0\x9F\x91\x8D'# """ % userinfo["first_name"] # pollice su
	print (response)
	exit()

#TOKEN = '413385905:AAEN1t4iOHGwJ8UDzkSPJH2a7NsPw3bV3ag'		# AnzioBot

#TOKEN = '385347809:AAGluuiZF1BbRtA9y6peSB6MbR_saJYGlVU'			# Segnalazioni_MontecchioEmilia_Bot DEVEL
#TOKEN = '534678830:AAH3MvgnILV71lRvFerjBTKxOn-C3WaMh3Y' 		# Segnalazioni_MontecchioEmilia_Bot ON LINE
TOKEN = '462484974:AAG-6eBXHXy6OEdFUCoRSF8klZohXobfnXw'           #Test_Segnalazioni_bot
bot = telepot.Bot(TOKEN)

import sys
#print (sys.argv)

bot.message_loop(on_chat_message)

#MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()

print ('REAL TIME MODE: Listening ...')
while 1:
	time.sleep(5)

