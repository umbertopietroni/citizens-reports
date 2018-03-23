

import re
import os
import pprint
import csv


def clean_txt(s):
	tmp = ''
	#accenti negrar
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
	

#compile crea un oggetto



# PARSE CASTELNUOVO (cartella html)
# nel replace ci vuole "'\n b'"

#tipologia_re = re.compile('Tipologia:</span> <span class="campo">(.+?)</span>')
#titolo_re = re.compile('Oggetto:</span> <span class="campo">(.+?)</span>')
#descrizione_re = re.compile('Descrizione problema:</span> <span class="campo">(.+?)</span>')

#count = 0
#for f in os.listdir('sources/castelnuovo'):
	
	#fname = "sources/castelnuovo/" + f
	#content = open(fname, 'r').read().replace("'\n b'","")
	
	#tipo = tipologia_re.findall(content)
	#titolo = titolo_re.findall(content)
	#descrizione = descrizione_re.findall(content)
	
	
	#if descrizione:
		#descr = clean_txt(descrizione[0])
		##descr = descrizione[0]
		#print (f, tipo, descr)
		#count += 1
		
	

#print ("count: "+ str(count))  


#PARSE VOLPIANO (cartella html_volpiano)
#nel replace ci vuole .replace("'\n '", "").replace("\n", "")
#tipologia_re = re.compile('Tipo</th><td class="menusoltesto width70f">(.+?)</td>')
#descrizione_re = re.compile('Segnalazione</th><td class="menusoltesto width70f">(.+?)</td>')




#PARSE NEGRAR (cartella html_negrar)    619 non disponibili(da eliminare)
#replace('"',"'").replace("'\n b'","").replace(r"\r\n","")

#tipologia_re = re.compile('Servizio</div></div></td>      <td>(.+?)</td>')
#descrizione_re = re.compile('Segnalazione</div></div></td>      <td>(.+?)</td>')



#count = 0
#for f in os.listdir('sources/negrar'):
	
	#fname = "sources/negrar/" + f
	#content = open(fname, 'r').read().replace('"',"'").replace("'\n b'","").replace(r"\r\n","")
	
	#tipo = tipologia_re.findall(content)
	##titolo = titolo_re.findall(content)
	#descrizione = descrizione_re.findall(content)
	
	
	#if descrizione:
		#descr = clean_txt(descrizione[0])
		##descr = descrizione[0]
		#print (f, tipo, descr)
		#count += 1
		
	

#print ("count: "+ str(count))  


#PARSE CAGLIARI
#IGIENE DEL SUOLO -> AMBIENTE
#Polizia_Municipale__ -> SICUREZZA
#Parchi__Verde_e_Gestione_Faunistica__Ufficio_Verde_Pubblico__ ->ambiente




#tipologia_re = re.compile('Uffici incaricati:</span>[ ]*(.+?)</div>')
##titolo_re = re.compile('Oggetto:</span> <span class="campo">(.+?)</span>')
#descrizione_re = re.compile('Descrizione:</span>[ ]*<span style="line-height: 2">(.+?)</span>')


				
					
#count = 0
#with open('cagliaridataset.csv', 'w') as csvfile:
	#filewriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
	#for f in os.listdir('sources/cagliari'):
		
		#fname = "sources/cagliari/" + f
		#content = open(fname, 'r').read().replace("\n"," ").replace("\t","").replace('&nbsp;',"")
		
		#tipo = tipologia_re.findall(content)
		##titolo = titolo_re.findall(content)
		#descrizione = descrizione_re.findall(content)
		
		##print (f, tipo, descrizione)
		#if descrizione and tipo:
			#descr = clean_txt(descrizione[0])
			#tipox = clean_txt(tipo[0]).replace(" ","_")
			##descr = descrizione[0]
			##print (f, tipo[0], descr)
			#array = [f,descr,tipox]
			#filewriter.writerow(array)
			#count += 1
		


#print ("count: "+ str(count)) 


#PARSE CAMERANO
#messo (.*?) perchè a volte la categoria non c'è
tipologia_re = re.compile('<div class="contenutocella">Servizio</div></div></td>[ ]*<td>(.*?)</td>')
#titolo_re = re.compile('Oggetto:</span> <span class="campo">(.+?)</span>')
descrizione_re = re.compile('div class="contenutocella">Segnalazione</div></div></td>[ ]*<td>(.+?)</td>')

					
count = 0
with open('cameranodataset.csv', 'w') as csvfile:
	filewriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
	for f in os.listdir('sources/camerano'):
		
		fname = "sources/camerano/" + f
		content = open(fname, 'r',encoding = "WINDOWS-1252").read().replace("\n"," ").replace("&quot;","")
		
		tipo = tipologia_re.findall(content)
		#titolo = titolo_re.findall(content)
		descrizione = descrizione_re.findall(content)
		
		#print (f, tipo, descrizione)
		if descrizione and tipo and tipo[0] != "":
			descr = clean_txt(descrizione[0])
			tipox = clean_txt(tipo[0]).replace(" ","_")
			descr = descrizione[0]
			print (f, tipox, descr)
			#array = [f,descr,tipox]
			#filewriter.writerow(array)
			count += 1
		


print ("count: "+ str(count)) 



 
 

 
 	

