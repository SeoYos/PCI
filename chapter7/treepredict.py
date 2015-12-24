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
        # col: $B%F%9%H$5$l$k4p=`$N%$%s%G%C%/%9CM(B
        # value: $B7k2L$,??$H$J$k$N$KI,MW$JCM(B
        # tb$B$H(Bfb: $B$3$N%N!<%I$N7k2L$,??$N$H$-(B(tb)$B!"(B
        #         $B56$N$H$-(B(fb)$B$K$?$I$k<!$N(Bdecisionnode
        # results: $B$3$N;^$,;}$D5"7k$N%G%#%/%7%g%J%j$G!"(B
        #          $B=*C<(B(endpoint)$B0J30$G$O(BNone$B$H$J$k(B
        self.col=col
        self.value=value
        self.results=results
        self.tb=tb
        self.fb=fb

# $BFCDj$N9`L\$K4p$E$-=89g$rJ,3d$9$k(B
# $B9`L\$NCM$,?tCM$G$bL>A0$G$b=hM}2DG=(B
def divideset(rows,column,value):
    # $B9T$,:G=i$N%0%k!<%W(B(true)$B$KF~$k$+BhFs$N%0%k!<%W(B(false)$B$K(B
    # $BF~$k$+65$($F$/$l$k4X?t$r:n$k(B
    split_function=None
    if isinstance(value,int) or isinstance(value,float):
        split_function=lambda row:row[column]>=value
    else:
        split_function=lambda row:row[column]==value

    # $B9T$r#2$D$N=89g$K?6$jJ,$1$FJV$9(B
    set1 = [row for row in rows if split_function(row)]
    set2 = [row for row in rows if not split_function(row)]
    return (set1,set2)
