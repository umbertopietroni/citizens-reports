import csv
import re
import os
import pprint

def clean_txt(s):
	tmp = ''
	s = s.replace("\\xf9","u")
	s = s.replace("\\xe8","e")
	s = s.replace("\\xe0","a")
	s = s.replace("\\x92"," ")
	s = s.replace("\\xf2","o")
	s = s.replace("?", " ")
	s = s.replace("!", " ")


	s = s.replace("'", " ")
	s = s.replace(".", " ")
	s = s.replace(",", " ")
	s = s.replace("<br />", " ")
	s = s.replace("\\n", " ")
	s = s.replace("</td>", " ")
	s = s.replace("<td>", " ")
	for ch in s:
		if ch in (' ') or \
		(ord(ch) >= 65 and ord(ch) <= 90) or \
		(ord(ch) >= 97 and ord(ch) <= 122) or \
		0:
			tmp += ch
	return tmp


tipologia_re = re.compile('Servizio</div></div></td>      <td>(.+?)</td>')
descrizione_re = re.compile('Segnalazione</div></div></td>      <td>(.+?)</td>')

illuminazione = ["Pubblica illuminazione"]
manutenzione = ["Manto stradale  Marciapiedi", "Edifici", "Edifici pericolanti"]
ambiente = ["Verde Pubblico  Arredo urbano","Ecologia  Rifiuti ","Derattizzazione  Disinfestazione", "Fognature e Depurazione","Autospurgo", "Acquedotto"] 
sicurezza = ["Segnaletica stradale", "Polizia Municipale","Impianti Semaforici"]

with open('dataset.csv', 'w') as csvfile:
	filewriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
	for f in os.listdir('html_negrar'):
		fname = "html_negrar/" + f
		content = open(fname, 'r').read().replace('"',"'").replace("'\n b'","").replace(r"\r\n","")
		tipo = tipologia_re.findall(content)
		#titolo = titolo_re.findall(content)
		descrizione = descrizione_re.findall(content)
		
		if descrizione and tipo:
			tipo_x = clean_txt(tipo[0])
			descrizione_x = clean_txt(descrizione[0])
			if (tipo_x in ambiente):
				tipo_x = "Ambiente"
			elif (tipo_x in manutenzione):
				tipo_x = "Manutenzione"
			elif (tipo_x in illuminazione):
				tipo_x = "Illuminazione"
			elif (tipo_x in sicurezza):
				tipo_x = "Sicurezza"
			
			array = [f,descrizione_x,tipo_x]
			filewriter.writerow(array)
    
