# -*- coding:utf-8 -*-

my_data=[['slashdot','USA','yes',18,'None'],
        ['google','France','yes',23,'Premium'],
        ['digg','USA','yes',24,'Basic'],
        ['kiwitobes','France','yes',23,'Basic'],
        ['google','UK','no',21,'Premium'],
        ['(direct)','New Zealand','no',12,'None'],
        ['(direct)','UK','no',21,'Basic'],
        ['google','USA','no',24,'Premium'],
        ['slashdot','France','yes',19,'None'],
        ['digg','USA','no',18,'None'],
        ['google','UK','no',18,'None'],
        ['kiwitobes','UK','no',19,'None'],
        ['digg','New Zealand','yes',12,'Basic'],
        ['slashdot','UK','no',21,'None'],
        ['google','UK','yes',18,'Basic'],
        ['kiwitobes','France','yes',19,'Basic']]

class decisionnode:
    def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
        # col: テストされる基準のインデックス値
        # value: 結果が真となるのに必要な値
        # tbとfb: このノードの結果が真のとき(tb)、
        #         偽のとき(fb)にたどる次のdecisionnode
        # results: この枝が持つ帰結のディクショナリで、
        #          終端(endpoint)以外ではNoneとなる
        self.col=col
        self.value=value
        self.results=results
        self.tb=tb
        self.fb=fb

# 特定の項目に基づき集合を分割する
# 項目の値が数値でも名前でも処理可能
def divideset(rows,column,value):
    # 行が最初のグループ(true)に入るか第二のグループ(false)に
    # 入るか教えてくれる関数を作る
    split_function=None
    if isinstance(value,int) or isinstance(value,float):
        split_function=lambda row:row[column]>=value
    else:
        split_function=lambda row:row[column]==value

    # 行を２つの集合に振り分けて返す
    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    return (set1,set2)
