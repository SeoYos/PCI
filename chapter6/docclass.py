# -*- coding: utf-8 -*-

import re
import math
import sqlite3

def sampletrain(cl):
    cl.train('Nobody owns the water.', 'good')
    cl.train('the quick rabbit jumps fences', 'good')
    cl.train('buy pharmaceuticals now', 'bad')
    cl.train('make quick money at the online casino', 'bad')
    cl.train('the quick brown fox jumps', 'good')

def getwords(doc):
    splitter=re.compile('\\W*')
    # 単語を非アルファベットの文字で分割する
    words=[s.lower() for s in splitter.split(doc)
           if len(s)>2 and len(s)<20]
    # ユニークな単語のみの集合を返す
    return dict([(w,1) for w in words])

class classifier:
    def __init__(self,getfeatures,filename=None):
        self.fc={}
        # それぞれのカテゴリの中のドキュメント数
        self.cc = {}
        self.getfeatures=getfeatures

    def setdb(self,dbfile):
        self.con=sqlite3.connect(dbfile)
        self.con.execute('create table if not exists fc(feature,category,count)')
        self.con.execute('create table if not exists cc(category,count)')

    # 特徴/カテゴリのカウントを増やす
    def incf(self,f,cat):
        count=self.fcount(f,cat)
        if count==0:
            self.con.execute("insert into fc values ('%s','%s',1)" % (f,cat))
        else:
            self.con.execute("update fc set count=%d where feature='%s' and category='%s'" % (count+1,f,cat))

    # あるカテゴリの中に特徴が現れた数
    def fcount(self,f,cat):
        res=self.con.execute("select count from fc where feature='%s' and category='%s'" % (f,cat)).fetchone()
        if res==None: return 0
        else: return float(res[0])

    # カテゴリのカウントを増やす
    def incc(self,cat):
        count=self.catcount(cat)
        if count==0:
            self.con.execute("insert into cc values ('%s',1)" % (cat))
        else:
            self.con.execute("update cc set count=%d where category='%s'" % (count+1,cat))

    # あるカテゴリ中のアイテムの数
    def catcount(self,cat):
        res=self.con.execute("select count from cc where category='%s'" % (cat)).fetchone()
        if res==None: return 0
        else: return float(res[0])

    # すべてのカテゴリたちのリスト
    def categories(self):
        cur=self.con.execute('select category from cc')
        return [d[0] for d in cur]

    # アイテムたちの総数
    def totalcount(self):
        res=self.con.execute('select sum(count) from cc').fetchone()
        return res[0]

    def train(self,item,cat):
        features=self.getfeatures(item)
        # このカテゴリの中の特徴たちのカウントを増やす
        for f in features:
            self.incf(f,cat)
        # このカテゴリのカウントを増やす
        self.incc(cat)
        self.con.commit()

    def fprob(self,f,cat):
        if self.catcount(cat)==0: return 0
        # このカテゴリの中にこの特徴が出現する回数を、
        # このカテゴリの中のアイテムの総数で割る
        return self.fcount(f,cat)/self.catcount(cat)

    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        # 現在の確率を計算する
        basicprob=prf(f,cat)

        # この特徴がすべてのカテゴリ中に出現する数を数える
        totals=sum([self.fcount(f,c) for c in self.categories()])

        # 重み付けした平均を計算
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp

class naivebayes(classifier):
    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.thresholds={}

    def setthreshold(self,cat,t):
        self.thresholds[cat]=t

    def getthreshold(self,cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]

    def classify(self,item,default=None):
        probs={}
        # もっとも確率の高いカテゴリを探す
        max=0.0
        for cat in self.categories():
            probs[cat]=self.prob(item,cat)
            if probs[cat]>max:
                max=probs[cat]
                best=cat

        # 確率がしきい値*2番目にベストなものを超えているか確認する
        for cat in probs:
            if cat==best: continue
            if probs[cat]*self.getthreshold(best)>probs[best]: return default
        return best

    def docprob(self,item,cat):
        features=self.getfeatures(item)
        # すべての特徴の確率を掛け合わせる
        p=1
        for f in features: p*=self.weightedprob(f,cat,self.fprob)
        return p

    def prob(self,item,cat):
        catprob=self.catcount(cat)/self.totalcount()
        docprob=self.docprob(item,cat)
        return docprob*catprob

class fisherclassifier(classifier):

    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.minimums={}

    def setminimum(self,cat,min):
        self.minimums[cat]=min

    def getminimum(self,cat):
        if cat not in self.minimums: return 0
        return self.minimums[cat]

    def classify(self,item,default=None):
        # もっともよい結果を探してループする
        best=default
        max=0.0
        for c in self.categories():
            p=self.fisherprob(item,c)
            # 下限値を超えていることを確認する
            if p>self.getminimum(c) and p>max:
                best=c
                max=p
        return best

    def cprob(self, f, cat):
        # このカテゴリの中でこの特徴の頻度
        clf=self.fprob(f,cat)
        if clf==0: return 0

        # すべてのカテゴリの中でこの特徴の頻度
        freqsum=sum([self.fprob(f,c) for c in self.categories()])
        # 確率はこのカテゴリでの頻度を全体の頻度で割ったもの
        p=clf/(freqsum)
        return p

    def fisherprob(self,item,cat):
        # すべての確率を掛け合わせる
        p=1
        features=self.getfeatures(item)
        for f in features:
            p*=(self.weightedprob(f,cat,self.cprob))

        # 自然対数を取り-2を掛け合わせる
        fscore=-2*math.log(p)

        return self.invchi2(fscore,len(features)*2)

    def invchi2(self,chi,df):
        m = chi / 2.0
        sum = term = math.exp(-m)
        for i in range(1, df/2):
            term *= m / i
            sum += term

        return min(sum, 1.0)
