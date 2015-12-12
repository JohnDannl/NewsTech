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
import logging,re
from common.toolpit import getMd5

ctable=dbconfig.tableName['zdnet']

# http://www.zdnet.com.cn/

def getHtmlInfo():
    url='http://www.zdnet.com.cn/'  
    content=getHtml(url)
#     print content
    newsList=[]
    if content:
        soup = BeautifulSoup(content, 'html.parser',from_encoding='gbk')
        soup=soup.find('div',{'id':'tab1'})
        if not soup:
            return newsList
        itemList=soup.find_all('div',{'class':'qu_loop'})
        for item in itemList:
            nInfo={}
            head=item.find('div',{'class':'qu_tix'})
            nInfo['url']=head.find('b').find('a').get('href')
            nInfo['newsid']=getMd5(nInfo['url'])
            nInfo['title']=head.find('b').getText()
            desc=head.find('p')
            nInfo['summary']=desc.getText()
            metas=head.find('p',{'class':'meta'})
            nInfo['keywords']=','.join(a.getText() for a in metas.find_all('a')) if metas else ''            
            nInfo['thumb']=item.find('div',{'class':'qu_ims'}).find('img').get('src')
            timeStr= item.find('div',{'class':'qu_times'}).getText()            
            nInfo['ctime']= long(time.mktime(time.strptime(timeStr,u'%Y-%m-%d %H:%M:%S'))) 
            nInfo['source']=ctable
            nInfo['author']=''  
            nInfo['description']=desc 
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
            table.InsertItemDict(ctable, info)
            print timeFormat.getTimeStamp(info['ctime']),info['title']
        except:
            logging.error('encoding not supported:%s'%info['url'])
    return ctable,len(infoList)
        
if __name__=='__main__':
#     getHtmlInfo()
#     getJsInfo()
    main()