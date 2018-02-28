import urllib
import string
import time
import http.client
import re

domain = "www.comunevolpiano.to.it"
url = "/ComSegnalazioniDettaglio.asp?Id=%s"

conn = http.client.HTTPConnection(domain)
idrex = re.compile('ComSegnalazioniDettaglio.asp\?Id=(.+?)>')

txt = open('volpianomain.html', 'rb').read()
ids = idrex.findall(str(txt))

for i in ids:
	print("%s ..." % i)
	conn.request("GET",url % i)
	print(url % i)
	txt = conn.getresponse().read()
	open('sources/volpiano/' + str(i).zfill(4) + '.html', 'wb').write(txt)
	time.sleep(0.2)
