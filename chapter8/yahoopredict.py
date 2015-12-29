# -*- coding:utf-8 -*-

import requests
from xml.dom.minidom import parse,parseString, Node

# 検索リクエストURL
url='http://auctions.yahooapis.jp/AuctionWebService/V2/search'
# アプリケーションID
apid='dj0zaiZpPXJFeElCbVUyOVZCcyZzPWNvbnN1bWVyc2VjcmV0Jng9MjY-'

def sendRequest(query):
    payload={'appid':apid,'Query':query}
    connection=requests.post(url,params=payload)
    data = connection.text.encode('utf-8')
    return data

def doSearch(query):
    data=sendRequest(query)
    response = parseString(data)
    itemNodes = response.getElementsByTagName('Item')
    results=[]
    for item in itemNodes:
        itemId=getSingleValue(item,'AuctionID')
        itemUrl=getSingleValue(item,'AuctionItemUrl')
        itemTitle=getSingleValue(item,'Title')
        itemPrice=getSingleValue(item,'CurrentPrice')
        itemBids=getSingleValue(item,'Bids')
        itemEnds=getSingleValue(item,'EndTime')
        results.append({'AuctionID':itemId,
                        'AuctionItemUrl':itemUrl,
                        'Title':itemTitle,
                        'CurrentPrice':itemPrice,
                        'Bids':itemBids,
                        'EndTime':itemEnds})
    return results

def getSingleValue(node,tag):
    nl=node.getElementsByTagName(tag)
    if len(nl)>0:
        tagNode=nl[0]
        if tagNode.hasChildNodes():
            return tagNode.firstChild.nodeValue
