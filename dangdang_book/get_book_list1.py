import urllib2
import time
from bs4 import *
import bs4
import dryscrape
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#url_preffix_1 = 'http://search.dangdang.com/?key=%CD%AF%CA%E9&category_path=01.41.01.00.00.00&page_index={}'
#1-9,0-2
url_preffix_2 = 'http://search.dangdang.com/?key=%CD%AF%CA%E9&category_path=01.41.02.00.00.00&page_index={}' #1-80, 3-6
url_list = [url_preffix_2]
fout1 = file("dangdang_list_36.txt", 'a')
#fout2 = file("dangdang_list_36.txt", 'w')
#file_list = [fout1, fout2]
log_file = file("dangdang_list36.log", 'w')
links_set = set()
index = [27]

if 'linux' in sys.platform:
    dryscrape.start_xvfb()

for url_preffix in url_list:
    for i in index:
        print('------------------------------------------------------------')
        log = url_preffix.format(i)
        print(log)
        '''
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        txt = ""
        interv = 1

        while(True):
            time.sleep(interv)
            try:
                html = opener.open(url_preffix.format(i))
                txt = html.read()
                break
            except:
                interv = interv * 2
                print "still wait" + str(interv)
                pass
        '''
        session = dryscrape.Session()
        session.set_attribute('auto_load_images', False)
        session.visit(url_preffix.format(i))
        response = session.body()
        soup = BeautifulSoup(response, "lxml")
        links = soup.findAll('a', {"name": "itemlist-title"})
        if not links:
            log_file.write(log + "\n find null links")
            print "null link"
        else :
            for j in links:
                if str(j['href']) not in links_set:
                    links_set.add(str(j['href']))

log_file.close()

for i in links_set:
	fout1.write(i+'\n')

fout1.close()
