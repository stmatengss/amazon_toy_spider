import urllib2
from bs4 import *
import bs4

url_preffix2 = 'https://book.douban.com/tag/%E7%BB%98%E6%9C%AC?start={}&type=T'
fout = file("douban_list.txt", 'w')
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

for i in range(0,98):
    print('------------------------------------------------------------')
    page = i * 20
    log = 'start crawler douban book page {}'.format(i)
    print(log)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    html = opener.open(url_preffix2.format(page))
    txt = html.read()
    soup = BeautifulSoup(txt, 'html.parser')
    links = soup.findAll('a', class_='nbg')
    if not links:
        log_file.write(log + "\n find null links")
        log_file.write(txt)
    for j in links:
        if j['href'] not in links_set:
            links_set.add(j['href'])

log_file.close()

for i in links_set:
	fout.write(i+'\n')

fout.close()
