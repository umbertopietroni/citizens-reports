#!/usr/bin/env python
# -*- coding: utf-8 -*
import telepot
import random
import time
import os
import pprint
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

from telepot.loop import MessageLoop
import traceback

bad_words = ["fanculo", "vaffa", "vaffanculo", "stronzo", "stronzi", "cazzo", "fottiti", "fottuto", "merda"]

users_category_choice = {}
state = 0



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
						[("Ambiente", "ambiente"), ("Sicurezza-Mobilità", "sicurezza")],
						[("Manutenzione", "manutenzione"), ("Illuminazione", "illuminazione")],
						[("Altro", "altro"),]
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
	#category_list è usato per controllare se text è uno delle categorie
	
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

	bot.sendMessage(chat_id, response, reply_markup=None)
	return 
		
	
	
"""
@on_callback_query

Uso della callback per gestire i vari passaggi di conferma della segnalazione e della categoria

1. InlineKeyboard per inviare o modificare segnalazione
2. InlineKeyboard dopo il calcolo della categoria per confermarla
3. Se categoria non è corretta si usa altra InlineKeyboard per chiedere direttamente a utente

"""

def on_callback_query(msg):
	
	
	global msg_to_save
	try:
		os.makedirs('inbox')
	except:
		pass
	ts = time.strftime("%Y-%m-%d--%H-%M-%S", time.localtime(time.time())) + "__" + str(time.time())
	msg_dir = "inbox/" + ts
	
	
	query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')

	
	msg_id = telepot.origin_identifier(msg)
	if (query_data == "invia"):
		print("pressed invia")
		response = """Grazie %s \nHo ricevuto la sua segnalazione! Sto calcolando la categoria...\n/menu_principale """ #% (str(["first_name"]))	# pollice su
		
		#SIMULAZIONE CLASSIFICAZIONE
		category= (random.choice(random.choice(REPLY_BUTTONS_TEXT)))[0]
		
		keyboard_btns = []
		L = []
		L.append(InlineKeyboardButton(text="Si", callback_data="si"))
		L.append(InlineKeyboardButton(text="No", callback_data="no"))
		keyboard_btns.append(L)
		response = """Calcolato categoria %s: è corretta?""" % category
		try:
			msg_to_save["category"] = category
			keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_btns)
			bot.editMessageText(msg_id,response, reply_markup = keyboard)
		except:
			print('Old Query Pressed')

		
	elif (query_data == "si"):
		keyboard_btns = []
		keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_btns)
		#bot.editMessageReplyMarkup(msg_id,reply_markup = keyboard)
		text = """Grazie! La sua segnalazione associata alla categoria %s è stata registrata correttamente. \nPuò inserire una nuova segnalazione""" % msg_to_save["category"]
		bot.editMessageText(msg_id,text, reply_markup = keyboard)
		print('Callback Query:', query_id, from_id, query_data,msg_id)
		
		pprint.pprint(msg_to_save, open(msg_dir +'.dict', 'w'))
		msg_to_save = None
	elif (query_data == "no"):
		keyboard_btns = []
		for row in REPLY_BUTTONS_TEXT:
			L = []
			for col in row:
				L.append(InlineKeyboardButton(text=col[0], callback_data=col[1]))
			keyboard_btns.append(L)
		keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_btns)
		bot.editMessageText(msg_id,'Scegli quale categoria è più corretta', reply_markup = keyboard)
	else:
		keyboard_btns = []
		keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_btns)
		#bot.editMessageReplyMarkup(msg_id,reply_markup = keyboard)
		text = """Grazie! La sua segnalazione associata alla categoria %s è stata registrata correttamente. \nPuò inserire una nuova segnalazione""" % query_data
		bot.editMessageText(msg_id,text, reply_markup = keyboard)
		print('Callback Query:', query_id, from_id, query_data,msg_id)
		msg_to_save["category"] = query_data
		pprint.pprint(msg_to_save, open(msg_dir + '.dict', 'w'))
		msg_to_save = None
		
		


	bot.answerCallbackQuery(query_id, text=query_data)

def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	
	global msg_to_save
	
	print (content_type, chat_type, chat_id, msg["message_id"])
	try:
				
		received_text = cleanChars(msg.get("text", ""))
		bot_name = '@'+bot.getMe()["username"]
		received_text = received_text.replace(bot_name,"")
		
		
		photo = msg.get("photo", [])
		document = msg.get("document", [])
		userinfo = msg["from"]
		
		if msg.get("text", "") and msg.get("text", "")[0] == '/':
			return menu_function(msg.get("text", ""), chat_id)

		if photo:
			photo_id = photo[-1]["file_id"] # dimensione maggiore
			bot.download_file(photo_id, msg_dir + "/" + photo_id + ".jpg")
			
		if document:
			document_id = document["file_id"]
			fname = document["file_name"] # dimensione maggiore
			bot.download_file(document_id, msg_dir + "/" + fname)
		
		keyboard_btns = []
		L = []
		L.append(InlineKeyboardButton(text="Invia", callback_data="invia"))
		L.append(InlineKeyboardButton(text="Modifica", switch_inline_query_current_chat=msg.get("text", "")))
		keyboard_btns.append(L)
		response = """Grazie %s \n Vuole inviare questa segnalazione o la vuole modificare?""" % (str(userinfo["first_name"]))
		
		
		
		

		#response = """Grazie %s \nLa tua segnalazione è stata ricevuta! Sto calcolando la categoria...\n/menu_principale """ % (str(userinfo["first_name"]))	# pollice su
		#bot.sendMessage(chat_id, response)
		
		##SIMULAZIONE CLASSIFICAZIONE
		#category= (random.choice(random.choice(REPLY_BUTTONS_TEXT)))[0]
		
		#keyboard_btns = []
		#L = []
		#L.append(InlineKeyboardButton(text="Si", callback_data="si"))
		#L.append(InlineKeyboardButton(text="No", callback_data="no"))
		#keyboard_btns.append(L)
		#response = """Calcolato categoria %s: è corretta?""" % category
		
		msg["text"] = received_text
		msg_to_save = msg
		
		bot.sendMessage(chat_id,response, reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard_btns))
			
		


	except:
		bot.sendMessage(chat_id, "Ooops! Qualcosa e' andato storto! Riprova, Grazie!")
		bot.sendSticker(chat_id, "CAADAgADzwUAAmMr4gmeXsfnL_icMwI")
		print (traceback.format_exc())


#TOKEN = '413385905:AAEN1t4iOHGwJ8UDzkSPJH2a7NsPw3bV3ag'		# AnzioBot

#TOKEN = '385347809:AAGluuiZF1BbRtA9y6peSB6MbR_saJYGlVU'			# Segnalazioni_MontecchioEmilia_Bot DEVEL
#TOKEN = '534678830:AAH3MvgnILV71lRvFerjBTKxOn-C3WaMh3Y' 		# Segnalazioni_MontecchioEmilia_Bot ON LINE
TOKEN = '462484974:AAG-6eBXHXy6OEdFUCoRSF8klZohXobfnXw'           #Test_Segnalazioni_bot
bot = telepot.Bot(TOKEN)

import sys
#print (sys.argv)

#bot.message_loop(on_chat_message)

MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()

#MessageLoop(bot,on_chat_message).run_as_thread()

print ('REAL TIME MODE: Listening ...')
while 1:
	time.sleep(5)
