# -*- coding: utf-8 -*-

import sys
import urllib2
from bs4 import BeautifulSoup

page=sys.argv[1]
#page='http://www.tk-game-diary.net/alllist_old.html'

c=urllib2.urlopen(page)
#c = open('./boadgame.html','r')
soup=BeautifulSoup(c.read(), "lxml")

f = open('link.txt','w')

for i in soup.find_all('a'):
    title=i.get_text()
    if len(title) > 1:
        f.write(title.encode('utf-8'))
        f.write("\n")
        print i.string

f.close()
