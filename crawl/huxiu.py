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
from common.common import r1, cost_log,getHtml
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

def getHtmlInfo():
    url=r'http://www.huxiu.com'   
    wap_url='http://m.huxiu.com'
    content=getHtml(url)
    #print content
    newsList=[]
    if content:
        soup = BeautifulSoup(content, 'html.parser',from_encoding='utf-8')
        itemList=soup.find_all('div',{'class':'mod-b mod-art '})
        itemList+=soup.find_all('div',{'class':'mod-b mod-art mod-b-push'})
        for item in itemList:
            nInfo={}
            head=item.find('',{'class':'mob-ctt'})
            if not head:
                continue
            title=head.find('h3')
            if not title:
                continue
            title=title.find('a')
            nInfo['url']=url+title.get('href')         
            nInfo['title']=title.getText()
            nInfo['newsid']=getMd5(nInfo['url'])                   
            nInfo['summary']=item.find('div',{'class':'mob-sub'}).getText() 
            nInfo['description']=nInfo['summary']      
            nInfo['thumb']= item.find('img',{'class':'lazy'}).get('data-original')            
            nInfo['keywords']= ''
            timeStr=head.find('span',{'class':'time'}).getText()  
            timeSec=time.time()   
            min_num=r1(u'(\d{1,2})分钟前',timeStr)   
            if min_num:
                timeSec-=60*long(min_num)
            else:
                hour_num=r1(u'(\d{1,2})小时前',timeStr) 
                if hour_num:
                    timeSec-=3600*long(hour_num)
                else:
                    day_num=r1(u'(\d{1,2})天前',timeStr) 
                    timeSec=timeSec-long(day_num)*24*3600 if day_num else timeSec             
            nInfo['ctime']=timeSec
            author_div=item.find('div',{'class':'mob-author'})
            nInfo['author']=''
            if author_div:
                author_span=author_div.find('span',{'class':'author-name '})
                nInfo['author']=author_span.getText() if author_span else ''
            nInfo['source']=ctable
            newsList.append(nInfo)
    return newsList

@cost_log
def main():
    infoList=getHtmlInfo()
    for info in infoList:
        try:
            table.InsertItemDict(ctable, info)
            print timeFormat.getTimeStamp(info['ctime']),info['title']
        except:
            logging.error('encoding not supported:%s'%info['url'])
    return ctable,len(infoList)

if __name__=='__main__':
    main()
#     infos=getRssInfo()
#     for info in infos:
#         print time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(info['ctime'])),info['title']
        