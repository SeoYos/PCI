# -*- coding:utf-8 -*-

from random import random,randint
from pylab import *
import math

def wineprice(rating,age):
    peak_age = rating-50

    # レーティングに基づく価格
    price = rating/2
    if age>peak_age:
        # ピークを過ぎると5年で駄目になる
        price = price*(5-(age-peak_age))
    else:
        # ピーク時には元価格の5倍になる
        price = price*(5*((age+1)/peak_age))
    if price<0: price=0
    return price

def wineset1():
    rows=[]
    for i in range(300):
        # 年齢とレーティングをランダムに生成
        rating=random()*50+50
        age=random()*50
        # 基準価格の取得
        price=wineprice(rating,age)
        # ノイズを加える
        price *=(random()*0.4+0.8)
        # データセットに追加
        rows.append({'input':(rating,age),
                    'result':price})
    return rows

def wineset2():
    rows=[]
    for i in range(300):
        rating=random()*50+50
        age=random()*50
        aisle=float(randint(1,20))
        bottlesize=[375.0,750.0,1500.0,3000.0][randint(0,3)]
        price=wineprice(rating,age)
        price *= (bottlesize/750)
        price *=(random()*0.9+0.2)
        rows.append({'input':(rating,age,aisle,bottlesize),
                    'result':price})
    return rows

def wineset3():
    rows=wineset1()
    for row in rows:
        if random()<0.5:
            # ワインがディスカウント店で購入された場合
            row['result']*=0.6
    return rows

# 類似度を定義する
def euclidean(v1,v2):
    d=0.0
    for i in range(len(v1)):
        d+=(v1[i]-v2[i])**2
    return math.sqrt(d)

def getdistances(data,vec1):
    distancelist=[]
    for i in range(len(data)):
        vec2=data[i]['input']
        distancelist.append((euclidean(vec1,vec2),i))
    distancelist.sort()
    return distancelist

def knnestimate(data,vec1,k=5):
    # 距離をソート済で得る
    dlist=getdistances(data,vec1)
    avg=0.0
    # 先頭k個の結果の平均を得る
    for i in range(k):
        idx=dlist[i][1]
        avg+=data[idx]['result']
    avg=avg/k
    return avg

# 反比例関数
def inverseweight(dist,num=1.0,const=0.1):
    return num/(dist+const)

# 減法（引算）関数
def subtractweight(dist,const=1.0):
    if dist>const:
        return 0
    else:
        return const-dist

# ガウス関数
def gaussian(dist,sigma=10.0):
    return math.e**(-dist**2/(2*sigma**2))

# 重み付けK近傍法
def weightedknn(data,vec1,k=5,weightf=gaussian):
    # 距離を得る
    dlist=getdistances(data,vec1)
    avg=0.0
    totalweight=0.0
    # 加重平均を得える
    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        avg+=weight*data[idx]['result']
        totalweight+=weight
    avg=avg/totalweight
    return avg

# クロス評価
def dividedata(data,test=0.05):
    trainset=[]
    testset=[]
    for row in data:
        if random()<test:
            testset.append(row)
        else:
            trainset.append(row)
    return trainset,testset

def testalgorithm(algf,trainset,testset):
    error=0.0
    for row in testset:
        guess=algf(trainset,row['input'])
        error+=(row['result']-guess)**2
    return error/len(testset)

def crossvalidate(algf,data,trials=100,test=0.05):
    error=0.0
    for i in range(trials):
        trainset,testset=dividedata(data,test)
        error+=testalgorithm(algf,trainset,testset)
    return error/trials

def rescale(data,scale):
    scaleddata=[]
    for row in data:
        scaled=[scale[i]*row['input'][i] for i in range(len(scale))]
        scaleddata.append({'input':scaled,'result':row['result']})
    return scaleddata

def createcostfunction(algf,data):
    def costf(scale):
        sdata=rescale(data,scale)
        return crossvalidate(algf,sdata,trials=10)
    return costf

weightdomain=[(0,20)]*4

def probguess(data,vec1,low,high,k=5,weightf=gaussian):
    dlist=getdistances(data,vec1)
    nweight=0.0
    tweight=0.0

    for i in range(k):
        dist=dlist[i][0]
        idx=dlist[i][1]
        weight=weightf(dist)
        v=data[idx]['result']

        # 点が範囲の中にあるか
        if v>=low and v<=high:
            nweight+=weight
        tweight+=weight
    if tweight==0: return 0

    # 確率は範囲の中にある重みをすべての重みで割ったもの
    return nweight/tweight

def cumulativegraph(data,vec1,high,k=5,weightf=gaussian):
    t1=arange(0.0,high,0.1)
    cprob=array([probguess(data,vec1,0,v,k,weightf) for v in t1])
    plot(t1,cprob)
    show()

def probabilitygraph(data,vec1,high,k=5,weightf=gaussian,ss=5.0):
    # 価格の範囲を形成
    t1=arange(0.0,high,0.1)

    # 範囲全体に渡り確率値を得る
    probs=[probguess(data,vec1,v,v+0.1,k,weightf) for v in t1]

    # 近接する確率のガウス関数荷重を加えてスムージング
    smoothed=[]
    for i in range(len(probs)):
        sv=0.0
        for j in range(0,len(probs)):
            dist=abs(i-j)*0.1
            weight=gaussian(dist,sigma=ss)
            sv+=weight*probs[j]
        smoothed.append(sv)
    smoothed=array(smoothed)

    plot(t1,smoothed)
    show()

