#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2015-5-18

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

ctable=dbconfig.tableName['donews']

# http://www.donews.com/original/

def getHtmlInfo():
    url='http://www.donews.com/original/'  
    content=getHtml(url)
#     print content
    newsList=[]
    if content:
        soup = BeautifulSoup(content, 'html.parser',from_encoding='utf-8')
        block=soup.find('ul',{'class':'art_list mt11'})
        if not block:
            return newsList
        itemList=block.find_all('li')
        for item in itemList:
            nInfo={}
            head=item.find('h5',{'class':'title'}).find('a')
            nInfo['url']=head.get('href')
            title=head.getText()# the result returned by getText() is unicode
            nInfo['title']=r1(u'(?:^[【,「].*?[】,」])?(.*)',title) 
            nInfo['newsid']=getMd5(nInfo['url'])                       
            nInfo['summary']=item.find('p',{'class':'info'}).getText().strip()
            img=item.find('img')
            nInfo['thumb']=img.get('src') if img else ''
            nInfo['keywords']=''
            timeStr= item.find('span',{'class':'time'}).getText()
            dateStr=r1('(\d{4}/\d{4})',nInfo['thumb']) 
            dateStr+=r1('(\d{2}:\d{2})',timeStr)                 
            nInfo['ctime']=long(time.mktime(time.strptime(dateStr,'%Y/%m%d%H:%M')))              
            nInfo['source']=ctable
            nInfo['author']=item.find('span',{'class':'place'}).getText()
            nInfo['description']=''     
            #print nInfo['newsid'],nInfo['url']
            #print nInfo['author'],nInfo['thumb']
            #print nInfo['summary']
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