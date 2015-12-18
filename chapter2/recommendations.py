# A dictionary of movie critics and their ratings of a small
# set of movies
critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 
 'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 
 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 
 'You, Me and Dupree': 3.5}, 
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
 'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
 'The Night Listener': 4.5, 'Superman Returns': 4.0,
 'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
 'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

from math import sqrt

# person1$B$H(Bperson2$B$N5wN%$r4p$K$7$?N`;w@-%9%3%"$rJV$9(B
def sim_distance(prefs,person1,person2):
    # $BFs?M$H$bI>2A$7$F$$$k%"%$%F%`$N%j%9%H$rF@$k(B
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

    # $BN><T6&$KI>2A$7$F$$$k$b$N$,0l$D$b$J$1$l$P(B0$B$rJV$9(B
    if len(si) == 0: return 0

    # $B$9$Y$F$N:9$NJ?J}$rB-$79g$o$;$k(B
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                    for item in si])
    return 1/(1+sqrt(sum_of_squares))

# p1$B$H(Bp2$B$N%T%"%=%sAj4X78?t$rJV$9(B
def sim_pearson(prefs,p1,p2):
    # $BN><T$,$*8_$$$KI>2A$7$F$$$k%"%$%F%`$N%j%9%H$r<hF@(B
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1

    # $BMWAG$N?t$rD4$Y$k(B
    n=len(si)

    # $B6&$KI>2A$7$F$$$k%"%$%F%`$,$J$1$l$P(B0$B$rJV$9(B
    if n==0: return 0

    # $B$9$Y$F$NSO9%$r9g7W$9$k(B
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    # $BJ?J}$r9g7W$9$k(B
    sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])

    # $B@Q$r9g7W$9$k(B
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

    # $B%T%"%=%s$K$h$k%9%3%"$r7W;;$9$k(B
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0: return 0

    r=num/den

    return r

# $B%G%#%/%7%g%J%j(Bpref$B$+$i(Bperson$B$K$b$C$H$b%^%C%A$9$k$b$N$?$A$rJV$9(B
# $B7k2L$N?t$HN`;w@-4X?t$O%*%W%7%g%s$N%Q%i%a!<%?(B
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other)
            for other in prefs if other!=person]
    # $B9b%9%3%"$,%j%9%H$N:G=i$KMh$k$h$&$KJB$SBX$($k(B
    scores.sort()
    scores.reverse()
    return scores[0:n]


# person$B0J30$NA4%f!<%6!<$NI>E@$N=E$_IU$-J?6Q$r;H$$!"(Bperson$B$X$N?dA&$r;;=P$9$k(B
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        # $B<+J,<+?H$HHf3S$7$J$$(B
        if other==person: continue
        sim=similarity(prefs,person,other)

        # 0 $B0J2<$N%9%3%"$OL5;k$9$k(B
        if sim<=0: continue

        for item in prefs[other]:
            # $B$^$@8+$F$$$J$$1G2h$NF@E@$N$_$r;;=P(B
            if item not in prefs[person] or prefs[person][item]==0:
                # $BN`;wEY(B * $B%9%3%"(B
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                # $BN`;wEY$r9g7W(B
                simSums.setdefault(item,0)
                simSums[item]+=sim

    # $B@55,2=$7$?%j%9%H$r:n$k(B
    rankings=[(total/simSums[item],item) for item, total in totals.items()]

    # $B%=!<%H:Q$_$N%j%9%H$rJV$9(B
    rankings.sort()
    rankings.reverse()
    return rankings

def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            # item$B$H(Bperson$B$rF~$lBX$($k(B
            result[item][person]=prefs[person][item]
    return result


