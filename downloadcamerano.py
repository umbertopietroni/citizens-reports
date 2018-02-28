import string
import time
import os
import urllib

msg_dir = "sources/camerano/"
print ("msg_dir => ", msg_dir)
try:
	os.makedirs(msg_dir)
except:
	pass
	
for i in range(1,2318):
	print("%s ..." % i)
	txt = urllib.urlopen("http://www.comune.camerano.an.it/gu/gu_p_consulta.php?idguasto="+str(i)+"&x=").read()
	open('sources/camerano/' + str(i).zfill(4) + '.html', 'w').write(txt)
	
