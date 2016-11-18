import urllib2
from bs4 import *
import bs4

url_preffix_hiuben = 'https://book.douban.com/tag/%E7%BB%98%E6%9C%AC?start={}&type=T'
url_preffix_tuhuashu = 'https://book.douban.com/tag/%E5%9B%BE%E7%94%BB%E4%B9%A6?start={}&type=T'
url_preffix_tonghua = 'https://book.douban.com/tag/%E7%AB%A5%E8%AF%9D?start={}&type=T'
url_preffix_tongshu = 'https://book.douban.com/tag/%E7%AB%A5%E4%B9%A6?start={}&type=T'
url_preffix_ertongwenxue = 'https://book.douban.com/tag/%E5%84%BF%E7%AB%A5%E6%96%87%E5%AD%A6?start={}&type=T'
url_preffix_tonghuahuiben = 'https://book.douban.com/tag/%E7%AB%A5%E8%AF%9D%E7%BB%98%E6%9C%AC?start={}&type=T'
url_list = [url_preffix_hiuben, url_preffix_tuhuashu, url_preffix_tonghua, url_preffix_tongshu, url_preffix_ertongwenxue, url_preffix_tonghuahuiben]
fout = file("douban_list_new.txt", 'w')
log_file = file("douban_list.log", 'w')
links_set = set()

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

for url_preffix in url_list:
    for i in range(0,98):
        print('------------------------------------------------------------')
        page = i * 20
        log = url_preffix.format(page)
        print(log)
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        html = opener.open(url_preffix.format(page))
        txt = html.read()
        soup = BeautifulSoup(txt, 'html.parser')
        links = soup.findAll('a', class_='nbg')
        if not links:
            log_file.write(log + "\n find null links")
            log_file.write(txt)
        else :
            for j in links:
                if j['href'] not in links_set:
                    links_set.add(j['href'])

log_file.close()

for i in links_set:
	fout.write(i+'\n')

fout.close()
