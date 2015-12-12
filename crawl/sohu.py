#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-5-14

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

ctable=dbconfig.tableName['sohu']

# http://it.sohu.com/
# http://it.sohu.com/tag/0270/000021270_utf8.inc?_=1449103206253
# http://it.sohu.com/tag/0270/000021270_86_utf8.inc?_=1449102818419

def getHtmlInfo(url):    
#     url='http://it.sohu.com/internet_2014.shtml'
    content=getHtml(url)
#     print content
    newsDict={}
    if content:
        soup = BeautifulSoup(content, "html.parser",from_encoding='gbk')
        itemList=soup.find_all('div',{'class':"item clear"})
        for item in itemList:
            nInfo={}
            item_txt=item.find('div',{'class':"item-txt"})            
            head=item_txt.find('h3').find('a')
            nInfo['title']= head.getText()
            nInfo['url']=head.get('href')             
            nInfo['newsid']=getMd5(nInfo['url'])
            item_info=item_txt.find('div',{'class':"news-info"}) 
            timeStr=item_info.find('span',{'class':"time"}).getText()  
            nInfo['ctime']=long(time.mktime(time.strptime(timeStr, u'%Y年%m月%d日%H:%M')))
            desc=item_txt.find('p')
            nInfo['summary']=desc.getText()
            item_pic=item.find('div',{'class':"item-pic"})
            nInfo['thumb']=item_pic.find('img').get('src') if item_pic else ''
            nInfo['keywords']=''
            nInfo['source']=ctable    
            nInfo['author']=item_info.find('span',{'class':"edit-info"}).getText().strip()
            nInfo['description']=str(desc)                
            newsDict[nInfo['newsid']]=nInfo
#             print nInfo['ctime'],nInfo['title']
#             print nInfo['newsid'],nInfo['url']
#             print nInfo['author'],nInfo['thumb']
#             print nInfo['summary']
    return newsDict

def getJsInfo():
    url=r'http://it.sohu.com/tag/0270/000021270_86_utf8.inc?_='
    url+=str(long(time.time()*1000))
#     print url
    content=getHtml(url)
#     print content   
    newsDict={}
    if content:
        infoList=json.loads(r1('.*?(\[.*\])',content),encoding='utf-8')                  
        for info in infoList:
            try:
                nInfo={}
                nInfo['newsid']=getMd5(info['url'])
                nInfo['title']= info['title']                
                nInfo['url']=info['url']                
                nInfo['summary']=info['text']
                nInfo['thumb']=info['image']
                nInfo['keywords']=','.join(tag['name'] for tag in info['tags']) if len(info['tags'])>0 else ''                    
                nInfo['source']=ctable
                nInfo['ctime']=long(time.mktime(time.strptime(info['time'],u'%Y年%m月%d日%H:%M')))
                nInfo['author']= info['source']            
                nInfo['description']=''             
                newsDict[nInfo['newsid']]=nInfo
            except:
                print 'Error:',info['url']
                logging.error(info['url'])
    return newsDict

# for 4 of total 5 categories
urls=['http://it.sohu.com/techcompany/index.shtml',
      'http://it.sohu.com/internet_2014.shtml',      
      'http://it.sohu.com/tele_new.shtml',
      'http://it.sohu.com/yejie_2014.shtml']

@cost_log
def main():
    infoDict={}
    infoDict.update(getJsInfo())
    for url in urls:
        infoDict.update(getHtmlInfo(url))
    for info in infoDict.itervalues():
        try:
            table.InsertItemDict(ctable, info)
            print timeFormat.getTimeStamp(info['ctime']),info['title']
        except:
            logging.error('encoding not supported:%s'%info['url'])  
    return ctable,len(infoDict)
if __name__=='__main__':
#     getJsInfo()
#     getHtmlInfo(urls[4]) 
    main()