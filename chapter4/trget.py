# -*- coding: utf-8 -*-

import sys
import urllib2
from bs4 import BeautifulSoup

page=sys.argv[1]
tag="tr"
#tag=sys.argv[2]
#page='http://www.tk-game-diary.net/alllist_old.html'

c=urllib2.urlopen(page)
soup=BeautifulSoup(c.read(), "lxml")

f = open('%s.txt' % tag,'w')

for i in soup.find_all(tag):
    f.write(i.encode('utf-8'))
    f.write("\n")
    print i

f.close()
