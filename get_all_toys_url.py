import urllib2
from bs4 import *
import bs4

url_preffix1 = 'https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A647070051%2Cn%3A%21647071051%2Cn%3A1982054051&page={}&sort=price-desc-rank'
url_preffix2 = 'https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A647070051%2Cn%3A%21647071051%2Cn%3A1982054051&page={}&sort=price-asc-rank'

fout = file("list", 'w')

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

for i in range(1,300):
	opener = urllib2.build_opener()
	opener.addheaders = [('User-agent', 'Mozilla/5.0')]
	html = opener.open(url_preffix2.format(i))
	# html = urllib2.urlopen(url_preffix2.format(i))
	txt = html.read()
	if i % 20 == 0:
		print (i/20)
	soup = BeautifulSoup(txt, 'html.parser')
	links = soup.findAll("a", class_='a-link-normal s-access-detail-page  a-text-normal')
	for j in links:
		if j['href'] not in links_set:
			links_set.add(j['href'])

for i in links_set:
	fout.write(i+'\n')

fout.close()




