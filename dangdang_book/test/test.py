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


def getDetailDescripe(soup):
    p_info = soup.find(id="detail_describe")
    series = ""
    isbn = ""
    pub_times = ""
    pages = ""
    words = ""
    pub_date = ""
    size = ""
    binding = ""
    if p_info:
        li_list = p_info.findAll("li")
        if li_list:
            try:
                for item in li_list:
                    item_str = str(item.get_text().strip())
                    if item_str.find("版 次") > -1:
                        pub_times = item_str.replace("版 次：", "")
                        continue
                    if item_str.find("页 数") > -1:
                        pages = item_str.replace("页 数：", "")
                        continue
                    if item_str.find("字 数") > -1:
                        words = item_str.replace("字 数：", "")
                        continue
                    if item_str.find("印刷时间") > -1:
                        pub_date = item_str.replace("印刷时间：", "")
                        continue
                    if item_str.find("开 本") > -1:
                        size = item_str.replace("开 本：", "")
                        continue
                    if item_str.find("包 装") > -1:
                        binding = item_str.replace("包 装：", "")
                        continue
                    if item_str.find("国际标准书号ISBN") > -1:
                        isbn = item_str.replace("国际标准书号ISBN：", "")
                        continue
                    if item_str.find("丛书名") > -1:
                        series = item_str.replace("丛书名：", "")
                print [series, isbn, pub_times, pages, words, pub_date, size, binding]
                return [series, isbn, pub_times, pages, words, pub_date, size, binding]
            except:
                pass
                return ["", "", "", "", "", "", "", ""]
        return ["", "", "", "", "", "", "", ""]
    else:
		return ["", "", "", "", "", "", "", ""]



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

def getDisAuthor(soup):
    name_tag = soup.find(id="author")
    if name_tag:
        try:
            name = str(name_tag.get_text()).strip().replace("作者:", "")
            return name
        except:
            return ""
    else:
        return ""

def getCountry(disAuthor):
    pattern1 = re.compile(r'.*\【(.+?)\】.*')
    pattern2 = re.compile(r'.*\[(.+?)\].*')
    match = pattern2.match(disAuthor)
    if match:
        print match.group(1)
        return match.group(1)
    else:
        match = pattern1.match(disAuthor)
        if match:
            print match.group(1)
            return match.group(1)
        else:
            return ""

def getAuthorAndTrans(soup):
    name_tag = soup.find(id="author")
    author = ""
    trans = ""
    previous = ""
    if name_tag:
        for item_l in name_tag.contents:
            if type(item_l).__name__ == "NavigableString":
                content =  str(item_l.string).strip()
                if content.find("译") > -1:
                    if content.find("编译") > -1:
                        content.replace("编译", "")
                    else:
                        content.replace("译", "")
                    trans = previous
                    previous = ""
                else:
                    if content.find("作者") > -1:
                        previous = previous + content.replace("作者:", "")
                    else:
                        if content:
                            author = author + previous + content
                            previous = ""
                        else:
                            previous = previous + ", " + content
            else:
                content = str(item_l.get_text()).strip()
                previous = previous + content
        author = author + previous
        return [author, trans]
    else:
        return ["", ""]

def getPublicator(soup):
    pub_tag = soup.find("span",{"dd_name": "出版社"})
    if pub_tag:
        pub_a = pub_tag.find("a")
        if pub_a:
            print str(pub_a.get_text()).strip()
            return str(pub_a.get_text()).strip()
        return ""
    else:
        return ""

def getPrice(soup):
    price_tag = soup.find(id="dd-price")
    if price_tag:
        print str(price_tag.get_text()).strip()
        return str(price_tag.get_text()).strip()
    else:
        return ""

def getEditorReco(soup):
    abstract_tag = soup.find(id="abstract")
    editor_reco = ""
    if abstract_tag:
        reco_tag = abstract_tag.find(id="abstract-all")
        if reco_tag:
            editor_reco = str(reco_tag.get_text()).strip()
        if not editor_reco:
            dis_tag = abstract_tag.find("div", class_="descrip")
            if dis_tag:
                editor_reco = str(dis_tag.get_text()).strip()
    print editor_reco
    return editor_reco

def getMediaReco(soup):
    content_tag = soup.find(id="mediaFeedback")
    if content_tag:
        media_tag = content_tag.find(id="mediaFeedback-textarea")
        if not media_tag:
            media_tag = content_tag.find("div", class_="descrip")
        try:
            content = media_tag.get_text().strip()
            print cleanStr(str(content))
            return cleanStr(str(content))
        except:
            return ""
    else:
        return ""

def getAuthorIntro(soup):
    content_tag = soup.find(id="authorIntroduction")
    if content_tag:
        media_tag = content_tag.find(id="authorIntroduction-textarea")
        if not media_tag:
            media_tag = content_tag.find("div", class_="descrip")
        try:
            content = media_tag.get_text().strip()
            print cleanStr(str(content))
            return cleanStr(str(content))
        except:
            return ""
    else:
        return ""

def getReviwsNumber(soup):
    num_tag = soup.find(id="comm_num_down")
    if num_tag:
        print str(num_tag.get_text()).strip()
        return str(num_tag.get_text()).strip()
    else:
        return ""

def getRank(soup):
    rank_tag = soup.find("span", {"dd_name": "图书排行榜排名"})
    if rank_tag:
        print str(rank_tag.get_text()).strip()
        return str(rank_tag.get_text()).strip()
    else:
        return ""

def getPic(soup, isbn):
    img_tag = soup.find(id="largePic")
    if img_tag:
        img_h = str(img_tag["src"])
        if img_h:
            file_name = "./img/" + isbn + ".jpg"
            try:
                urllib.urlretrieve(img_h, file_name)
            except:
                print "get pic error"

if 'linux' in sys.platform:
    dryscrape.start_xvfb()

test_count = 0

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
    #getDetailDescripe(soup)
    getPic(soup, str(test_count))
    test_count = test_count + 1

test_log.close()
result = "pass number : " + str(pass_count)

fout.close()
