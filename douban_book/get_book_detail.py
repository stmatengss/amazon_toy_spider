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
csvfile = file('douban_book.csv', 'wb')
log_file = file('douban_book.log', 'w')
pass_link = file('pass_link.txt', 'w')
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile)
pass_count = 0
cu_count = 0

contents_need = ['isbn', 'figure', 'title', 'content_into', 'rate_num', 'brand' , 'series', 'author', 'author_origin', 'author_country', 'tranlator', 'publicator', 'author_prize', 'book_prize', 'raw_title', 'age', 'responsibility', 'lan', 'words', 'size', 'binding', 'pub_date', 'pub_times', 'pages', 'price', 'editor_reco', 'media_reco', 'author_intro', 'douban_rating']

line1 = ['ISBN', '封面图', '绘本名称', '内容', '评论', '图书品牌', '图书套装', '作者', '作者原名', '作者国别', '译者', '出版社', '作者获奖经历', '绘本获奖经历', '绘本原作名', '适合年龄', '责任编辑', '正文语种', '字数', '开本', '装帧', '出版时间', '版次', '页数/页', '定价/元', '编辑推荐', '媒体推荐', '作者简介', '豆瓣评分']
writer.writerow(line1)

print len(contents_need)

def initMap():
    lines_map = {}
    c_len = len(contents_need)
    for i in range(0, c_len):
        lines_map[contents_need[i]] = ''
    return lines_map

def getTitle(soup):
    return soup.title.string.replace("(豆瓣)",'')

def getCountry(name):
    country = getCountry1(name)
    if country:
        return country
    else:
        country = getCountry2(name)
        return country

def getCountry1(name):
	pattern = re.compile(r'\((.+)\)')
	match = pattern.match(name)
	if match:
		return match.group(1)
	else:
		return ""

def getCountry2(name):
	pattern = re.compile(r'\[(.+)\]')
	match = pattern.match(name)
	if match:
		return match.group(1)
	else:
		return ""

def getAuthor(info):
	name = info.find(text=' 作者')
	try:
		return name.parent.next_sibling.next_sibling.get_text().strip()
	except:
		return ""

def getTranslator(info):
	name = info.find(text=' 译者')
	try:
		return name.parent.next_sibling.next_sibling.get_text().strip()
	except:
		return ""

def getPublication(info):
	pub = info.find(text='出版社:')
	try:
		return pub.parent.next_sibling.strip()
	except:
		return ""

def getRawTitle(info):
	r_title = info.find(text='原作名:')
	try :
		return r_title.parent.next_sibling.strip()
	except:
		return ""

def getBinding(info):
	bind = info.find(text='装帧:')
	try:
		return bind.parent.next_sibling.strip()
	except:
		return ""

def getPubDate(info):
	date = info.find(text='出版年:')
	try:
		return date.parent.next_sibling.strip()
	except:
		return ""

def getPages(info):
	pages = info.find(text='页数:')
	try:
		return pages.parent.next_sibling.strip()
	except:
		return ""

def getPrice(info):
	price = info.find(text='定价:')
	try:
		return price.parent.next_sibling.strip()
	except:
		return ""

def getSeries(info):
	series = info.find(text='丛书:')
	try:
		return series.parent.next_sibling.next_sibling.get_text().strip()
	except:
		return ""

def getISBN(info):
	isbn = info.find(text='ISBN:')
	try:
		return isbn.parent.next_sibling.strip()
	except:
		return ""

def getinfo(soup, line_map):
    info = soup.find(id = 'info')
    line_map[contents_need[0]] = getISBN(info)
    line_map[contents_need[6]] = getSeries(info)
    line_map[contents_need[7]] = getAuthor(info)
    line_map[contents_need[9]] = getCountry(line_map[contents_need[7]])
    line_map[contents_need[10]] = getTranslator(info)
    line_map[contents_need[11]] = getPublication(info)
    line_map[contents_need[14]] = getRawTitle(info)
    line_map[contents_need[20]] = getBinding(info)
    line_map[contents_need[21]] = getPubDate(info)
    line_map[contents_need[23]] = getPages(info)
    line_map[contents_need[23]] = getPrice(info)

def getContent(soup):
	content_intro = soup.find(id = 'link-report')
	if content_intro :
		[x.extract() for x in content_intro.findAll('script')]
		[x.extract() for x in content_intro.findAll('style')]
		if content_intro.find('span', class_='short'):
			return content_intro.find('span', class_='all hidden').get_text().strip()
		else:
			return content_intro.get_text().strip()
	else:
		return ""

def getRatingPeople(soup):
	rates_num = soup.find('a', class_='rating_people')
	if rates_num:
		number = rates_num.find('span')
		return number.get_text().strip()
	else:
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
				return content.find('span', class_='all hidden').get_text().strip()
			else:
				return content.get_text().strip()
		else:
			return ""
	except:
		return ""

def getRating(soup):
	rating = soup.find('strong',class_='ll rating_num ')
	if rating:
		return rating.get_text().strip()
	else:
		return ""

def getPic(soup, ibsn):
	pic = soup.find('a', class_='nbg')
	if pic:
		pic_h = pic['href']
		file_name = "./img/" + str(ibsn) + ".jpg"
		urllib.urlretrieve(pic_h, file_name)

def write2line(lines_map):
    line = []
    c_len = len(contents_need)
    for i in range(0, c_len):
        line.append(lines_map[contents_need[i]])
    return line

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
    line_map = initMap()
    getinfo(soup, line_map)
    line_map[contents_need[2]] = getTitle(soup)
    line_map[contents_need[3]] = getContent(soup)
    line_map[contents_need[4]] = getRatingPeople(soup)
    line_map[contents_need[27]] = getAuthorIntro(soup)
    line_map[contents_need[28]] = getRating(soup)
    #getPic(soup, line_map[contents_need[0]])
    line = write2line(line_map)
    writer.writerow(line)
    cu_count = cu_count + 1


result = "pass number : " + str(pass_count)
print result
log_file.write(result)

fout.close()
csvfile.close()
log_file.close()
pass_link.close()
