#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2014-5-3

@author: JohnDannl
'''
import time
import re
def extractTimeStamp(timeStr):
    if not timeStr:
        return
#     pattern:YYYY mm dd HH:MM
    pattern=r'.*?(\d{4}).*?(\d{2}).*?(\d{2}).*?(\d{2}):(\d{2})'
    m = re.search(pattern, timeStr)
    if m:
        return m.group(1)+'-'+m.group(2)+'-'+m.group(3)+' '+m.group(4)+':'+m.group(5)
    else:
        return extractShortTimeStamp(timeStr)
    
def extractShortTimeStamp(timeStr): 
#     in format:%Y-%m-%d    
    pattern=r'.*?(\d{4}).*?(\d{2}).*?(\d{2})'
    m=re.search(pattern,timeStr)
    if m:
        return m.group(1)+'-'+m.group(2)+'-'+m.group(3)
def getTimeStamp(seconds=-1):
    '''generate the time stamp format time string for postgresql database
    '''
    if(seconds==-1):
        timeTuple=time.localtime()  
    else:
        timeTuple=time.localtime(seconds)
    timeStr=time.strftime('%Y-%m-%d %H:%M:%S',timeTuple) 
    return timeStr

def getTimeGap(seconds=0):
    second=int(seconds%60)
    minutes=int(seconds//60)
    minute=int(minutes%60)
    hours=int(minutes//60)
    hour=int(hours)
#     timeStr=str.format('%2d h %2d m %2d s' % (hour,minute,second))
    timeStr='{:0>2d} h {:0>2d} m {:0>2d} s'.format(hour,minute,second)
    return timeStr

def getLongTime(timeStr):
    try:
        return (long)(time.mktime(time.strptime(timeStr, '%Y-%m-%d %H:%M:%S')))
    except:
        return (long)(time.mktime(time.strptime(timeStr, '%Y-%m-%d %H:%M')))

if __name__=='__main__':
    print 1406645511853
    print time.time()
    print 2**32
    print type(int(1406645511853))
    from sys import getsizeof
    print getsizeof(1),getsizeof(1406645511853),getsizeof(1.0)    
#     print time.ctime()
#     print getTimeStamp(1406858133)
#     print getLongTime('2014-07-25 12:10:10')    
#     print getTimeStamp(time.time()-3600) 
#     print getTimeStamp(1431842125.8)
#     print getTimeGap(3701)   
