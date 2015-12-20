#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-12-14

@author: dannl
'''
import feedparser
from bs4 import BeautifulSoup
import time,logging
from database import dbconfig,table
from common.common import r1, cost_log
from common import timeFormat
from common.toolpit import getMd5

ctable=dbconfig.tableName['feng']

urls=['http://www.feng.com/rss.xml',
      'http://lab.feng.com/rss.xml']
def getRssInfo(url):
    d=feedparser.parse(url)
#     print d.feed.title
#     print d.feed.link
#     print d.feed.description 
#     print d.etag
#     print d.modifed
    infoList=[]
    for entry in d.entries:
        info={}
#         print entry
        info['url']=entry.link
        info['newsid']=getMd5(info['url'])
        info['title']=entry.title
        info['ctime']=(long)(time.mktime(entry.published_parsed))
        info['author']=entry.author
#         print timeFormat.getTimeStamp(info['ctime']),info['title']
        info['source']=ctable
        tags=entry.tags if 'tags' in entry else None   
        info['keywords']=','.join(tag.term for tag in tags) if tags else ''        
        info['description']=entry.summary #entry.content[0].value
        soup = BeautifulSoup(info['description'], "html.parser",from_encoding='utf-8')        
        img=soup.find('img')
        info['thumb']=img.get('src') if img else ''
        info['summary']=soup.getText() #' '.join(p.getText().strip() for p in soup.find_all('p'))
#         print info['newsid'],info['url']
#         print info['author']
#         print info['keywords'],info['thumb']
#         print info['summary']
#         print info['description']
        infoList.append(info)
    return infoList

@cost_log
def main():
    infoList=[]
    for url in urls:
        infoList+=getRssInfo(url)
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)
            print timeFormat.getTimeStamp(info['ctime']),info['title']     
        except:
            logging.error('encoding not supported:%s'%info['url'])
    return ctable,len(infoList)

if __name__=='__main__':
    main()