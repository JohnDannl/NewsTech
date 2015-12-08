#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-12-2

@author: dannl
'''
import feedparser
from bs4 import BeautifulSoup
import time,logging
from database import dbconfig,table
from common.common import r1, cost_log
from common import timeFormat
from common.toolpit import getMd5

ctable=dbconfig.tableName['w36kr']

def getRssInfo():
    url='http://36kr.com/feed'
    d=feedparser.parse(url)
#     print d.feed.title
#     print d.feed.link
#     print d.feed.description 
#     print d.etag
#     print d.modifed
    infoList=[]
    for entry in d.entries:
        info={}
        info['url']=entry.link
        info['newsid']=getMd5(info['url'])
        info['title']=entry.title
        info['description']=entry.description
        info['ctime']=(long)(time.mktime(entry.published_parsed))
        info['author']=entry.author
        info['source']=ctable
        info['keywords']=''
        soup = BeautifulSoup(entry.description, "html.parser",from_encoding='utf-8')
        img=soup.find('img')
        info['thumb']=img.get('src') if img else ''
        info['summary']=soup.getText()
        #         print entry
#         print info['newsid'],info['url']
#         print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(info['ctime'])),info['title']
#         print info['author'],info['thumb']
#         print info['description']
#         print info['summary']
        infoList.append(info)
    return infoList

@cost_log
def main():
    infoList=getRssInfo()
    for info in infoList:
        try:
#             table.InsertItemDict(ctable, info)
            print timeFormat.getTimeStamp(info['ctime']),info['title']            
        except:
            logging.error('encoding not supported:%s'%info['url'])
    return ctable,len(infoList)

if __name__=='__main__':
    main()