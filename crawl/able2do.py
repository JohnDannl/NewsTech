#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-5-20

@author: dannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')
from common import timeFormat,fileKit
from common.common import *
from bs4 import BeautifulSoup
import time
import json
from database import table
from database import dbconfig
from common.logger import log
import logging
from common.toolpit import getMd5

ctable=dbconfig.tableName['able2do']

# http://www.able2do.com/archives/category/information-products
headers=[('Host', 'www.able2do.com'),
     ('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:38.0) Gecko/20100101 Firefox/38.0'),
     ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), 
     ('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
     ('Connection', 'keep-alive'),
     ('Accept-Encoding','gzip, deflate')] 
monthDic={u'一月':'1',u'二月':'2',u'三月':'3',u'四月':'4',u'五月':'5',u'六月':'6',
          u'七月':'7',u'八月':'8',u'九月':'9',u'十月':'10',u'十一月':'11',u'十二月':'12'}
def getHtmlInfo():
    url='http://www.able2do.com/archives/category/information-products'  
    content=getHtmlwithCookie(url,headers)
    newsList=[]
    if content:
        soup = BeautifulSoup(content,'html.parser', from_encoding='utf-8')
        itemList=soup.find_all('article',{'class':"blog-thumb style_1 clearfix"})
        for item in itemList:
            nInfo={}
            head=item.find('a',{'class':'title'})
            nInfo['url']=head.get('href')
            nInfo['title']=head.getText()
            nInfo['newsid']=getMd5(nInfo['url'])              
            nInfo['summary']=item.find('p',{'class':'content-short'}).getText()
            img=item.find('img')
            nInfo['thumb']=img.get('src') if img else ''
            block_m=item.find('ul',{'class':'meta-entry clearfix'}).find_all('li')          
            nInfo['keywords']=','.join(i.getText() for i in block_m[0].find_all('a',{'rel':'category tag'}))
            timeStr=block_m[1].getText().split()
            timeStr= timeStr[2]+'-'+monthDic[timeStr[0]]+'-'+timeStr[1].replace(',','')
            nInfo['ctime']= long(time.mktime(time.strptime(timeStr,u'%Y-%m-%d')))  
            nInfo['source']=ctable
            nInfo['author']=''  
            nInfo['description']=''   
#             print nInfo['newsid'],nInfo['url']
#             print nInfo['keywords'],nInfo['thumb']
#             print nInfo['summary']
            newsList.append(nInfo)
    return newsList

@cost_log
def main():
    infoList=[]
    infoList+=getHtmlInfo()   
    for info in infoList:
        try:
#             table.InsertItemDict(ctable, info)
            print timeFormat.getTimeStamp(info['ctime']),info['title']
        except:
            logging.error('encoding not supported:%s'%info['url'])
    return ctable,len(infoList)
        
if __name__=='__main__':
#     getHtmlInfo()
#     getJsInfo()
    main()