#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-5-16

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

ctable=dbconfig.tableName['ittime']

# http://news.ittime.com.cn/newslist.shtml

def getHtmlInfo():
    domain='http://news.ittime.com.cn'
    url='http://news.ittime.com.cn/newslist.shtml'   
    content=getHtml(url)
#     print content
    newsList=[]
    if content:
        soup = BeautifulSoup(content,"html.parser", from_encoding='utf-8')
        itemList=soup.find_all('div',{'class':"left-list"})
        for item in itemList:
            nInfo={}
            head=item.find('h3').find('a')
            nInfo['url']=domain+head.get('href')
            nInfo['title']=head.getText()
            nInfo['newsid']=getMd5(nInfo['url'])   
            desc=item.find('p')             
            nInfo['summary']=desc.getText()  
            img=item.find('a',{'class':'img_212'}).find('img')
            nInfo['thumb']=domain+img.get('src')
            nInfo['keywords']=','.join([i.getText() if i.getText() else '' for i in item.find('span',{'style':'float:left;'}).find_all('a')])
            timeStr=r1('(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})',item.find('div',{'class':'box-other1'}).get_text())
            nInfo['ctime']= long(time.mktime(time.strptime(timeStr,'%Y-%m-%d %H:%M:%S')))         
            nInfo['source']=ctable
            author=item.find('div',{'class':'box-other3'}).find('a')
            nInfo['author']=author.getText() if author else ''
            nInfo['description']=str(desc)
#             print nInfo['ctime'],nInfo['title']
#             print nInfo['newsid'],nInfo['url']
#             print nInfo['author'],nInfo['thumb']
#             print nInfo['keywords'],nInfo['summary']
            newsList.append(nInfo)
    return newsList

def getJsInfo():
    url=r'http://feed.mix.sina.com.cn/api/roll/get?pageid=1&lid=21&num=30&versionNumber=1.2.6&page=1&encode=utf-8&callback=feedCardJsonpCallback&_='
    url+=str(time.time()*1000)
    print url
    content=getHtml(url)
    print content
   
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
                    nInfo['newsid']=r1('.*/(.*?)\.',info['url'])
                    nInfo['title']= info['title']                
                    nInfo['url']=info['url']                
                    nInfo['summary']=info['summary']
                    nInfo['thumb']=info['img']['u'] 
#                     if len(info['img'])>0 and 'u' in info['img']:
#                         nInfo['thumb']=info['img']['u'] 
#                     elif 'images' in info and len(info['images'])>0:
#                         nInfo['thumb']=info['images'][0]['u']
                    nInfo['keywords']=info['keywords'] if 'keywords' in info else ''
                    nInfo['commentid']=info['commentid']
                    nInfo['type']='tech'
                    nInfo['source']=ctable
                    nInfo['ctime']=long(info['ctime'])             
                    nInfo['wapurl']=info['wapurl'] if 'wapurl' in info else ''                   
                    newsList.append(nInfo)
#                     print nInfo['ctime']
#                     print nInfo['waptitle']
#                     print nInfo['wapurl']
#                     print nInfo['wapsummary']
                except:
                    print 'Error:',info['url']
                    logging.error(info['url'])
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