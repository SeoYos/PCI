# -*- coding: utf-8 -*-

import feedparser

rssurl="http://seopon.blog89.fc2.com/?xml"

fdp = feedparser.parse(rssurl)

for entry in fdp['entries']:
    title = entry['title']
    link  = entry['link']
    print "title:",title
    print "link: ",link

