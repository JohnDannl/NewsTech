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

ctable=dbconfig.tableName['ciweek']

# http://www.ciweek.com/v7/list.jsp

def getHtmlInfo():
    url='http://www.ciweek.com/v7/list.jsp'  
    domain='http://www.ciweek.com'
    content=getHtml(url)
#     print content
    newsList=[]
    if content:
        soup = BeautifulSoup(content, 'html.parser',from_encoding='gbk')
        itemList=soup.find_all('dl',{'class':"clearfix"})
        for item in itemList:
            nInfo={}
            head=item.find('h2').find('a')
            nInfo['url']=domain+head.get('href')
            nInfo['title']=head.getText()
            nInfo['newsid']=getMd5(nInfo['url'])      
            desc=item.find('p').find('span')         
            nInfo['summary']=desc.getText()
            img=item.find('img')
            nInfo['thumb']=img.get('src') if img else ''                                      
            nInfo['keywords']=''
            timeStr= item.find('span',{'class':'date hidden-xs'}).getText()
            nInfo['ctime']= long(time.mktime(time.strptime(timeStr,'%Y-%m-%d'))) 
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