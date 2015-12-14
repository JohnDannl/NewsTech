#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-11-12

@author: JohnDannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')
sys.path.append(r'../crawl')
sys.path.append(r'../aggregate')
sys.path.append(r'../crawl_mpd')
#from apscheduler.scheduler import Scheduler
from crawl import bnet,ciweek,cnet,csdn,donews,geekpark,hiapk,huxiu,ifanr,ittime,\
    leiphone,pingwest,pintu360,qq,sina,sohu,techcrunch,technews,techweb,tmt,\
    w163,w36kr,zdnet,zhidx,zol,feng
from common import timeFormat
from aggregate import merge,merge2
import multiprocessing
import time
# sched = Scheduler()  
# sched.daemonic = False 
# sched.start() 
 
# @sched.cron_schedule(hour='*/3',minute='25',second='15')
# def newsCrawl():
#     sina.main()
#     sohu.main()
#     v1.main()
#     kankan.main()
#     ifeng.main()
#     china.main()
#     qq.main()
#     aggregate.main()
#     print 'Main thread begins to sleep'

# @sched.cron_schedule(hour='*',minute='*/30',second='31')
# def newsCrawl():  
#     call_async_3()
#     aggregate.main()
#     print 'Main thread begins to sleep at time %s' %(timeformat.getTimeStamp(),)
# webs=[able2do,alibuybuy,bianews,bnet,ciweek,cnet,csdn,donews,geekpark,hiapk,\
#     huxiu,ifanr,ittime,leiphone,pingwest,pintu360,sina,sohu,techcrunch,technews,\
#     techweb,tmt,w163,w36kr,zdnet,zhidx,zol]

webdic={'sina':sina,'sohu':sohu,'w163':w163,'huxiu':huxiu,'ittime':ittime,
       'w36kr':w36kr,'leiphone':leiphone,'ifanr':ifanr,'zol':zol,'tmt':tmt,
       'csdn':csdn,'ciweek':ciweek,'geekpark':geekpark,'donews':donews,'zhidx':zhidx,
       'techweb':techweb,'bnet':bnet,'cnet':cnet,'techcrunch':techcrunch,'technews':technews,
       'zdnet':zdnet,'pingwest':pingwest,'pintu360':pintu360,'hiapk':hiapk,'qq':qq,
       'feng':feng}
webs=['bnet','ciweek','cnet','csdn','donews','geekpark','hiapk','huxiu','ifanr','ittime',\
      'leiphone','pingwest','pintu360','qq','sina','sohu','techcrunch','technews','techweb','tmt',\
      'w163','w36kr','zdnet','zhidx','zol','feng']

count=0
def call_sync():
    global count       
    count+=1
    if count%24==0:
        merge.garbageDepos(20) 
        merge2.garbageDepos(20)
    for web in webs:
        webdic[web].main()
        merge.mergeWeb(web)
        merge2.mergeWeb()
        print 'Main thread begins to sleep at time %s' %(timeFormat.getTimeStamp(),)
        time.sleep(120)
    
def call_async():
    # Just like single-processing,why?
    # if the function is not named main,'()'is needed
    oldtime=time.time()
    pool=multiprocessing.Pool() # if none will use default :cpu_count() processings     
    pool.apply_async(bnet.main())    
    pool.apply_async(ciweek.main())
    pool.apply_async(cnet.main())    
    pool.apply_async(csdn.main)    
    pool.close()
    pool.join()
    msg='Total time cost: %s (seconds)' % (time.time()-oldtime,)     
    print msg  

def call_crawl():
    for web in webs:
        webdic[web].main()
if __name__=='__main__':    
#     call_crawl()
    while True:
        call_sync()
#         aggregate.main()
#         print 'Main thread begins to sleep at time %s' %(timeformat.getTimeStamp(),)
#         time.sleep(1800)
        
