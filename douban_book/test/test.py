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
import re

fout = file("test_list.txt", 'r')
links_set = fout.readlines()
pass_count = 0
cu_count = 0


def getTitle(soup):
	print soup.title.string.replace("(豆瓣)",'')
	return soup.title.string.replace("(豆瓣)",'')

def getCountry1(name):
	pattern = re.compile(r'\((.+)\)')
	match = pattern.match(name)
	if match:
		print match.group(1)
		return match.group(1)
	else:
		print "no country"
		return ""

def getCountry2(name):
	pattern = re.compile(r'\[(.+)\]')
	match = pattern.match(name)
	if match:
		print match.group(1)
		return match.group(1)
	else:
		print "no country"
		return ""

def getAuthor(info):
	name = info.find(text=' 作者')
	t_span = name.parent.parent
	item = t_span.findAll('a')
	list_t = []
	for i in item:
		 list_t.append(i.get_text())
	print ",".join(list_t)

def getTranslator(info):
	name = info.find(text=' 译者')
	print name
	#try:
	t_span = name.parent.parent
	item = t_span.findAll('a')
	list_t = []
	for i in item:
		 list_t.append(i.get_text())
		#print name.parent.next_sibling.next_sibling.get_text().strip()
		#return name.parent.next_sibling.next_sibling.get_text().strip()
	#except:
	#	print "无译者"
	#	return ""
	print ",".join(list_t)

def getPublication(info):
	pub = info.find(text='出版社:')
	try:
		print pub.parent.next_sibling.strip()
		return pub.parent.next_sibling.strip()
	except:
		print "no publiction"
		return ""

def getRawTitle(info):
	r_title = info.find(text='原作名:')
	try :
		print r_title.parent.next_sibling.strip()
		return r_title.parent.next_sibling.strip()
	except:
		print "no raw title"
		return ""

def getBinding(info):
	bind = info.find(text='装帧:')
	try:
		print bind.parent.next_sibling.strip()
		return bind.parent.next_sibling.strip()
	except:
		print "no binding"
		return ""

def getPubDate(info):
	date = info.find(text='出版年:')
	try:
		print date.parent.next_sibling.strip()
		return date.parent.next_sibling.strip()
	except:
		print "no publication date"
		return ""

def getPages(info):
	pages = info.find(text='页数:')
	try:
		print pages.parent.next_sibling.strip()
		return pages.parent.next_sibling.strip()
	except:
		print "no pages"
		return ""

def getPrice(info):
	price = info.find(text='定价:')
	try:
		print price.parent.next_sibling.strip()
		return price.parent.next_sibling.strip()
	except:
		print "no price"
		return ""

def getSeries(info):
	series = info.find(text='丛书:')
	try:
		print series.parent.next_sibling.next_sibling.get_text().strip()
		return series.parent.next_sibling.next_sibling.get_text().strip()
	except:
		print "no series"
		return ""

def getISBN(info):
	isbn = info.find(text='ISBN:')
	try:
		print isbn.parent.next_sibling.strip()
		return isbn.parent.next_sibling.strip()
	except:
		print "no isbn"
		return ""

def getinfo(soup):
	info = soup.find(id = 'info')
	#getISBN(info)
	#getSeries(info)
	#getPrice(info)
	#getPages(info)
	#getPubDate(info)
	#getBinding(info)
	#getRawTitle(info)
	#getPublication(info)
	#getAuthor(info)
	getTranslator(info)

def getContent(soup):
	content_intro = soup.find(id = 'link-report')
	if content_intro :
		[x.extract() for x in content_intro.findAll('script')]
		[x.extract() for x in content_intro.findAll('style')]
		if content_intro.find('span', class_='short'):
			print content_intro.find('span', class_='all hidden').get_text().strip()
			return content_intro.find('span', class_='all hidden').get_text().strip()
		else:
			print content_intro.get_text().strip()
			return content_intro.get_text().strip()
	else:
		print "no content intro"
		return ""

def getRatingPeople(soup):
	rates_num = soup.find('a', class_='rating_people')
	if rates_num:
		number = rates_num.find('span')
		print number.get_text().strip()
		return number.get_text().strip()
	else:
		print "no people rate"
		return ""

def getAuthorIntro(soup):
	author_intro = soup.find(text='作者简介')
	try:
		content = author_intro.parent.parent.next_sibling.next_sibling
		if content:
			content = content.find('div', class_='intro')
			[x.extract() for x in content.findAll('script')]
			[x.extract() for x in content.findAll('style')]
			if content.find('span', class_='short'):
				print content.find('span', class_='all hidden').get_text().strip()
				return content.find('span', class_='all hidden').get_text().strip()
			else:
				print content.get_text().strip()
				return content.get_text().strip()
		else:
			print "no author intro"
			return ""
	except:
		print "no author intro"
		return ""

def getRating(soup):
	rating = soup.find('strong',class_='ll rating_num ')
	if rating:
		print rating.get_text().strip()
		return rating.get_text().strip()
	else:
		print "no rating"
		return ""

def getPic(soup, ibsn):
	pic = soup.find('a', class_='nbg')
	if pic:
		pic_h = pic['href']
		file_name = "./img/" + str(ibsn) + ".jpg"
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
		pass_count = pass_count + 1
		print "pass"
		continue
	soup = BeautifulSoup(txt, 'html.parser')
	info = soup.find(id = 'info')
	isbn = getPages(info)
	#getPic(soup, isbn)




result = "pass number : " + str(pass_count)

fout.close()
