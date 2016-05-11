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

ctable=dbconfig.tableName['leiphone']

# http://www.leiphone.com/page/1#lph-pageList

def getHtmlInfo():
    url='http://www.leiphone.com/page/1'  
    content=getHtml(url)
#     print content
    newsList=[]
    if content:
        soup = BeautifulSoup(content, "html.parser",from_encoding='utf-8')
        soup=soup.find('div',{'class':"lph-pageList index-pageList"})
        if not soup:
            return newsList
        itemList=soup.find_all('li',{'class':'pbox clr'})
        for item in itemList:
            nInfo={}
            word=item.find('div',{'class':'word'})
            head=word.find('a')
            nInfo['url']=head.get('href')
            title=head.find('div',{'class':'tit'}).getText()
            nInfo['title']=r1(u'(?:^[【,「].*?[】,」])?(.*)',title) 
            nInfo['newsid']=getMd5(nInfo['url'])             
            desc=word.find('div',{'class':'des'})         
            nInfo['summary']=desc.getText().strip()             
            img=item.find('img',{'class':'lazy'}).get('data-original')
            if not img:
                img=item.find('img',{'class':'lazy'}).get('src')
            nInfo['thumb']=img               
            nInfo['keywords']=''         
            time_block= item.find('div',{'class':'time'})
            if not time_block:
                continue
            timeStr=' '.join(i.getText().replace(' / ','-') for i in time_block.find_all('span'))
            nInfo['ctime']= long(time.mktime(time.strptime(timeStr,'%Y-%m-%d %H:%M')))   
            author=word.find('div',{'class':'aut'})                        
            nInfo['author']=author.getText().strip() if author else ''
            nInfo['source']=ctable
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