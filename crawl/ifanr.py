#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-12-7

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

ctable=dbconfig.tableName['ifanr']

def getRssInfo():
    url='http://www.ifanr.com/feed'
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
        info['description']=entry.content[0].value
        info['ctime']=(long)(time.mktime(entry.published_parsed))
        info['author']=entry.author
        info['source']=ctable
        tags=entry.tags
        info['keywords']=','.join(tag.term for tag in tags) if tags else ''
        soup = BeautifulSoup(info['description'], "html.parser",from_encoding='utf-8')        
        img=soup.find('img')
        info['thumb']=img.get('src') if img else ''
        info['summary']=' '.join(p.getText() for p in soup.find_all('p')[:-2])
#         print entry
#         print info['newsid'],info['url']
#         print timeFormat.getTimeStamp(info['ctime']),info['title']
#         print info['author'],info['thumb']
#         print info['keywords'],
#         print info['summary']
#         print info['description']
        infoList.append(info)
    return infoList

@cost_log
def main():
    infoList=getRssInfo()
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)
            print timeFormat.getTimeStamp(info['ctime']),info['title']
        except:
            logging.error('encoding not supported:%s'%info['url'])
    return ctable,len(infoList)

if __name__=='__main__':
    main()