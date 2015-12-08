#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on 2014-9-17

@author: JohnDannl
'''
from table import dbconn as dbconn
from dbconfig import tableName as tableName
import time

import dbconfig

def InsertItem(tablename, data):    
    if ChkExistRow(tablename, data[13]):
        return
    query = """INSERT INTO """ + tablename + """(
               mtid,url,title,newsid,thumb,summary,keywords,ctime,commentid,type,source,wapurl,img,mid,mtype,related)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.Insert(query, data)

def InsertItemMany(tablename, datas):
    for data in datas:
        InsertItem(tablename, data)

def InsertItems(tablename, datas):
    query = """INSERT INTO """ + tablename + """(
               mtid,url,title,newsid,thumb,summary,keywords,ctime,commentid,type,source,wapurl,img,mid,mtype,related)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.insertMany(query, datas)

def InsertItemDict(tablename, data):
    if ChkExistRow(tablename, data['mid']):
        return 1
    query = "INSERT INTO " + tablename + """(
             mtid,url,title,newsid,thumb,summary,keywords,ctime,commentid,type,source,wapurl,img,mid,mtype,related) 
             values(%(mtid)s, %(url)s, %(title)s,%(newsid)s, %(thumb)s, %(summary)s, %(keywords)s,%(ctime)s,%(commentid)s, 
             %(type)s,%(source)s, %(wapurl)s, %(img)s, %(mid)s, %(mtype)s, %(related)s)"""
    dbconn.Insert(query, data)
    return 0

def getAllCount(tablename):
    query="select count(id) from "+tablename
    count=dbconn.Select(query,())[0][0]
    return count

def getAllRecords(tablename):
    query = "SELECT * FROM " + tablename
    rows = dbconn.Select(query, ())
    return rows

def getTitleBriefRecords(tablename,dayago=30):
    starttime=time.time()-24*3600*dayago
    query = "SELECT mid,title,ctime,source FROM " + tablename+' where ctime > %s'
    rows = dbconn.Select(query, (starttime,))
    return rows

def getMaxMtId(tablename):
    query='select max(mtid) from '+tablename
    rows=dbconn.Select(query,())
    return rows[0][0]

def getRecordsByCtime(tablename, starttime, endtime):    
    query = "SELECT * FROM " + tablename + """ WHERE ctime >= %s AND ctime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def getTitleByCtime(tablename,startday=30,enday=None):
    # return [(title,mid),]     
    starttime=time.time()-86400*startday
    endtime=time.time()
    query = "SELECT title,mid FROM " + tablename + """ WHERE ctime >= %s AND ctime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

# def getRecordsBySourceNewsid(tablename,source,newsid):
#     # return the user clicked news info,should be only one if no accident
#     query = "SELECT title,mid,mtype FROM " + tablename + """ WHERE source = %s AND newsid = %s""" 
#     rows = dbconn.Select(query, (source,newsid))   
#     return rows

def getRecordsByMid(tablename,mid):
    # return the user clicked news info,should be only one if no accident
    query = "SELECT * FROM " + tablename + """ WHERE mid = %s""" 
    rows = dbconn.Select(query, (mid,))   
    return rows

def getTopRecords(tablename,topnum=10,mtype=None):
#     @attention: get top @param topnum: records from @param tablename:
#     order by time,that is,get recent @param topnum: records  
    if not mtype:
        query='select * from '+tablename+' order by ctime desc,mid desc limit %s'
        rows=dbconn.Select(query,(topnum,))
    else:
        query='select * from '+tablename+' where mtype = %s order by ctime desc,mid desc limit %s'
        rows=dbconn.Select(query,(mtype,topnum))
    return rows

def getTopETSMRecords(tablename,ctime,mid,topnum=10,mtype=None):
#     return the topnum records whose ctime equals @param ctime: and mid smaller than @param mid:
    if not mtype: 
        query='select * from '+tablename+' where ctime = %s and mid < %s order by ctime desc,mid desc limit %s'
        rows=dbconn.Select(query,(ctime,mid,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and ctime = %s and mid < %s order by ctime desc,mid desc limit %s'
        rows=dbconn.Select(query,(mtype,ctime,mid,topnum))
    return rows

def getTopSTRecords(tablename,ctime,topnum=10,mtype=None):
#     return the topnum records smaller ctime  
    if not mtype:
        query='select * from '+tablename+' where ctime < %s order by ctime desc,mid desc limit %s'
        rows=dbconn.Select(query,(ctime,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and ctime < %s order by ctime desc,mid desc limit %s'
        rows=dbconn.Select(query,(mtype,ctime,topnum))
    return rows

def getBottomETBMRecords(tablename,ctime,mid,topnum=10,mtype=None):
#     return the bottom records equal ctime bigger mid
    if not mtype:
        query='select * from '+tablename+' where ctime = %s and mid > %s order by ctime asc,mid asc limit %s'
        rows=dbconn.Select(query,(ctime,mid,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and ctime = %s and mid > %s order by ctime asc,mid asc limit %s'
        rows=dbconn.Select(query,(mtype,ctime,mid,topnum))
    return rows

def getBottomBTRecords(tablename,ctime,topnum=10,mtype=None):
#     return the bottom records bigger ctime bigger mid
    if not mtype:
        query='select * from '+tablename+' where ctime > %s order by ctime asc,mid asc limit %s'
        rows=dbconn.Select(query,(ctime,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and ctime > %s order by ctime asc,mid asc limit %s'
        rows=dbconn.Select(query,(mtype,ctime,topnum))
    return rows

def ChkExistRow(tablename, mid):
    query = "SELECT COUNT(id) FROM " + tablename + " WHERE mid = %s"
    row = dbconn.Select(query, (mid,))[0][0]
    if row == 0:
        return False
    return True

def updateMtype(tablename,mtype,source,mid):
    query = "UPDATE " + tablename + """ SET mtype = %s WHERE  mid = %s"""
    dbconn.Update(query, (mtype,source,mid))

# def getRelated(tablename):
#     query = 'select related from '+tablename+""" WHERE related !='' """
#     rows=dbconn.Select(query,())    
#     print rows
#     print rows[0][0]
    
def addRelated(tablename,mid,addmid):
    query = 'select related from '+tablename+""" WHERE mid = %s"""
    rows=dbconn.Select(query,(mid,))
    if rows !=-1 and len(rows)>0:        
        related=rows[0][0]
        related+=';;'+addmid
        query = "UPDATE " + tablename + """ SET related = %s WHERE mid = %s"""
        dbconn.Update(query, (related,mid))
        
def getTitleSummary(tablename):
    query = "SELECT mtid,title,summary,ctime,source FROM " + tablename +' order by title desc,ctime desc'
    rows = dbconn.Select(query, ())
    return rows

def CreateTable(tablename):
    query = """CREATE TABLE """ + tablename + """(
               id serial primary key, 
               mtid integer,
               url varchar(4096),   
               title varchar(512),           
               newsid varchar(1024),                              
               thumb varchar(4096),
               summary varchar(10240),
               keywords varchar(512),  
               ctime bigint, 
               commentid varchar(4096),            
               type varchar(255),
               source varchar(255),
               wapurl varchar(4096),
               img varchar(4096),
               mid varchar(255),
               mtype varchar(255),
               related varchar(4096))"""
    dbconn.CreateTable(query, tablename)      
    dbconn.CreateIndex('create index on %s (ctime)'%tablename)
    dbconn.CreateIndex('create index on %s (ctime,mid)'%tablename)
    dbconn.CreateIndex('create index on %s (mid)'%tablename)
    dbconn.CreateIndex('create index on %s (mtid)'%tablename)

if __name__ == "__main__":    
    CreateTable(dbconfig.mergetable2) 
#     getRelated(dbconfig.mergetable2)
#     print getMaxId(dbconfig.mergetable,'sohu')
#     rows=getBottomETBVRecords(dbconfig.tableName[2],'2014-09-04 10:09:02','1310457')
#     rows=getBottomBTRecords(dbconfig.tableName[2],'2014-09-04 10:09:02',10)
#     rows=getTopETSVRecords(dbconfig.tableName[2],'2014-09-04 10:09:02','1310458')
#     rows=getTopSTRecords(dbconfig.tableName[2],'2014-09-04 10:09:02','10')
#     if rows !=-1:
#         for item in rows:
#             print item[1],item[11]  
            
#     rows=getTopUrls(dbconfig.tableName[0],10)  
#     if rows !=-1:
#         for item in rows:
#             print item[1],item[0]     
            