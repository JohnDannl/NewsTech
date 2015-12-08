#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import re
import urllib2
import os
import hashlib
import time
import cookielib 
from StringIO import StringIO
import gzip
import logging,functools

__all__=['r1','cost_log','getHtml','getHtmlwithCookie','getHtmlwithSinaCookie','getHtmlwithQQCookie']

def r1(pattern, text):
    m = re.search(pattern, text)
    if m:
        return m.group(1)
def cost_log(func):
    @functools.wraps(func)
    def wrapper(*args,**kw):
        oldtime=time.time()
        web,num=func(*args,**kw)
        timecost=time.time()-oldtime
        msg='%s crawled %d article(s),time cost:%.2f s'%(web,num,timecost)
        logging.info(msg)
        print msg
        return web,num
    return wrapper

def getHtml(url): 
    r=urllib2.Request(url)
    r.add_header("Accept-Language","zh-cn,en-us;q=0.7,en;q=0.3")
    r.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.2; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0")
    try:
        content=urllib2.urlopen(r, timeout=3).read()
        time.sleep(0.3)
        return content
    except:
        return None
    
def getHtmlwithCookie(url,headers): 
    ''' headers is like:
    [('Host', 'api.v1.cn'),
     ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0'),
     ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), 
     ('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
     ('Connection', 'keep-alive'),
     ('Accept-Encoding','gzip, deflate'),
     ('Referer', 'http://news.v1.cn/')] 
    '''
    cookiejar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    opener.addheaders = headers   
    try:
        response=opener.open(url)        
        if response.info().get('Content-Encoding') == 'gzip':
            buf = StringIO( response.read())
            f = gzip.GzipFile(fileobj=buf)
            content = f.read()
        else:
            content=response.read()
        time.sleep(0.3)
        return content
    except:
        return None
    
def getHtmlwithSinaCookie(url): 
    cookiejar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    opener.addheaders = [('Host', 'api.roll.news.sina.com.cn'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0'),
                         ('Accept', '*/*'), 
                         ('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
                         ('Connection', 'keep-alive'),
                         ('Referer', 'http://video.sina.com.cn/news/')]    
    try:
        content=opener.open(url).read()
        time.sleep(0.3)
        return content
    except:
        return None

def getHtmlwithQQCookie(url): 
    cookiejar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    opener.addheaders = [('Host', 'v.qq.com'),
                         ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0'),
                         ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), 
                         ('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'),
                         ('Connection', 'keep-alive'),
                         ('Referer', 'http://v.qq.com/news/')]    
    try:
        content=opener.open(url).read()
        time.sleep(0.3)
        return content
    except:
        return None    