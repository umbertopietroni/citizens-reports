def clean_txt(s):
	tmp = ''
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


 
