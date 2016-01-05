# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from bs4 import BeautifulStoneSoup
from janome.tokenizer import Tokenizer

feedlist=['http://headlines.yahoo.co.jp/rss/zdn_mkt-dom.xml',
          'http://headlines.yahoo.co.jp/rss/jct-dom.xml',
          'http://headlines.yahoo.co.jp/rss/wordleaf-dom.xml',
          'http://headlines.yahoo.co.jp/rss/withnews-dom.xml',
          'http://headlines.yahoo.co.jp/rss/asahik-dom.xml',
          'http://headlines.yahoo.co.jp/rss/asiap-dom.xml',
          'http://headlines.yahoo.co.jp/rss/at_s-dom.xml',
          'http://headlines.yahoo.co.jp/rss/cbn-dom.xml',
          'http://headlines.yahoo.co.jp/rss/wmap-dom.xml',
          'http://headlines.yahoo.co.jp/rss/san-dom.xml',
          'http://headlines.yahoo.co.jp/rss/sanspo-dom.xml',
          'http://headlines.yahoo.co.jp/rss/spnannex-dom.xml',
          'http://headlines.yahoo.co.jp/rss/sph-dom.xml',
          'http://headlines.yahoo.co.jp/rss/zeiricom-dom.xml',
          'http://headlines.yahoo.co.jp/rss/nishinp-dom.xml',
          'http://headlines.yahoo.co.jp/rss/nksports-dom.xml',
          'http://headlines.yahoo.co.jp/rss/agrinews-dom.xml',
          'http://headlines.yahoo.co.jp/rss/socra-dom.xml',
          'http://headlines.yahoo.co.jp/rss/videonewsv-dom.xml',
          'http://headlines.yahoo.co.jp/rss/fukushi-dom.xml',
          'http://headlines.yahoo.co.jp/rss/bengocom-dom.xml',
          'http://headlines.yahoo.co.jp/rss/doshin-dom.xml',
          'http://headlines.yahoo.co.jp/rss/mbsnews-dom.xml',
          'http://headlines.yahoo.co.jp/rss/rescuenow-dom.xml',
          'http://headlines.yahoo.co.jp/rss/rps-dom.xml',
          'http://headlines.yahoo.co.jp/rss/logmi-dom.xml']

#url="http://headlines.yahoo.co.jp/hl?a=20151221-00000086-zdn_mkt-soci"

def gettext(url):
    alist = []
    r = requests.get(url)
    soup=BeautifulSoup(r.text)
    #alist.append(soup.find('h1').text)
    alist+=separatewords(soup.find('h1').text)
    for p in soup.findAll('p'):
        try:
            alist+=separatewords(p.text)
        except:
            continue
    #    alist.append(p.text)
    return alist

def separatewords(text):
    wordlist = []
    t = Tokenizer()
    for token in t.tokenize(text):
        word=str(token).split('\t')[0]
        wordlist+=[word]
    return wordlist

def getarticlewords():
    allwords={}
    articlewords=[]
    articletitles=[]
    ec = 0
    # すべてのフィードをループする
    for feed in feedlist:
        r=requests.get(feed)
        soup=BeautifulStoneSoup(r.text)

        for i in soup.findAll('item'):
            if i.title in articletitles: continue

            # 単語を抽出する
            words=gettext(i.link.text)
            articlewords.append({})
            articletitles.append(i.title.text)

            # allwordsとarticlewordsのこの単語のカウントを増やす
            for word in words:
                allwords.setdefault(word,0)
                allwords[word]+=1
                articlewords[ec].setdefault(word,0)
                articlewords[ec][word]+=1
            ec+=1

    return allwords,articlewords,articletitles
