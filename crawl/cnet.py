#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-5-19

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

ctable=dbconfig.tableName['cnet']

# http://www.cnetnews.com.cn/

def getHtmlInfo():
    url='http://www.cnetnews.com.cn/'  
    domain='http://www.cnetnews.com.cn'
    content=getHtml(url)
#     print content
    newsList=[]
    if content:
#         content=content[content.find(">")+1:]
        soup = BeautifulSoup(content, 'html.parser',from_encoding='gbk')
        soup=soup.find('div',{'class':'news'})
        if not soup:
            return newsList
        itemList=soup.find_all('div',{'class':'qu_loop'})
        for item in itemList:
            nInfo={}
            head=item.find('div',{'class':'qu_tix'})
            nInfo['url']=head.find('b').find('a').get('href')
            nInfo['newsid']=getMd5(nInfo['url'])
            nInfo['title']=head.find('b').getText()
            nInfo['summary']=head.find('p').getText()
            metas=head.find('p',{'class':'meta'})
            nInfo['keywords']=' '.join(a.getText() for a in metas.find_all('a')) if metas else ''            
            nInfo['thumb']=item.find('div',{'class':'qu_ims'}).find('img').get('src')
            timeStr= item.find('div',{'class':'qu_times'}).getText()            
            nInfo['ctime']= long(time.mktime(time.strptime(timeStr,u'%Y-%m-%d %H:%M:%S'))) 
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