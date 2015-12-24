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
        print 'Guess: '+str(classifier.classify(fulltext))

        # ユーザに正しいカテゴリを尋ね、それを元にトレーニングする
        cl=raw_input('Enter category: ')
        classifier.train(fulltext,cl)
