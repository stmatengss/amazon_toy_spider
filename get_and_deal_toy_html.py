# -*- coding: utf-8 -*-  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
from bs4 import *
import bs4
import csv
import codecs

fout = file("list", 'r')
csvfile = file('toys.csv', 'wb')
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile)

get_list = [
	u'productTitle',
	u'brand'
	u'acrCustomerReviewText',
	u'priceblock_ourprice',
	u'ddmMerchantMessage'
]

links_set = fout.readlines()

# for i in range(1,300):
# 	print url_preffix1.format(i)
# 	opener = urllib2.build_opener()
# 	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
# 	html = opener.open(url_preffix1.format(i))
# 	# html = urllib2.urlopen(url_preffix1.format(i))
# 	txt = html.read()
# 	if i % 20 == 0:
# 		print (i/20)
# 	soup = BeautifulSoup(txt, 'html.parser')
# 	links = soup.findAll("a", class_='a-link-normal s-access-detail-page  a-text-normal')
# 	for j in links:
# 		if j['href'] not in links_set:
# 			links_set.add(j['href'])

for i in links_set:
	print i
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Chrome/51.0.2704.63')]
	html = opener.open(i)
	html = urllib2.urlopen(i)
	txt = html.read()
	soup = BeautifulSoup(txt, 'html.parser')
	line = []
	#***************#
	for i in get_list:
		divs = soup.findAll(id = i)
		if len(divs) == 0:
			line.append("")
			continue
		name = divs[0].text.strip()
		print name
		if name:
			line.append(name)
		else:
			line.append("")
	#***************#
	classify = soup.findAll("a",  class_="a-link-normal a-color-tertiary")
	if len(classify) == 3:
		line.append(classify[2].text.strip())
	else:
		line.append("")
	#***************#
	# table = soup.findAll("td", class_="bucket")[0].div.findAll('li')
	# for i in table:
	# 	pass
	writer.writerow(line)

fout.close()
csvfile.close()



