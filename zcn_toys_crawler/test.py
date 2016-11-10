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

log_file = file("test.log", "w")

get_list = [
	u'aplus'
]



#print i
#opener = urllib2.build_opener()
#opener.addheaders = [('User-agent', 'Mozilla/5.0')]
#opener.addheaders.append(('Cookie', 'cookiename=cookievalue'))
#html = opener.open(i)
#html = urllib2.urlopen(i)
#txt = html.read()

#获得建议零售价
txt = codecs.open("test.html", 'r').read()
log_file.write(txt)
soup = BeautifulSoup(txt, 'html.parser')
line = []
price_re = soup.find(id = "price")
price_t = price_re.findAll('table')
flag = False
#for row in price_t:
#	cols = row.find_all('td')
#	if cols[0].get_text() == u'厂商建议零售价:':
#		print cols[1].get_text()


# 获得描述信息
#for i in get_list:
#	divs = soup.find(id = u'aplus')
#	[x.extract() for x in divs.findAll('script')]
#	[x.extract() for x in divs.findAll('style')]
#	for j in divs:
#		try:
#			print j.get_text()
#		except:
#			pass

#逐条获得基本信息
descript = soup.find(id = "detail_bullets_id")
#print descript
'''
[x.extract() for x in descript.findAll('script')]
[x.extract() for x in descript.findAll('style')]
lists = descript.findAll('li')
for li in lists:
	try:
		print "-------"
		print li.get_text()
		if str(li.get_text()).find("产地") > -1:
			break;
	except:
		pass
'''

# 获得排名
rank = soup.find(id = "SalesRank")
[x.extract() for x in rank.findAll('a')]
[x.extract() for x in rank.findAll('script')]
[x.extract() for x in rank.findAll('style')]
[x.extract() for x in rank.findAll('ul')]
print rank.get_text().strip()

# 逐条获得基本信息
#totalDes = soup.find(id = "productDescription_feature_div")
#[x.extract() for x in totalDes.findAll('script')]
#[x.extract() for x in totalDes.findAll('style')]
#h2 = totalDes.findAll('div', class_='disclaim')
#print h2[0].get_text()
#subTitles = totalDes.findAll('h3')
#for title in subTitles:
#	print title.get_text()
#	print title.next_sibling.next_sibling.get_text()



log_file.close()
