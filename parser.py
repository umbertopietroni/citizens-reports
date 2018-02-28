import re
import os
import pprint
import traceback
#from BeautifulSoup import  BeautifulSoup
from tools import clean_txt




dataset_file = open('dataset.csv', 'w')
dataset_file.write('text,class,infoclass\n')
data = []

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
		"tipologia": re.compile('Servizio</div></div></td>\r\n[ ]*<td>(.+?)</td>'),
		"titolo": None,
		"descrizione": re.compile('<div class="contenutocella">Segnalazione</div></div></td>[ ]*<td>(.+?)</td>'),
	},
}


if 0:
	rex = rex_dict["negrar"]["descrizione"]
	txt = open("sources/negrar/4896.html", "r").read().replace("\n", " ").replace("\r", " ")
	l = rex.findall(txt)
	print(l)
	exit()

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
		#print("          >>>  ", f)
		fname = files_dir + f
		# reads file contents
		content = open(fname, 'r').read()
		
		if s in ('castelnuovo',):
			content = content.replace("'\n b'", "")
			content = content.replace("'\n b\"", "")
			content = content.replace("\\'", "'")
			
			content = content.replace("'\n '", "").replace("\n", "")
		if s in ('volpiano', 'negrar'):
			content = content.replace("\n", " ").replace("\r", " ").replace("<br />", " ")
		
		# block messages:
		if s in ('negrar'):
			if content.find("Questa segnalazione non ") > -1:
				continue
		
		if s in ('castelnuovo'):
			if content.find("La segnalazione %s non esiste" % f) > -1:
				continue

		
		# extracts info by reg exp
		type_rex = rex_dict[s]["tipologia"]
		descr_rex = rex_dict[s]["descrizione"]
		title_rex = rex_dict[s]["titolo"]
		
		tipo = descrizione = titolo = ""
		
		if type_rex:
			tipo = type_rex.findall(content)
			if tipo:
				tipo = tipo[0].replace(" ", "_")
			else:
				tipo = "Generic"
		if descr_rex:
			descrizione = descr_rex.findall(content)
			if descrizione:
				descrizione = clean_txt(descrizione[0]).encode("ascii","ignore")
			else:
				descrizione = ''
		if title_rex:
			titolo = title_rex.findall(content)
			if titolo:
				titolo = titolo[0]
			else:
				titolo = ''

		if descrizione:
			#print (">>>", s, f, tipo, descrizione)
			tipoidx = gettipo(tipo)
			data.append('"%s",%s,"%s","%s"' % (descrizione, tipoidx, tipo, s ))
			count += 1
			scount += 1
		else:
			print (">>> SKIP", s, f, tipo, descrizione)
			pass
			
	print(" >>>> ", scount, " files")
print ("%s files analyzed" % count) 	

for elem in data:
	dataset_file.write(elem + '\n')

import pprint
pprint.pprint(tipodic, open('categories.dict', 'w'))




