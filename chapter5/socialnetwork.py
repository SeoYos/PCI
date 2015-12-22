# -*- coding: utf-8 -*-

import math
from PIL import Image,ImageDraw

people=['Charlie', 'Augustus', 'Veruca', 'Violet', 'Mike', 'Joe', 'Willy', 'Miranda']

links = [('Augustus', 'Willy'),
          ('Mike', 'Joe'),
          ('Miranda', 'Mike'),
          ('Violet', 'Augustus'),
          ('Miranda', 'Willy'),
          ('Charlie', 'Mike'),
          ('Veruca', 'Joe'),
          ('Miranda', 'Augustus'),
          ('Willy', 'Augustus'),
          ('Joe', 'Charlie'),
          ('Veruca', 'Augustus'),
          ('Miranda', 'Joe')]

def crosscount(v):
    # 数字のリストを人:(x,y) 形式のディクショナリに変換
    loc = dict([(people[i], (v[i*2], v[i*2+1])) for i in range(0, len(people))])
    total = 0

    # リンクのすべての組み合わせに対してループをかける
    for i in range(len(links)):
        for j in range(i+1, len(links)):

            # 座標の取得
            (x1, y1), (x2, y2) = loc[links[i][0]], loc[links[i][1]]
            (x3, y3), (x4, y4) = loc[links[j][0]], loc[links[j][1]]

            den = (y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)

            # den == 0 なら線は平行
            if den == 0: continue

            # 他の場合uaとubは交点を各線の分点で表現したもの
            ua=((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/float(den)
            ub=((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/float(den)

            #print ua, ub

            # 両方の線で分点が0から1の間にあれば線は交差している
            if ua>0 and ua<1 and ub>0 and ub<1:
                total+=1

    for i in range(len(people)):
        for j in range(i+1, len(people)):
            # 2つのノードの座標を取る
            (x1, y1), (x2, y2) = loc[people[i]], loc[people[j]]

            # 両者の距離を求める
            dist=math.sqrt(math.pow(x1-x2, 2) + math.pow(y1-y2,2))
            # 50ピクセルより近ければペナルティ
            if dist < 50:
                total+=(1.0-(dist/50.0))

    return total

def drawnetwork(sol):
    # イメージの作成
    img=Image.new('RGB',(400,400),(255,255,255))
    draw=ImageDraw.Draw(img)

    # 座標ディクショナリの生成
    pos=dict([(people[i],(sol[i*2],sol[i*2+1])) for i in range(0,len(people))])

    # リンクの描画
    for (a, b) in links:
        draw.line((pos[a],pos[b]), fill=(255,0,0))

    # 人の描画
    for n,p in pos.items():
        draw.text(p,n,(0,0,0))

    img.save('ssocial.jpg','JPEG')

domain = [(10,370)]*(len(people)*2)
