import urllib
import string
import time
for i in range(4908):
	print("%s ..." % i)
	txt = urllib.urlopen("http://www.comunenegrar.it/c023052/gu/gu_p_consulta.php?idguasto=%s&x=" % i).read()
	open('sources/negrar/' + string.zfill(i, 4) + '.html', 'w').write(txt)
	time.sleep(0.2)
