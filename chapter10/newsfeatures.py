# -*- coding:utf-8 -*-

import requests
from numpy import *
from bs4 import BeautifulSoup
from bs4 import BeautifulStoneSoup
from janome.tokenizer import Tokenizer

feedlist=['http://headlines.yahoo.co.jp/rss/zdn_mkt-dom.xml',
          'http://headlines.yahoo.co.jp/rss/jct-dom.xml',
          'http://headlines.yahoo.co.jp/rss/wordleaf-dom.xml',
          'http://headlines.yahoo.co.jp/rss/withnews-dom.xml',
          'http://headlines.yahoo.co.jp/rss/asahik-dom.xml']
'''
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
'''
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

def makematrix(allw,articlew):
    wordvec=[]

    # 一般的だけど、一般的すぎない単語のみを利用する
    for w,c in allw.items():
        if c>3 and c<len(articlew)*0.6:
            wordvec.append(w)

    # 単語の行列を作る
    l1 = [[(word in f and f[word] or 0) for word in wordvec] for f in articlew]
    return l1,wordvec

def showfeatures(w,h,titles,wordvec,out='features.txt'):
    outfile=file(out,'w')
    pc,wc=shape(h)
    toppatterns=[[] for i in range(len(titles))]
    patternnames=[]

    # すべての特徴をループする
    for i in range(pc):
        slist=[]
        # 単語とその重みのリストを作る
        for j in range(wc):
            slist.append((h[i,j],wordvec[j]))
        # 単語のリストを逆順にする
        slist.sort()
        slist.reverse()

        # 最初の6つの要素を出力する
        n=[s[1] for s in slist[0:6]]
        outfile.write('[ \'')
        for wd in n:
            outfile.write(wd+'\' \'')
        outfile.write(']\n')
        #outfile.write(str(n)+'\n')
        patternnames.append(n)

        # この特徴の記事のリストを作る
        flist=[]
        for j in range(len(titles)):
            # 記事をその重みとともに加える
            flist.append((w[j,i],titles[j]))
            toppatterns[j].append((w[j,i],i,titles[j]))

        # リストを逆にソートする
        flist.sort()
        flist.reverse()

        # 上位３つの記事を表示する
        for f in flist[0:3]:
            outfile.write(str(f[0])+' ')
            outfile.write(f[1].encode('utf-8')+'\n')
        outfile.write('\n')

    outfile.close()
    # 後々のためにパターンの名前を返す
    return toppatterns,patternnames

def showarticles(titles,toppatterns,patternnames,out='articles.txt'):
    outfile=file(out,'w')
    # すべての記事をループする
    for j in range(len(titles)):
        outfile.write(titles[j].encode('utf-8')+'\n')

        # この記事たちの特徴を取得しソートする
        toppatterns[j].sort()
        toppatterns[j].reverse()

        # 上位３パターンを出力する
        for i in range(3):
            outfile.write(str(toppatterns[j][i][0])+' ')
            for a_pattern in patternnames[toppatterns[j][i][1]]:
                outfile.write('\''+a_pattern+'\' ')
            outfile.write('\n')
        outfile.write('\n')
    outfile.close()
