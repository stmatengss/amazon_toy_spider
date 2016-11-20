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
from selenium import webdriver

# 0:0-1, 1:3-6
option = 0
file_name = ["dangdang_list_02.txt", "dangdang_list_36.txt"]
age = ["0-2", "3-6"]
output_csv = ["dangdang_book_02.csv", "dangdang_book_36.csv"]
log_name = ["dangdang_book_02.log", "dangdang_book_36.log"]
pass_file_name = ["pass_url_02.txt", "pass_url_02_.txt"]



fout = file(file_name[option], 'r')
links_set = fout.readlines()

csvfile = file(output_csv[option], 'w')
csvfile.write(codecs.BOM_UTF8)
writer = csv.writer(csvfile)

log_file = file(log_name[option], 'w')

pass_file = file(pass_file_name[option], 'w')


cu_count = 0

contents_need = ['isbn', 'pic', 'title', 'con_reco', 'comment', 'brand' , 'series', 'author', 'author_origin', 'author_country', 'translator', 'publicator', 'author_prize', 'book_prize', 'raw_title', 'age', 'responsibility', 'lan', 'words', 'size', 'binding', 'pub_date', 'pub_times', 'pages', 'price', 'editor_reco', 'media_reco', 'author_intro', 'review_num', 'dangdang_rank']
line1 = ['ISBN', '封面图', '绘本名称', '内容', '评论', '图书品牌', '图书套装', '作者', '作者原名', '作者国别', '译者', '出版社', '作者获奖经历', '绘本获奖经历', '绘本原作名', '适合年龄', '责任编辑', '正文语种', '字数', '开本', '装帧', '出版时间', '版次', '页数/页', '定价/元', '编辑推荐', '媒体推荐', '作者简介', '当当评论数', '当当童书排名']
writer.writerow(line1)

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
                #print [series, isbn, pub_times, pages, words, pub_date, size, binding]
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
			return cleanStr(str(content))
		except:
			return ""
	else:
		return ""

def getCountry(soup):
    name_tag = soup.find(id="author")
    disAuthor = ""
    name = ""
    if name_tag:
        name = str(name_tag.get_text()).strip().replace("作者:", "")
    pattern1 = re.compile(r'.*\【(.+?)\】.*')
    pattern2 = re.compile(r'.*\[(.+?)\].*')
    pattern3 = re.compile(r'.*\（(.+?)\）.*')
    pattern_list = [pattern1, pattern2, pattern3]
    for pattern in pattern_list:
        match = pattern.match(name)
        if match:
            return match.group(1)
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
                        if content and content != "，":
                            author = author + previous + content
                            previous = ""
                        else:
                            previous = previous + " " + content
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
            return str(pub_a.get_text()).strip()
        return ""
    else:
        return ""

def getPrice(soup):
    o_price_tag = soup.find(id="original-price")
    if o_price_tag:
        return str(o_price_tag.get_text()).strip()
    price_tag = soup.find(id="dd-price")
    if price_tag:
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
    return editor_reco

def getMediaReco(soup):
    content_tag = soup.find(id="mediaFeedback")
    if content_tag:
        media_tag = content_tag.find(id="mediaFeedback-textarea")
        if not media_tag:
            media_tag = content_tag.find("div", class_="descrip")
        try:
            content = media_tag.get_text().strip()
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
            return cleanStr(str(content))
        except:
            return ""
    else:
        return ""

def getReviwsNumber(soup):
    num_tag = soup.find(id="comm_num_down")
    if num_tag:
        return str(num_tag.get_text()).strip()
    else:
        return ""

def getRank(soup):
    rank_tag = soup.find("span", {"dd_name": "图书排行榜排名"})
    if rank_tag:
        return str(rank_tag.get_text()).strip()
    else:
        return ""

def getPic(soup, lines_map):
    lines_map[contents_need[1]] = "miss"
    if not lines_map["isbn"]:
        return
    img_tag = soup.find(id="largePic")
    if img_tag:
        img_h = str(img_tag["src"])
        if img_h:
            file_name = "./img/" + lines_map["isbn"] + ".jpg"
            try:
                urllib.urlretrieve(img_h, file_name)
                lines_map[contents_need[1]] = "ok"
            except:
                print "get pic error"

def initMap():
    lines_map = {}
    c_len = len(contents_need)
    for i in range(0, c_len):
        lines_map[contents_need[i]] = ''
    lines_map['age'] = age[option]
    return lines_map

def write2line(lines_map):
    line = []
    c_len = len(contents_need)
    for i in range(0, c_len):
        line.append(lines_map[contents_need[i]])
    return line

driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550)
log_file.write("null link")
for i in links_set:
    print "------------------------------------"
    print i
    txt = ""
    wait_time = 1
    while(True):
        time.sleep(wait_time)
        try:
            driver.get(i)
            response = driver.page_source
            break
        except:
            print "Unexpected error:", sys.exc_info()[0]
            print "wait time :" + str(wait_time)
            wait_time = wait_time * 2
            pass
    if not response:
        print "null"
        pass_file.write(i + "       null \n")
        continue
    soup = BeautifulSoup(response, "lxml")
    lines_map = initMap()
    [series, isbn, pub_times, pages, words, pub_date, size, binding] = getDetailDescripe(soup)
    lines_map[contents_need[6]] = series
    lines_map[contents_need[0]] = isbn
    lines_map[contents_need[22]] = pub_times
    lines_map[contents_need[23]] = pages
    lines_map[contents_need[18]] = words
    lines_map[contents_need[21]] = pub_date
    lines_map[contents_need[19]] = size
    lines_map[contents_need[20]] = binding
    getPic(soup, lines_map)
    lines_map[contents_need[2]] = getTitle(soup)
    lines_map[contents_need[3]] = getContent(soup)
    lines_map[contents_need[4]] = getComment(soup)
    [author, translator] = getAuthorAndTrans(soup)
    lines_map[contents_need[7]] = author
    lines_map[contents_need[10]] = translator
    lines_map[contents_need[9]] = getCountry(soup)
    lines_map[contents_need[11]] = getPublicator(soup)
    lines_map[contents_need[24]] = getPrice(soup)
    lines_map[contents_need[25]] = getEditorReco(soup)
    lines_map[contents_need[26]] = getMediaReco(soup)
    lines_map[contents_need[27]] = getAuthorIntro(soup)
    lines_map[contents_need[28]] = getReviwsNumber(soup)
    lines_map[contents_need[29]] = getRank(soup)
    line = write2line(lines_map)
    line.append(i)
    writer.writerow(line)
    cu_count = cu_count + 1
    print cu_count
    if cu_count > 100:
        break

driver.quit()
fout.close()
csvfile.close()
log_file.close()
pass_file.close()
