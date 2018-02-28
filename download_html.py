import urllib.request
import pprint
import os
from urllib.request import Request, urlopen
import re



#http://castelnuovobga.ldpgis.it/urp/pub/info_segnalazione.php?id=246 (max sono 246)
#http://www.comunevolpiano.to.it/ComSegnalazioniDettaglio.asp?Id=2753   (non sono veramente 2753)

#http://www.comune.arezzo.it/il-comune/servizi/comunicazione/gestione-reclami/420 (da 420 a 2700) molte non hanno categoria


msg_dir = "html_negrar/"
print ("msg_dir => ", msg_dir)
try:
	os.makedirs(msg_dir)
except:
	pass
	
# html per comune di Castelnuovo
#for val in range(17,247):
	#with urllib.request.urlopen('http://castelnuovobga.ldpgis.it/urp/pub/info_segnalazione.php?id=246'+str(val)) as response:
		#html = response.read()
		#pprint.pprint(html, open(msg_dir + str(val), 'w'))


#html per comune Volpiano 

#tipologia_re = re.compile('Tipo</th><td class="menusoltesto width70f">(.+?)</td>')
#descrizione_re = re.compile('Segnalazione</th><td class="menusoltesto width70f">(.+?)</td>')


#for val in range(1, 2754):
	#req = Request('http://www.comunevolpiano.to.it/ComSegnalazioniDettaglio.asp?Id='+str(val), headers={'User-Agent': 'Mozilla/5.0'})
	#webpage = urlopen(req).read().decode('latin-1')
	##content = webpage.replace("'\n b'", "")
	#tipo = tipologia_re.findall(webpage)
	#if (tipo):
		#print(val);
		#pprint.pprint(webpage, open(msg_dir + str(val), 'w'))
		
	##prima di modifiche
	##webpage = urlopen(req).read()
	##pprint.pprint(webpage, open(msg_dir + str(val), 'w'))
	
   
#html per comune di Negrar (da 12 a 4905)
#http://www.comunenegrar.it/c023052/gu/gu_p_consulta.php?idguasto=12&x=

for val in range(12,4906):
	with urllib.request.urlopen('http://www.comunenegrar.it/c023052/gu/gu_p_consulta.php?idguasto='+str(val)+'&x=') as response:
		html = response.read()
		print(val)
		pprint.pprint(html, open(msg_dir + str(val), 'w'))
		
