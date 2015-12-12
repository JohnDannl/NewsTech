#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-5-15

@author: dannl
'''
from common import timeFormat,fileKit
from common.common import *
from bs4 import BeautifulSoup
import time
import sys
import json
sys.path.append(r'..')
sys.path.append(r'../database')
from database import table
from database import dbconfig
from common.logger import log
import logging
from common.toolpit import getMd5

ctable=dbconfig.tableName['w163']

# http://tech.163.com/

def getHtmlInfo():
    url=r'http://tech.163.com/'   
    content=getHtml(url)
#     print content
    newsList=[]
    if content:
        soup = BeautifulSoup(content, "html.parser",from_encoding='gbk')
        itemList=soup.find_all('div',{'class':"hot-list-item border-top-dotted clearfix"})
        for item in itemList:
            nInfo={}
            head=item.find('h2',{'class':'color-link'})
            nInfo['url']=head.find('a').get('href')
            nInfo['title']=head.getText() # getText() is a safer way than .string to get text
            nInfo['newsid']=getMd5(nInfo['url'])      
            desc=item.find('p',{'class':'color-dig w390'})   
            nInfo['summary']=desc.find('a').getText()
            img=item.find('a',{'class':'left'}).find('img')
            nInfo['thumb']=img.get('src') if img.get('src') else img.get('data-src')
            nInfo['keywords']=','.join(i.getText() for i in item.find('span',{'class':'join-keys left clearfix'}).find_all('a'))
            timeStr=r1('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',item.find('h3',{'class':'color-date-from'}).getText())
            nInfo['ctime']= long(time.mktime(time.strptime(timeStr,'%Y-%m-%d %H:%M:%S')))
            nInfo['source']=ctable
            nInfo['author']=''
            nInfo['description']=desc
            newsList.append(nInfo)
    return newsList

@cost_log
def main():
    infoList=[]
    infoList+=getHtmlInfo()   
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)
            print timeFormat.getTimeStamp(info['ctime']),info['title']
        except:
            logging.error('encoding not supported:%s'%info['url'])
    return ctable,len(infoList)
        
if __name__=='__main__':
#     getHtmlInfo()
#     getJsInfo()
    main()
    