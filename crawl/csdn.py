#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-5-18

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

ctable=dbconfig.tableName['csdn']

# http://news.csdn.net/news/1

def getHtmlInfo(url):
#     url='http://news.csdn.net/news/1'  
    content=getHtml(url)
#     print content
    newsList=[]
    if content:
        soup = BeautifulSoup(content, 'html.parser',from_encoding='utf-8')
        itemList=soup.find_all('div',{'class':"unit"})
        for item in itemList:
            nInfo={}
            head=item.find('h1').find('a')
            nInfo['url']=head.get('href')
            title=head.getText()
            nInfo['title']=r1(u'(?:^[【,「].*?[】,」])?(.*)',title)
            nInfo['newsid']=getMd5(nInfo['url'])    
            desc=item.find('dd')         
            nInfo['summary']=desc.getText()
            img=item.find('img')
            nInfo['thumb']=img.get('src') if img else ''                              
            nInfo['keywords']=','.join(tag.getText() for tag in item.find('div',{'class':'tag'}).find_all('a'))
            timeStr= item.find('span',{'class':'ago'}).getText()
            timeStamp=r1('(\d{4}-\d{2}-\d{2} \d{2}:\d{2})',timeStr)
            if not timeStamp:
                hourago=r1(u'(\d{1,2})小时前',timeStr)
                ctime=time.time()-int(hourago)*3600 if hourago else time.time()
            else:
                ctime=time.mktime(time.strptime(timeStr,'%Y-%m-%d %H:%M'))
            nInfo['ctime']= long(ctime)                    
            nInfo['source']=ctable
            nInfo['author']=''          
            nInfo['description']=desc
            newsList.append(nInfo)
    return newsList
urls=['http://news.csdn.net/',
      'http://mobile.csdn.net/',
      'http://cloud.csdn.net/',
      'http://sd.csdn.net/',
      'http://programmer.csdn.net/']
@cost_log
def main():
    infoList=[]
    for url in urls:
        infoList+=getHtmlInfo(url)   
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