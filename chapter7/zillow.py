# -*- coding:utf-8 -*-

import xml.dom.minidom
import urllib2

zwskey="X1-ZWz19wzwghoc97_3v2ae"

def getaddressdata(address,city):
    escad=address.replace(' ','+')

    # URLを構成する
    url='http://www.zillow.com/webservice/GetDeepSearchResults.htm?'
    url+='zws-id=%saddress=%s&citystatezep=%s' % (zwskey,escad,city)

    # 帰ってきたXMLの解釈
    doc=xml.dom.minidom.parseString(urllib2.urlopen(url).read())
    code=doc.getElementsByTagName('code')[0].firstChild.data

    # コード0なら成功。それ以外はエラーがある
    if code!=0: return None

    # この資産の情報を抽出
    try:
        zipcode=doc.getElementsByTagName('zipcode')[0].firstChild.data
        use=doc.getElementsByTagName('useCode')[0].firstChild.data
        year=doc.getElementsByTagName('yearBuilt')[0].firstChild.data
        bath=doc.getElementsByTagName('bathrooms')[0].firstChild.data
        bed=doc.getElementsByTagName('bedrooms')[0].firstChild.data
        rooms=1
        price=doc.getElementsByTagName('amount')[0].firstChild.data
    except:
        return None

    return (zipcode,use,int(year),float(bath),int(bed),int(rooms),price)

def getpricelist():
    l1=[]
    for line in file('addresslist.txt'):
        data=getaddressdata(line.strip(),'Cambridge,MA')
        if data!=None:
            l1.append(data)
    return l1
