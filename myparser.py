import re
import os
import pprint
import traceback
#from BeautifulSoup import  BeautifulSoup
def clean_txt(s):
	tmp = ''
	s = s.replace("\\xf9","u")
	s = s.replace("\\xe8","e")
	s = s.replace("\\xe0","a")
	s = s.replace("\\x92"," ")
	s = s.replace("\\xf2","o")
	
	#castelnuovo
	s = s.replace(r"\xc3\x83\xc2\x83\xc3\x82\xc2\xa8",'e')
	s = s.replace(r"\xc3\x83\xc2\x83\xc3\x82\xc2\xb2",'o')
	s = s.replace(r"\xc3\x83\xc2\x83\xc3\x82\xc2\xa0",'a')
	s = s.replace(r"\xc3\x83\xc2\x82\xc3\x82\xc2\xb0",' ')
	s = s.replace(r"\xc3\xa8",'e')
	s = s.replace(r"\xc3\xa9",'e')
	s = s.replace(r"\xc3\xb2",'o')
	s = s.replace(r"\xc3\xa0",'a')
	s = s.replace(r"\xc3\xb9",'u')
	
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




dataset_file = open('dataset.csv', 'w')
dataset_file.write('text,class,infoclass,city\n')
data = []
illuminazione = ["Pubblica_illuminazione","Illuminazione_Pubblica","Mobilita___Infrastrutture_viarie_e_Reti___Illuminazione_pubblica__"]
manutenzione = ["Manto_stradale__Marciapiedi", "Edifici","Edifici_pubblici", "Edifici_pericolanti","Strade_Piazze","Manutenzione_Strade","Arredo_Urbano","Mobilita___Infrastrutture_viarie_e_Reti__"]
ambiente = ["Verde Pubblico__Arredo urbano","Rifiuti","Ecologia__Rifiuti_","Animali","Deratizzazione","Derattizzazione__Disinfestazione", "Fognature_e_Depurazione","Autospurgo", "Acquedotto","Verde_Pubblico__Arredo_urbano","Verde_Pubblico","Parchi_Giardini","Fognatura_acquedotto","Cimitero","RifiutiAbbandono_rifiuti","Acquedotto_e_fognature","Servizi_di_igiene","Spazzamento","Pulizia_Fossi","Igiene_del_Suolo__","Parchi__Verde_e_Gestione_Faunistica__Ufficio_Verde_Pubblico__"] 
sicurezza = ["Segnaletica_stradale", "Polizia_Municipale","Impianti_Semaforici","Segnaletica","Mobilita___Infrastrutture_viarie_e_Reti___Polizia_Municipale__","Polizia_Municipale__","Polizia_Municipale___Mobilita___Infrastrutture_viarie_e_Reti__"]

rex_dict = {
	"castelnuovo" : {
		"tipologia": re.compile('Tipologia:</span> <span class="campo">(.+?)</span>'),
		"titolo": re.compile('Oggetto:</span> <span class="campo">(.+?)</span>'),
		"descrizione": re.compile('Descrizione problema:</span> <span class="campo">(.+?)</span>'),
	},
	"volpiano": {
		"tipologia": re.compile('Tipo</th><td class="menusoltesto width70f">(.+?)</td>'),
		"titolo": None,
		"descrizione": re.compile('Segnalazione</th><td class="menusoltesto width70f">(.+?)</td></tr>'),
	},
	"negrar": {
		"tipologia": re.compile('Servizio</div></div></td>      <td>(.+?)</td>'),
		"titolo": None,
		"descrizione": re.compile('Segnalazione</div></div></td>      <td>(.+?)</td>'),
	},
		"camerano": {
		"tipologia": re.compile('<div class="contenutocella">Servizio</div></div></td>[ ]*<td>(.*?)</td>'),
		"titolo": None,
		"descrizione": re.compile('div class="contenutocella">Segnalazione</div></div></td>[ ]*<td>(.+?)</td>'),
	},
		"cagliari": {
		"tipologia": re.compile('Uffici incaricati:</span>[ ]*(.+?)</div>'),
		"titolo": None,
		"descrizione": re.compile('Descrizione:</span>[ ]*<span style="line-height: 2">(.+?)</span>'),
	},
}


tipodic = {}
idx = 0
def gettipo(t):
	if not t:
		return 0
	if tipodic.get(t): return tipodic[t]
	global idx
	idx += 1
	tipodic[t] = idx
	return idx

count = 0
sources = os.listdir('sources/')
for s in sources:
	files_dir = 'sources/'+s+'/'
	files = os.listdir(files_dir)
	files.sort()
	scount = 0
	print("Source %s : %s files..." % (s, len(files)))
	
	for f in files:
		
		fname = files_dir + f
		
		
		if s in ('castelnuovo'):
			content = open(fname, 'r').read()
			content = content.replace("'\n b'", "")
			
			#content = content.replace("'\n b\"", "")
			#content = content.replace("\\'", "'")
			#content = content.replace("'\n '", "").replace("\n", "")
		elif s in ('volpiano'):
			content = open(fname, 'r').read()
			content = content.replace("'\n '", "").replace("\n", "")
		elif s in ('negrar'):
			content = open(fname, 'r').read()
			content = content.replace('"',"'").replace("'\n b'","").replace(r"\r\n","")
		elif s in ('camerano'):
			content = open(fname, 'r',encoding = "WINDOWS-1252").read().replace("\n"," ").replace("&quot;","")
		elif s in ('cagliari'):
			content = open(fname, 'r').read().replace("\n"," ").replace("\t","").replace('&nbsp;',"")
			
		
		# extracts info by reg exp
		type_rex = rex_dict[s]["tipologia"]
		descr_rex = rex_dict[s]["descrizione"]
		title_rex = rex_dict[s]["titolo"]
		
		tipo = descrizione = titolo = ""
		
		if type_rex:
			tipo = type_rex.findall(content)
			if tipo:
				tipo = clean_txt(tipo[0]).replace(" ", "_")
				if (tipo in ambiente):
					tipo = "Ambiente"
				elif (tipo in manutenzione):
					tipo = "Manutenzione"
				elif (tipo in illuminazione):
					tipo = "Illuminazione"
				elif (tipo in sicurezza):
					tipo = "Sicurezza"
				else:
					continue
			else:
				tipo = "Generic"
		if descr_rex:
			descrizione = descr_rex.findall(content)
			if descrizione:
				descrizione = clean_txt(descrizione[0])  #.encode("ascii","ignore")
			else:
				descrizione = ''
		if title_rex:
			titolo = title_rex.findall(content)
			if titolo:
				titolo = clean_txt(titolo[0])
			else:
				titolo = ''

		if descrizione:
			#print (">>>", s, f, tipo, descrizione)
			tipoidx = gettipo(tipo)
			data.append('"%s",%s,"%s","%s"' % (descrizione, tipoidx, tipo, s ))
			count += 1
			scount += 1
			
	print(" >>>> ", scount, " files")
print ("%s files analyzed" % count) 	

for elem in data:
	dataset_file.write(elem + '\n')

import pprint
pprint.pprint(tipodic, open('categories.dict', 'w'))
