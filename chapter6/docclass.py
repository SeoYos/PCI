# -*- coding: utf-8 -*-

import re
import math

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

    # 特徴/カテゴリのカウントを増やす
    def incf(self,f,cat):
        self.fc.setdefault(f,{})
        self.fc[f].setdefault(cat,0)
        self.fc[f][cat]+=1

    # カテゴリのカウントを増やす
    def incc(self,cat):
        self.cc.setdefault(cat,0)
        self.cc[cat]+=1

    # あるカテゴリの中に特徴が現れた数
    def fcount(self,f,cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    # あるカテゴリ中のアイテムの数
    def catcount(self,cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0

    # アイテムたちの総数
    def totalcount(self):
        return sum(self.cc.values())

    # すべてのカテゴリたちのリスト
    def categories(self):
        return self.cc.keys()

    def train(self,item,cat):
        features=self.getfeatures(item)
        # このカテゴリの中の特徴たちのカウントを増やす
        for f in features:
            self.incf(f,cat)
        # このカテゴリのカウントを増やす
        self.incc(cat)

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