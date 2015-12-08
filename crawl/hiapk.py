#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-5-20

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

ctable=dbconfig.tableName['hiapk']

urls=['http://news.hiapk.com/brands/',
      'http://news.hiapk.com/industry/',
      'http://news.hiapk.com/internet/',
      'http://news.hiapk.com/tech/',
      'http://news.hiapk.com/column/']

def getHtmlInfo(url):
#     url='http://news.hiapk.com/internet/'
    content=getHtml(url)
#     print content
    newsList=[]
    if content:
        soup = BeautifulSoup(content, 'html.parser',from_encoding='utf-8')
        itemList=soup.find_all('div',{'class':"box"})
        for item in itemList:
            nInfo={}
            head=item.find('strong').find('a')
            nInfo['url']=head.get('href')
            title=head.getText()
            nInfo['title']=r1(u'(?:^[【,「].*?[】,」])?(.*)',title) 
            nInfo['newsid']=getMd5(nInfo['url'])  
            nInfo['summary']=item.find('p',{'class':'intro'}).getText()
            nInfo['thumb']=item.find('img').get('src')  
            nInfo['keywords']=','.join(i.getText() for i in item.find('p',{'class':'clearfix tag'}).find_all('a'))
            timeStr= time.strftime('%Y')+'-'+item.find('span',{'class':'right time'}).getText()
            nInfo['ctime']= long(time.mktime(time.strptime(timeStr,'%Y-%m-%d')))  
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
    for url in urls:
        print url
        infoList+=getHtmlInfo(url)   
    for info in infoList:
        try:
#             table.InsertItemDict(ctable, info)
            print timeFormat.getTimeStamp(info['ctime']),info['title']
        except:
            logging.error('encoding not supported:%s'%info['url'])
    return ctable,len(infoList)
        
if __name__=='__main__':
#     getHtmlInfo(urls[2])
#     getJsInfo()
    main()