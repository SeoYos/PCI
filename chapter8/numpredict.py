# -*- coding:utf-8 -*-

from random import random,randint
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
