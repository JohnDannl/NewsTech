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
        itemList=soup.find_all('div',{'class':"hot_board clearfix"})
        for item in itemList:
            nInfo={}
            nInfo['url']=item.find('a').get('href')
            head=item.find('div',{'class':'hb_detail'})            
            nInfo['title']=head.find('h3').getText() # getText() is a safer way than .string to get text
            nInfo['newsid']=getMd5(nInfo['url'])      
            desc=head.find('p').string   
            nInfo['summary']=desc
            img=item.find('div',{'class':'img_box'}).find('img')
            nInfo['thumb']=img.get('src') if img.get('src') else img.get('data-src')
            nInfo['keywords']=head.find('span').getText()
            timeStr=head.find('em').get('time')
            nInfo['ctime']= long(time.mktime(time.strptime(timeStr,'%m/%d/%Y %H:%M:%S')))
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
    