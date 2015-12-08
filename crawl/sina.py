#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Created on 2015-5-13

@author: JohnDannl
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


ctable=dbconfig.tableName['sina']

# http://tech.sina.com.cn/
# http://feed.mix.sina.com.cn/api/roll/get?pageid=1&lid=21&num=30&versionNumber=1.2.6&page=1&encode=utf-8
# &callback=feedCardJsonpCallback&_=1431564274159
# "commentid": "kj:comos-cpkqeaz4163931:0"
# http://comment5.news.sina.com.cn/page/info?version=1&format=js&channel=kj&newsid=comos-cpkqeaz4163931
# &group=0&compress=1&ie=utf-8&oe=utf-8&page=1&show_reply=1&page_size=20&jsvar=loader_1431566275233_9905542

def getHtmlInfo():
    url=r'http://video.sina.com.cn/news/'   
    content=getHtml(url)
#     print content
    newsList=[]
    if content:
        soup = BeautifulSoup(content, from_encoding='gbk')
        videoList=soup.find_all('div',{'suda-uatrack-key':"news_video"})
        for item in videoList:
            nInfo={}
            nInfo['vid']=item.find('div',{'class':"news-item-count"}).get('data-vid-count')
            nInfo['title']=item.get('data-title') 
            nInfo['url']=item.get('data-url')
            nInfo['thumb']=item.find('img').get('src')
            nInfo['summary']=item.find('p',{'class':"desc"}).getText()
            nInfo['keywords']=item.get('data-key')
            nInfo['newsid']=item.get('data-newsid')        
            nInfo['duration']=''
            nInfo['web']=ctable
            try:
                subContent=getHtml(nInfo['url'])
                subSoup=BeautifulSoup(subContent, from_encoding='utf-8')
                tblock=subSoup.find('p',{'class':"channel"})
                nInfo['vtype']= tblock.find('a').getText()
                fblock=subSoup.find('p',{'class':"from"})
                nInfo['source']= fblock.find_all('span')[1].getText().replace(u'来源：','')
                nInfo['related']='' # related news is no needed
                block2=subSoup.find('p',{'class':"from"})
                timeStr=block2.find('em').getText()
                nInfo['loadtime']= timeFormat.extractTimeStamp(timeStr)
                newsList.append(nInfo) 
                print nInfo['loadtime'],nInfo['url'] 
            except:
                print 'Error: ',nInfo['url']
#                 logging.error('Error: '+nInfo['url'])
    return newsList

def getJsInfo():
    url=r'http://feed.mix.sina.com.cn/api/roll/get?pageid=1&lid=21&num=30&versionNumber=1.2.6&page=1&encode=utf-8&callback=feedCardJsonpCallback&_='
    url+=str(long(time.time()*1000))
#     print url
    content=getHtml(url)
#     print content
   
    newsList=[]
    if content:
        info=json.loads(r1('.*?\((\{.*\})\)',content),encoding='utf-8')
        if info.has_key('result'):
            tResult=info['result']  
            infoList=[]
            if 'data' in tResult:
                infoList+=tResult['data']
#             if 'cre' in tResult:
#                 infoList+=tResult['cre']
#             if 'pdps' in tResult:
#                 infoList+=tResult['pdps']
#             if 'top' in tResult:
#                 infoList+=tResult['top']
            for info in infoList:
                try:
                    nInfo={}
                    nInfo['newsid']=getMd5(info['url'])
                    nInfo['title']= info['title']                
                    nInfo['url']=info['url']                
                    nInfo['summary']=info['summary']
                    nInfo['thumb']=info['img']['u']                    
                    nInfo['keywords']=info['keywords'] if 'keywords' in info else ''
                    nInfo['source']=ctable
                    nInfo['ctime']=long(info['ctime'])   
                    nInfo['author']=info['author']
                    nInfo['description']=''
                    newsList.append(nInfo)
                except:
                    print 'Error:',info['url']
                    logging.error(info['url'])
    return newsList

@cost_log
def main():
    infoList=[]
    infoList+=getJsInfo()   
    for info in infoList:
        try:
#             table.InsertItemDict(ctable, info)
            print timeFormat.getTimeStamp(info['ctime']),info['title']
        except:
            logging.error('encoding not supported:%s'%info['url'])
    return ctable,len(infoList)
        
if __name__=='__main__':
#     getJsInfo()
    main()
    