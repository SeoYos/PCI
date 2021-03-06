# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin
import sqlite3
import re
import nn
mynet=nn.searchnet('nn.db')

# 無視すべき単語のリストを作る
ignorewords=set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it'])

class crawler:
    # データベースの名前でクローラーを初期化する
    def __init__(self,dbname):
        self.con=sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def dbcommit(self):
        self.con.commit()

    # エントリIDを取得したり、それが存在しない場合には追加
    # するための補助関数
    def getentryid(self,table,field,value,createnew=True):
        cur=self.con.execute(
            "select rowid from %s where %s='%s'" % (table,field,value))
        res=cur.fetchone()
        if res==None:
            cur=self.con.execute(
                "insert into %s (%s) values ('%s')" % (table,field,value))
            return cur.lastrowid
        else:
            return res[0]

    # 個々のページをインデックスする
    def addtoindex(self,url,soup):
        if self.isindexed(url): return
        print 'Indexing ' + url

        # 個々の単語を取得する
        text=self.gettextonly(soup)
        words=self.separateword(text)

        # URL idを取得する
        urlid=self.getentryid('urllist','url',url)

        # それぞれの単語と、このurlのリンク
        for i in range(len(words)):
            word=words[i]
            if word in ignorewords: continue
            wordid=self.getentryid('wordlist','word',word)
            self.con.execute("insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)" % (urlid,wordid,i))

    # HTMLのページからタグのない状態でテキストを抽出する
    def gettextonly(self,soup):
        v=soup.string
        if v==None:
            c=soup.contents
            resulttext=''
            for t in c:
                subtext=self.gettextonly(t)
                resulttext+=subtext+'\n'
            return resulttext
        else:
            return v.strip()

    # 空白以外の文字で単語を分割する
    def separateword(self,text):
        splitter=re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s!='']

    # URLがすでにインデックスされていたらtrueを返す
    def isindexed(self,url):
        u=self.con.execute \
            ("select rowid from urllist where url='%s'" % url).fetchone()
        if u!=None:
            v=self.con.execute(
                'select * from wordlocation where urlid=%d' % u[0]).fetchone()
            if v!=None: return True
        return False

    # 2つのページの間にリンクを付け加える
    def addlinkref(self,urlFrom,urlTo,linkText):
        words=self.separateword(linkText)
        fromid=self.getentryid('urllist','url',urlFrom)
        toid=self.getentryid('urllist','url',urlTo)
        if fromid==toid: return
        cur=self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid,toid))
        linkid=cur.lastrowid
        for word in words:
            if word in ignorewords: continue
            wordid=self.getentryid('wordlist','word',word)
            self.con.execute("insert into linkwords(linkid,wordid) values (%d,%d)" % (linkid,wordid))


    # ページのリストを受け取り、与えられた深さで幅優先の検索を行い
    # ページをインデクシングする
    def crawl(self,pages,depth=2):
        for i in range(depth):
            newpages=set()
            for page in pages:
                try:
                    c=urllib2.urlopen(page)
                except:
                    print "Could not open %s" % page
                    continue
                soup=BeautifulSoup(c.read())
                self.addtoindex(page,soup)

                links=soup('a')
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url=urljoin(page,link['href'])
                        if url.find("'")!=-1: continue
                        url=url.split('#')[0] # アンカーを取り除く
                        if url[0:4]=='http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText=self.gettextonly(link)
                        self.addlinkref(page,url,linkText)

                self.dbcommit()
            pages=newpages

    # データベースのテーブルを作る
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create index wordidx on wordlist(word)')
        self.con.execute('create index urlidx on urllist(url)')
        self.con.execute('create index wordurlidx on wordlocation(wordid)')
        self.con.execute('create index urltoidx on link(toid)')
        self.con.execute('create index urlfromidx on link(fromid)')
        self.dbcommit()

    def calculatepagerank(self,iterations=20):
        # 現在のページランクのテーブルを削除
        self.con.execute('drop table if exists pagerank')
        self.con.execute('create table pagerank(urlid primary key,score)')

        # すべてのURLのPageRankを1で初期化する
        self.con.execute('insert into pagerank select rowid, 1.0 from urllist')
        self.dbcommit()

        for i in range(iterations):
            print "Iteration %d" % (i)
            for (urlid,) in self.con.execute('select rowid from urllist'):
                pr=0.15

                # このページにリンクしているすべてのページをループする
                for (linker,) in self.con.execute(
                'select distinct fromid from link where toid=%d' % urlid):
                    # linkerのPageRankを取得する
                    linkingpr=self.con.execute(
                    'select score from pagerank where urlid=%d' % linker).fetchone()[0]
                    # linkerからリンクの合計を取得する
                    linkingcount=self.con.execute(
                    'select count(*) from link where fromid=%d' % linker).fetchone()[0]
                    pr+=0.85*(linkingpr/linkingcount)
                self.con.execute(
                'update pagerank set score=%f where urlid=%d' % (pr,urlid))
            self.dbcommit()



