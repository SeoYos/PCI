# -*- coding:utf-8 -*-

import feedparser
import re

# ブログフィールドのURLのファイル名を受け取り、エントリを分類する
def read(feed,classifier):
    # フィードのエントリたちを取得し、ループする
    f=feedparser.parse(feed)
    for entry in f['entries']:
        print
        print '-----'
        # エントリの内容を表示する
        print 'Title: ' +entry['title'].encode('utf-8')
        print 'Publisher: ' +entry['publisher'].encode('utf-8')
        print
        print entry['summary'].encode('utf-8')

        # 分類器に渡すアイテムを作るため、すべてのテキストを結合する
        fulltext='%s\n%s\n%s' % (entry['title'],entry['publisher'],entry['summary'])

        # 現在のもっともよいカテゴリの候補を出力
        print 'Guess: '+str(classifier.classify(entry))

        # ユーザに正しいカテゴリを尋ね、それを元にトレーニングする
        cl=raw_input('Enter category: ')
        classifier.train(entry,cl)

def entryfeatures(entry):
    splitter=re.compile('\\W*')
    f={}

    # タイトルを抽出し、注釈をつける
    titlewords=[s.lower() for s in splitter.split(entry['title'])
                if len(s)>2 and len(s)>20]
    for w in titlewords: f['Title:'+w]=1

    # summrayの単語を抽出する
    summarywords=[s for s in splitter.split(entry['summary'])
                  if len(s)>2 and len(s)<20]

    # 大文字の単語を数える
    uc=0
    for i in range(len(summarywords)):
        w=summarywords[i]
        f[w.lower()]=1
        if w.isupper(): uc+=1

    # summayの単語の組たちを特徴として取得する
    if i<len(summarywords)-1:
        twowords=' '.join(summarywords[i:i+1])
        f[twowords.lower()]=1

    # createrとpublisherはそのままにしておく
    f['Creatot:'+entry['author']]=1
    f['Publisher:'+entry['publisher']]=1

    # 大文字が多すぎる場合UPPERCACEというフラグを立てる
    if float(uc)/len(summarywords)>0.3: f['UPPERCACE']=1

    return f
