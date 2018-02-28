
import string
import time
import os
import urllib

msg_dir = "sources/cagliari/"
print ("msg_dir => ", msg_dir)
try:
	os.makedirs(msg_dir)
except:
	pass
	
for i in range(901,2689):
	print("%s ..." % i)
	txt = urllib.urlopen("https://servizi.comune.cagliari.it/portale/it/listasegnalazioni.page?internalServletActionPath=%2FExtStr2%2Fdo%2Fjpgeofeedback%2FFront%2FFeedback%2Fview&internalServletFrameDest=28&id="+str(i)).read()
	open('sources/cagliari/' + str(i).zfill(4) + '.html', 'w').write(txt)
	time.sleep(0.2)

