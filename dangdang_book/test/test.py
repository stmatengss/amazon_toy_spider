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
import dryscrape

fout = file("test_list.txt", 'r')
test_log = file("test.log.txt", 'w')
links_set = fout.readlines()
pass_count = 0
cu_count = 0

def cleanStr(in_str):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', in_str)
    return cleantext

def getISBN(p_info):
	if p_info:
		li_list = p_info.findAll("li")
		if li_list:
			try:
				for item in li_list:
					item_str = item.get_text().strip()
					if item_str.find("国际标准书号ISBN") > -1:
						print item_str.replace("国际标准书号ISBN：", "")
						return item_str.replace("国际标准书号ISBN：", "")
			except:
				return ""
			return ""
		return ""
	else:
		return ""



def getDetailDescripe(soup):
	p_info = soup.find(id="detail_describe")
	getISBN(p_info)

def getTitle(soup):
    name_tag = soup.find("div", class_="name_info")
    if name_tag:
        title_tag = name_tag.find("h1")
        if title_tag:
            try:
                title = title_tag.get_text().strip()
                print str(title)
                return str(title)
            except:
				return ""
        else:
            return ""
    else:
        return ""

def getComment(soup):
    name_tag = soup.find("div", class_="name_info")
    if name_tag:
        content_tag = name_tag.find("h2")
        if content_tag:
            try:
                content = content_tag.get_text().strip()
                print str(content)
                return str(content)
            except:
                return ""
        else:
            return ""
    else:
        return ""



def getContent(soup):
	content_tag = soup.find(id="content")
	if content_tag:
		dsc_tag = content_tag.find(id="content-textarea")
		if not dsc_tag:
			dsc_tag = content_tag.find("div", class_="descrip")
		try:
			content = dsc_tag.get_text().strip()
			print cleanStr(str(content))
			return cleanStr(str(content))
		except:
			return ""
	else:
		return ""

if 'linux' in sys.platform:
    dryscrape.start_xvfb()

for i in links_set:
    print "------------------------------------"
    print i
    txt = ""
    session = dryscrape.Session()
    session.set_attribute('auto_load_images', False)
    session.visit(i)
    response = session.body()
    soup = BeautifulSoup(response, "lxml")
    test_log.write(txt)
	#print soup
    #getDetailDescripe(soup)
    #getTitle(soup)
    #getContent(soup)
    getComment(soup)

test_log.close()
result = "pass number : " + str(pass_count)

fout.close()
