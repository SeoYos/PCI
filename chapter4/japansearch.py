# -*- coding:utf-8 -*-

import sys
import urllib2
from bs4 import BeautifulSoup
import sqlite3
from janome.tokenizer import Tokenizer
import re

class crawler:

    #
    def __init__(self,dbname):
        self.con=sqlite3.connect(dbname)

    def __del__(self):
        self.con.close

    def dbcommint(self):
        self.con.commit

    # 形態素解析
    def janomeexec(self,text):
        t=Tokenizer(udic='dic.csv', udic_enc="utf8")
        tokens = t.tokenize(text)
        for token in tokens:
            word=str(token).split('\t')[0]
            hinshi=str(token).split('\t')[1].split(',')[0]
            p = re.compile('^[a-zA-Z0-9!-/:-@¥[-`{-~]+$')
            m = p.match(word)

            if hinshi == "名詞":
                if not m:
                        print(word)

    def separateword(self,text):
        pass

    def crawl(self,page):
        c=urllib2.urlopen(page)
        soup=BeautifulSoup(c.read())
        for string in soup.stripped_strings:
            self.janomeexec(string)

