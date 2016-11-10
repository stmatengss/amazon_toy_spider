# -*- coding: utf-8 -*-  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
from bs4 import *
import bs4
import csv
import codecs
import re

fout = file("list.test", 'r')
log_file = file("test.log", "w")

get_list = [
	u'aplus'
]

links_set = fout.readlines()


for i in links_set:
	print i
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	opener.addheaders.append(('Cookie', 'cookiename=cookievalue'))
	html = opener.open(i)
	#html = urllib2.urlopen(i)
	txt = html.read()
	log_file.write(txt)
	print txt
	soup = BeautifulSoup(txt, 'html.parser')
	line = []
	#***************#
	for i in get_list:
		print i
		divs = soup.find(id = u'brand')
		print divs
		cleanr = re.compile('<.*?>')
		#cleantext = re.sub(cleanr, '', divs)
		#print cleantext
		
	#***************#
	#***************#
	# table = soup.findAll("td", class_="bucket")[0].div.findAll('li')
	# for i in table:
	# 	pass

fout.close()
log_file.close()


