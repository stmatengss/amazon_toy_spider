# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
import urllib
from bs4 import *
import bs4
import csv
import codecs
import time

fout = file("toy_list.txt", 'r')
csvfile = file('toys.csv', 'wb')
log_file = file('n_normal.log', 'w')
pass_link = file('pass_link.txt', 'w')
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile)
links_set = fout.readlines()
pass_count = 0
cu_count = 0

def normalTag(soup, line, tag):
	divs = soup.findAll(id = tag)
	if len(divs) == 0:
		line.append("")
	else:
		name = divs[0].text.strip()
		try:
			line.append(name)
		except:
			line.append("")
	return line

def productName(soup, line):
	return normalTag(soup, line, u'productTitle')

def productBrand(soup, line):
	return normalTag(soup, line, u'brand')

def produceRate(soup, line):
	return normalTag(soup, line, u'avgRating')

def reviewNumber(soup, line):
	return normalTag(soup, line, u'acrCustomerReviewText')

def recoPrice(soup, line):
	price_re = soup.find(id = "price")
	if price_re is None:
		line.append("")
		return line
	price_t = price_re.findAll('table')
	for row in price_t:
		cols = row.find_all('td')
		if cols[0].get_text() == u'厂商建议零售价:':
			line.append(u'厂商建议零售价:' + cols[1].get_text().strip())
			return line
		else:
			line.append("")
			return line

def priceSale(soup ,line):
	price = ""
	divs = soup.findAll(id = u'priceblock_ourprice')
	if len(divs) == 0:
		divs = soup.findAll(id = u'priceblock_saleprice')
		price = ""
	if len(divs) > 0:
		name = divs[0].text.strip()
		try:
			price = name
		except:
			pass
	line.append(price)
	return line


def productDescription(soup, line):
	totalDes = soup.find(id = "productDescription_feature_div")
	if totalDes is None:
		line.append("")
		return line
	[x.extract() for x in totalDes.findAll('script')]
	[x.extract() for x in totalDes.findAll('style')]
	h2 = totalDes.findAll('div', class_='disclaim')
	#line.append(h2[0].get_text()).strip()
	if len(h2) > 0:
		line.append(h2[0].get_text())
	else:
		line.append("")
	subTitles = totalDes.findAll('h3')
	for title in subTitles:
		title_str = ""
		content_str = ""
		try:
			title_str = title.get_text().strip()
			#line.append(title.get_text().strip() + title.next_sibling.next_sibling.get_text().strip())
		except:
			pass
		try:
			content_str = title.next_sibling.next_sibling.get_text().strip()
		except:
			pass
		line.append(title_str + content_str)
			
	return line

def offerDescription(soup, line):
	dsp = ""
	divs = soup.find(id = u'aplus')
	if divs:
		[x.extract() for x in divs.findAll('script')]
		[x.extract() for x in divs.findAll('style')]
		for j in divs:
			try:
				dsp = dsp + "\n" + j.get_text().strip()
			except:
				pass
	line.append(dsp)
	return line

def baseInfo(soup, line):
	descript = soup.find(id = "detail_bullets_id")
	if descript:
		[x.extract() for x in descript.findAll('script')]
		[x.extract() for x in descript.findAll('style')]
		lists = descript.findAll('li')
		for li in lists:
			try:
				line.append(li.get_text().strip())
				if str(li.get_text()).find("产地") > -1 :
					break
			except:
				pass
	else:
		line.append("")
	return line

def productRak(soup, line):
	rank = soup.find(id = "SalesRank")
	if rank:
		[x.extract() for x in rank.findAll('a')]
		[x.extract() for x in rank.findAll('script')]
		[x.extract() for x in rank.findAll('style')]
		[x.extract() for x in rank.findAll('ul')]
		line.append(rank.get_text().strip())
	else :
		line.append("")
	return line

def savePic(soup, cu_count):
	pic = soup.find(id = "imgTagWrapperId")
	if pic:
		pic_h = pic.findAll('img')[0]['src']
		file_name = "./img/" + str(cu_count) + ".jpg"
		urllib.urlretrieve(pic_h, file_name)



for i in links_set:
	print "------------------------------------"
	print i
	txt = ""
	try:
		opener = urllib2.build_opener()
		opener.addheaders = [('User-agent', 'Mozilla/5.0')]
		html = opener.open(i)
		txt = html.read()
	except:
		log_file.write(txt)
		pass_link.write(i)
		pass_count = pass_count + 1
		print "pass"
		continue
	soup = BeautifulSoup(txt, 'html.parser')
	line = []
	line.append(str(cu_count))
	#***************#
	productName(soup, line)
	productBrand(soup, line)
	produceRate(soup, line)
	reviewNumber(soup, line)
	recoPrice(soup, line)
	priceSale(soup, line)
	productDescription(soup, line)
	offerDescription(soup, line)
	baseInfo(soup, line)
	productRak(soup, line)
	savePic(soup, cu_count)
	line.append(i)
	writer.writerow(line)
	cu_count = cu_count + 1
	time.sleep(1)

result = "pass number : " + str(pass_count)
print result
log_file.write(result)

fout.close()
csvfile.close()
log_file.close()
pass_link.close()
