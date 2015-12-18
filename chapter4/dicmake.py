# -*- coding: utf-8 -*-

import sys

f = open('./link.txt','r')
w = open('dic.csv','w')

for line in f:
    #print line.split("\n")
    w.write(line.split("\n")[0])
    w.write(",1288,1288,6058,名詞,固有名詞,*,名,*,*,,,")
    w.write("\n")

w.close()
f.close()