class searcher:
    def __init__(self,dbname):
        self.con=sqlite3.connect(dbname)

    def __del__(self):
        self.con.close()

    def nnscore(self,rows,wordids):
        # ユニークなURL IDをソートされたリストとして取得する
        urlids=[urlid for urlid in set([row[0] for row in rows])]
        nnres=mynet.getresult(wordids,urlids)
        scores=dict([(urlids[i],nnres[i]) for i in range(len(urlids))])
        return self.normalizescores(scores)

    def getmatchrows(self,q):
        # クエリを作るための文字列
        fieldlist='w0.urlid'
        tablelist=''
        clauselist=''
        wordids=[]

        # 空白で単語を分ける
        words=q.split(' ')
        tablenumber=0

        for word in words:
            # 単語のIDを取得
            wordrow=self.con.execute(
                "select rowid from wordlist where word='%s'" % word.lower()).fetchone()
            if wordrow!=None:
                wordid=wordrow[0]
                wordids.append(wordid)
                if tablenumber>0:
                    tablelist+=','
                    clauselist+=' and '
                    clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumber-1,tablenumber)
                fieldlist+=',w%d.location' % tablenumber
                tablelist+='wordlocation w%d' % tablenumber
                clauselist+='w%d.wordid=%d' % (tablenumber,wordid)
                tablenumber+=1

        # 分割されたパーツからクエリを構築
        if tablenumber == 0: return None,wordids
        fullquery='select %s from %s where %s' % (fieldlist,tablelist,clauselist)
        cur=self.con.execute(fullquery)
        rows=[row for row in cur]

        return rows,wordids

    def getscoredlist(self,rows,wordids):
        totalscores=dict([(row[0],0) for row in rows])

        # ここには後ほどスコアリング関数を入れる
        weights=[(1.0,self.locationscore(rows)),(1.0,self.frequencyscore(rows)),\
                 (1.0,self.pagerankscore(rows)),(1.0,self.linktextscore(rows,wordids))]

        for (weight,scores) in weights:
            for url in totalscores:
                totalscores[url]+=weight*scores[url]
        return totalscores

    def geturlname(self,id):
        return self.con.execute(
            "select url from urllist where rowid=%d" %id).fetchone()[0]

    def query(self,q):
        rows,wordids=self.getmatchrows(q)
        if rows == None: return
        scores=self.getscoredlist(rows,wordids)
        rankedscores=[(score,url) for (url,score) in scores.items()]
        rankedscores.sort()
        rankedscores.reverse()
        for (score,urlid) in rankedscores[0:10]:
            print '%f\t%s' % (score,self.geturlname(urlid))

        return wordids,[r[1] for r in rankedscores[0:10]]

    # 単語の頻度
    def frequencyscore(self,rows):
        counts=dict([(row[0],0) for row in rows])
        for row in rows: counts[row[0]]+=1
        return self.normalizescores(counts)

    # ドキュメント中での位置
    def locationscore(self,rows):
        locations=dict([(row[0],1000000) for row in rows])
        for row in rows:
            loc=sum(row[1:])
            if loc<locations[row[0]]: locations[row[0]]=loc
        return self.normalizescores(locations,smallIsBetter=1)

    # 単語間の距離
    def distancescore(self,rows):
        # 単語が１つしかない場合、全員が勝者！
        if len(rows[0])<=2: return dict([(row[0],1.0) for row in rows])

        # 大きな値でディクショナリを初期化する
        mindistance=dict([(row[0],1000000) for row in rows])

        for row in rows:
            dist=sum([abs(row[i]-row[i-1]) for i in range(2,len(row))])
            if dist<mindistance[row[0]]: mindistance[row[0]]=dist
        return self.normalizescores(mindistance,smallIsBetter=1)

    # インバウンドリンク（被リンク）を数える
    def inboundlinkscore(self,rows):
        uniqueurls=set([row[0] for row in rows])
        inboundcount=dict([(u,self.con.execute( \
            'select count(*) from link where toid=%d' % u).fetchone()[0]) \
            for u in uniqueurls])
        return self.normalizescores(inboundcount)

    # ページランクスコア
    def pagerankscore(self,rows):
        pageranks=dict([(row[0],self.con.execute('select score from pagerank where urlid=%d' % row[0]).fetchone()[0]) for row in rows])
        maxrank=max(pageranks.values())
        normalizescores=dict([(u,float(l)/maxrank) for (u,l) in pageranks.items()])
        return normalizescores

    # リンクのテキストを利用する
    def linktextscore(self,rows,wordids):
        linkscores=dict([(row[0],0) for row in rows])
        for wordid in wordids:
            cur=self.con.execute('select link.fromid,link.toid from linkwords,link where wordid=%d and linkwords.linkid=link.rowid' % wordid)
            for (fromid,toid) in cur:
                if toid in linkscores:
                    pr=self.con.execute('select score from pagerank where urlid=%d' % fromid).fetchone()[0]
                    linkscores[toid]+=pr
        maxscore=max(linkscores.values())
        normalizescores=dict([(u,float(l)/maxscore) for (u,l) in linkscores.items()])
        return normalizescores

    # 正規化関数 p73
    def normalizescores(self,scores,smallIsBetter=0):
        vsmall=0.00001 # 0で除算することによるエラーを回避する
        if smallIsBetter:
            minscore=min(scores.values())
            return dict([(u,float(minscore)/max(vsmall,l)) for (u,l)\
                        in scores.items()])
        else:
            maxscore=max(scores.values())
            if maxscore==0: maxscore=vsmall
            return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

