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

# 可能な帰結(各行の最終項目)を集計する
def uniquecounts(rows):
    results={}
    for row in rows:
        # 帰結は最後の項目
        r = row[len(row)-1]
        if r not in results: results[r]=0
        results[r]+=1
    return results

# ジニ不純度：無作為においた要素が間違ったカテゴリーに入る確率
def giniimpurity(rows):
    total=len(rows)
    counts=uniquecounts(rows)
    imp=0
    for k1 in counts:
        p1=float(counts[k1])/total
        for k2 in counts:
            if k1==k2: continue
            p2=float(counts[k2])/total
            imp+=p1*p2
    return imp

# エントロピーは可能な帰結それぞれの
# p(x)log(p(x))を合計したものである
def entropy(rows):
    from math import log
    log2=lambda x:log(x)/log(2)
    results=uniquecounts(rows)
    # ここからがエントロピーの計算
    ent=0.0
    for r in results.keys():
        p=float(results[r])/len(rows)
        ent=ent-p*log2(p)
    return ent

def buildtree(rows,scoref=entropy):
    if len(rows)==0: return None
    current_score=scoref(rows)

    # 最良分割基準の追跡に使う変数のセットアップ
    best_gain=0.0
    best_criteria=None
    best_sets=None

    column_count=len(rows[0])-1
    for col in range(0,column_count):
        # まずこの項目が取り得る値のリストを生成
        column_values={}
        for row in rows:
            column_values[row[col]]=1
        # この項目が取るそれぞれの値により行を振り分けてみる
        for value in column_values.keys():
            (set1,set2)=divideset(rows,col,value)

            # 情報ゲイン
            p=float(len(set1))/len(rows)
            gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
            if gain>best_gain and len(set1)>0 and len(set2)>0:
                best_gain=gain
                best_criteria=(col,value)
                best_sets=(set1,set2)

    # 次の段階の枝の作成
    if best_gain>0:
        trueBranch=buildtree(best_sets[0],scoref)
        falseBranch=buildtree(best_sets[1],scoref)
        return decisionnode(col=best_criteria[0],value=best_criteria[1],
                            tb=trueBranch,fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))

def printtree(tree,indent=''):
    # このノードはリーフ（葉＝末端）か？
    if tree.results != None:
        print str(tree.results)
    else:
    # 基準の出力
        print str(tree.col)+':'+str(tree.value)+'? '

        # 枝の出力
        print indent+'T->',
        printtree(tree.tb,indent+'  ')
        print indent+'F->',
        printtree(tree.fb,indent+'  ')
