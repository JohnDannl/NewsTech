#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-12-1

@author: dannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')
import feedparser
from bs4 import BeautifulSoup
import time,logging
from database import dbconfig,table
from common.common import r1, cost_log
from common import timeFormat,logger
from common.toolpit import getMd5

ctable=dbconfig.tableName['huxiu']

def getRssInfo():
    url='http://www.huxiu.com/rss/0.xml'
    d=feedparser.parse(url)
#     print d.feed.title
#     print d.feed.link
#     print d.feed.description 
    # print d.etag
    # print d.modifed
    infoList=[]
    for entry in d.entries:
        info={}
        info['url']=entry.link
        info['newsid']=getMd5(info['url'])
        info['title']=entry.title
        info['description']=entry.description
        info['ctime']=(long)(time.mktime(entry.published_parsed))
        info['author']=entry.source.title
        info['source']=ctable
        info['keywords']=''
#         print entry
#         print info['url']
#         print info['newsid']
#         print info['title'],info['ctime']
#         print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(info['ctime'])),info['author']
#         print entry.published_parsed
#         print info['description']
        soup = BeautifulSoup(entry.description, "html.parser",from_encoding='utf-8')
        img=soup.find('img')
        info['thumb']=img.get('src') if img else ''
        info['summary']=soup.getText()
#         print info['thumb']
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
#     infos=getRssInfo()
#     for info in infos:
#         print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(info['ctime'])),info['title']
        