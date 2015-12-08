#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-5-19

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

ctable=dbconfig.tableName['bnet']

# http://www.bnet.com.cn/

def getHtmlInfo():
    url='http://www.bnet.com.cn/files/list_more_2013.php?class_id=129&page=1'  
    content=getHtml(url)
#     print content
    newsList=[]
    if content:
        soup = BeautifulSoup(content, 'html.parser',from_encoding='gbk')
        itemList=soup.find_all('div',{'class':"item"})
        for item in itemList:
            nInfo={}
            head=item.find('h3').find('a')
            nInfo['url']=head.get('href')
            title=head.getText()
            nInfo['title']=r1(u'(?:^[【,「].*?[】,」])?(.*)',title)
            nInfo['newsid']=getMd5(nInfo['url'])              
            nInfo['summary']=item.find('p',{'class':'summary'}).getText().strip()
            img=item.find('a',{'class':'thumb'}).find('img')
            nInfo['thumb']=img.get('src')  
            nInfo['keywords']=','.join(i.getText() for i in item.find_all('span')[1].find_all('a'))
            timeStr= r1('/(\d{4}/\d{4})/',nInfo['url'])
            nInfo['ctime']= long(time.mktime(time.strptime(timeStr,'%Y/%m%d')))                             
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