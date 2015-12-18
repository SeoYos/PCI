# -*- coding: utf-8 -*-

import time
import random
import math

people = [('Seymour', 'BOS'),
          ('Francy', 'DAL'),
          ('Zooey', 'CAK'),
          ('Walt', 'MIA'),
          ('Buddy', 'ORD'),
          ('Les', 'OMA')]

# $B%K%e!<%h!<%/$N%i%,!<%G%#%"6u9A(B
destination = 'LGA'

flights={}
#
for line in file('schedule.txt'):
    origin,dest,depart,arrive,price=line.strip().split(',')
    flights.setdefault((origin,dest),[])

    # $B%j%9%H$K%U%i%$%H$N>\:Y$rDI2C(B
    flights[(origin,dest)].append((depart,arrive,int(price)))

def getminutes(t):
    x=time.strptime(t,'%H:%M')
    return x[3]*60+x[4]

def printschedule(r):
    for d in range(len(r)/2):
        name=people[d][0]
        origin=people[d][1]
        out=flights[(origin,destination)][int(r[d*2])]
        ret=flights[(destination,origin)][int(r[d*2+1])]
        print '%10s%10s %5s-%5s $%3s %5s-%5s $%3s' % (name,origin,
                                                     out[0],out[1],out[2],
                                                     ret[0],ret[1],ret[2])

def schedulecost(sol):
    totalprice = 0
    latestarrival=0
    earliestdep=24*60

    for d in range(len(sol)/2):
        # $B9T$-(B(outbound)$B$H5"$j(B(return)$B$N%U%i%$%H$rF@$k(B
        origin=people[d][1]
        outbound=flights[(origin,destination)][int(sol[d*2])]
        returnf=flights[(destination,origin)][int(sol[d*2+1])]

        # $B1?DBAm3[(Btotal price$B$O=PN)JX$H5"BpJX$9$Y$F$N1?DB(B
        totalprice+=outbound[2]
        totalprice+=returnf[2]

        # $B:G$bCY$$E~Ce$H:G$bAa$$=PH/$r5-O?(B
        if latestarrival<getminutes(outbound[1]):
            latestarrival=getminutes(outbound[1])
        if earliestdep>getminutes(returnf[0]):
            earliestdep=getminutes(returnf[0])

    totalwait = 0
    for d in range(len(sol)/2):
        origin=people[d][1]
        outbound=flights[(origin,destination)][int(sol[d*2])]
        returnf=flights[(destination,origin)][int(sol[d*1])]
        totalwait+=latestarrival-getminutes(outbound[1])
        totalwait+=getminutes(returnf[0])-earliestdep

    # $B$3$N2r$G$O%l%s%?%+!<$NDI2CNA6b$,I,MW$+!)$3$l$O#5#0%I%k!*(B
    if latestarrival<earliestdep:
        totalprice+=50

    return totalprice+totalwait

def randomoptimize(domain,costf):
    best=999999999
    bestr=None
    for i in range(1000):
        # $BL5:n0Y2r$N@8@.(B
        r=[random.randint(domain[i][0],domain[i][1])
           for i in range(len(domain))]

        # $B%3%9%H$N<hF@(B
        cost = costf(r)

        # $B:GNI2r$HHf3S(B
        if cost<best:
            best=cost
            bestr=r

    return bestr

def hillclimb(domain,costf):
    # $BL5:n0Y2r$N@8@.(B
    sol = [random.randint(domain[i][0],domain[i][1])
           for i in range(len(domain))]

    # Main loop
    while 1:

        # $B6aK52r%j%9%H$N@8@.(B
        neighbors=[]

        for j in range(len(domain)):
            # $B3FJ}8~$K(B1$B$:$D$:$i$9(B
            if sol[j]>domain[j][0]:
                neighbors.append(sol[0:j]+[sol[j]-1]+sol[j+1:])
            if sol[j]<domain[j][1]:
                neighbors.append(sol[0:j]+[sol[j]+1]+sol[j+1:])

        # $B6aK52rCf$N%Y%9%H$rC5$9(B
        current=costf(sol)
        best=current
        for j in range(len(neighbors)):
            cost=costf(neighbors[j])
            if cost<best:
                best=cost
                sol=neighbors[j]

        # $B2~A1$,8+$i$l$J$1$l$P$=$l$,:G9b(B
        if best==current:
            break

    return sol

def annealingoptimize(domain,costf,T=10000.0,cool=0.95,step=1):
    # $B%i%s%@%`$JCM$G2r$r=i4|2=(B
    vec = [float(random.randint(domain[i][0],domain[i][1]))
            for i in range(len(domain))]

    while T>0.1:
        # $B%$%s%G%C%/%9$r0l$DA*$V(B
        i=random.randint(0,len(domain)-1)

        # $B%$%s%G%C%/%9$NCM$K2C$($kJQ99$NJ}8~$rA*$V(B
        dir=random.randint(-step,step)

        # $BCM$rJQ99$7$?%j%9%H!J2r!K$r@8@.(B
        vecb=vec[:]
        vecb[i]+=dir
        if vecb[i]<domain[i][0]: vecb[i]=domain[i][0]
        elif vecb[i]>domain[i][1]: vecb[i]=domain[i][1]

        # $B8=:_2r$H@8@.2r$N%3%9%H$r;;=P(B
        ea=costf(vec)
        eb=costf(vecb)
        p=pow(math.e,-abs(eb-ea)/T)

        # $B@8@.2r$,%Y%?!<!)!!$^$?$O3NN(E*$K:NMQ!)(B
        if (eb<ea or random.random()<p):
            vec=vecb

        # $B29EY$r2<$2$k(B
        T=T*cool

    return vec

def geneticoptimize(domain,costf,popsize=50,step=1,
                     mutprob=0.2,elite=0.2,maxiter=100):

    # $BFMA3JQ0[$NA`:n(B
    def mutate(vec):
        i=random.randint(0,len(domain)-1)
        if random.random()<0.5 and vec[i]>domain[i][0]:
            return vec[0:i] + [vec[i]-step]+vec[i+1:]
        elif vec[i]<domain[i][1]:
            return vec[0:i]+[vec[i]+step]+vec[i+1:]

    # $B8r:5$NA`:n(B
    def crossover(r1,r2):
        i=random.randint(1,len(domain)-2)
        return r1[0:i]+r2[i:]

    # $B=i4|8DBN72$N9=C[(B
    pop=[]
    for i in range(popsize):
        vec=[random.randint(domain[i][0],domain[i][1])
             for i in range(len(domain))]
        pop.append(vec)

    # $B3F@$Be$N>!<T?t$O!)(B
    topelite=int(elite*popsize)

    # Main loop
    for i in range(maxiter):
        scores=[(costf(v),v) for v in pop]
        scores.sort()
        ranked=[v for (s,v) in scores]

        # $B$^$:=c?h$J>!<T(B
        pop=ranked[0:topelite]

        # $B>!<T$KFMA3JQ0[$d8rG[$r9T$C$?$b$N$rDI2C(B
        while len(pop)<popsize:
            if random.random()<mutprob:

                # $BFMA3JQ0[(B
                c=random.randint(0,topelite)
                pop.append(mutate(ranked[c]))
            else:

                # $B8r:5(B
                c1=random.randint(0,topelite)
                c2=random.randint(0,topelite)
                pop.append(crossover(ranked[c1],ranked[c2]))

        # $B8=:_$N%Y%9%H%9%3%"$r=PNO(B
        print scores[0][0]

    return scores[0][1]
