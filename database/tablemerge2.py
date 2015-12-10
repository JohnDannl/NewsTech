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
    if ChkExistRow(tablename, data[3]):
        return
    query = """INSERT INTO """ + tablename + """(
               mtid,url,title,newsid,thumb,summary,keywords,ctime,source,author,description,mtype,related)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.Insert(query, data)

def InsertItemMany(tablename, datas):
    for data in datas:
        InsertItem(tablename, data)

def InsertItems(tablename, datas):
    query = """INSERT INTO """ + tablename + """(
               mtid,url,title,newsid,thumb,summary,keywords,ctime,source,author,description,mtype,related)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.insertMany(query, datas)

def InsertItemDict(tablename, data):
    if ChkExistRow(tablename, data['newsid']):
        return 1
    query = "INSERT INTO " + tablename + """(
             mtid,url,title,newsid,thumb,summary,keywords,ctime,source,author,description,mtype,related) 
             values(%(mtid)s, %(url)s, %(title)s,%(newsid)s, %(thumb)s, %(summary)s, %(keywords)s,%(ctime)s, 
             %(source)s, %(author)s, %(description)s,%(mtype)s, %(related)s)"""
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
    query = "SELECT newsid,title,ctime,source FROM " + tablename+' where ctime > %s'
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
    # return [(title,newsid),]     
    starttime=time.time()-86400*startday
    endtime=time.time()
    query = "SELECT title,newsid FROM " + tablename + """ WHERE ctime >= %s AND ctime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

# def getRecordsBySourceNewsid(tablename,source,newsid):
#     # return the user clicked news info,should be only one if no accident
#     query = "SELECT title,mid,mtype FROM " + tablename + """ WHERE source = %s AND newsid = %s""" 
#     rows = dbconn.Select(query, (source,newsid))   
#     return rows

def getRecordsByNewsid(tablename,newsid):
    # return the user clicked news info,should be only one if no accident
    query = "SELECT * FROM " + tablename + """ WHERE newsid = %s""" 
    rows = dbconn.Select(query, (newsid,))   
    return rows

def getTopRecords(tablename,topnum=10,mtype=None):
#     @attention: get top @param topnum: records from @param tablename:
#     order by time,that is,get recent @param topnum: records  
    if not mtype:
        query='select * from '+tablename+' order by ctime desc,newsid desc limit %s'
        rows=dbconn.Select(query,(topnum,))
    else:
        query='select * from '+tablename+' where mtype = %s order by ctime desc,newsid desc limit %s'
        rows=dbconn.Select(query,(mtype,topnum))
    return rows

def getTopETSNRecords(tablename,ctime,newsid,topnum=10,mtype=None):
#     return the topnum records whose ctime equals @param ctime: and newsid smaller than @param newsid:
    if not mtype: 
        query='select * from '+tablename+' where ctime = %s and newsid < %s order by ctime desc,newsid desc limit %s'
        rows=dbconn.Select(query,(ctime,newsid,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and ctime = %s and newsid < %s order by ctime desc,newsid desc limit %s'
        rows=dbconn.Select(query,(mtype,ctime,newsid,topnum))
    return rows

def getTopSTRecords(tablename,ctime,topnum=10,mtype=None):
#     return the topnum records smaller ctime  
    if not mtype:
        query='select * from '+tablename+' where ctime < %s order by ctime desc,newsid desc limit %s'
        rows=dbconn.Select(query,(ctime,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and ctime < %s order by ctime desc,newsid desc limit %s'
        rows=dbconn.Select(query,(mtype,ctime,topnum))
    return rows

def getBottomETBNRecords(tablename,ctime,newsid,topnum=10,mtype=None):
#     return the bottom records equal ctime bigger newsid
    if not mtype:
        query='select * from '+tablename+' where ctime = %s and newsid > %s order by ctime asc,newsid asc limit %s'
        rows=dbconn.Select(query,(ctime,newsid,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and ctime = %s and newsid > %s order by ctime asc,newsid asc limit %s'
        rows=dbconn.Select(query,(mtype,ctime,newsid,topnum))
    return rows

def getBottomBTRecords(tablename,ctime,topnum=10,mtype=None):
#     return the bottom records bigger ctime bigger newsid
    if not mtype:
        query='select * from '+tablename+' where ctime > %s order by ctime asc,newsid asc limit %s'
        rows=dbconn.Select(query,(ctime,topnum))
    else:
        query='select * from '+tablename+' where mtype = %s and ctime > %s order by ctime asc,newsid asc limit %s'
        rows=dbconn.Select(query,(mtype,ctime,topnum))
    return rows

def ChkExistRow(tablename, newsid):
    query = "SELECT COUNT(id) FROM " + tablename + " WHERE newsid = %s"
    row = dbconn.Select(query, (newsid,))[0][0]
    if row == 0:
        return False
    return True

def updateMtype(tablename,mtype,newsid):
    query = "UPDATE " + tablename + """ SET mtype = %s WHERE  newsid = %s"""
    dbconn.Update(query, (mtype,newsid))

# def getRelated(tablename):
#     query = 'select related from '+tablename+""" WHERE related !='' """
#     rows=dbconn.Select(query,())    
#     print rows
#     print rows[0][0]
    
def addRelated(tablename,newsid,addnewsid):
    query = 'select related from '+tablename+""" WHERE newsid = %s"""
    rows=dbconn.Select(query,(newsid,))
    if rows !=-1 and len(rows)>0:        
        related=rows[0][0]
        related+=','+addnewsid
        query = "UPDATE " + tablename + """ SET related = %s WHERE newsid = %s"""
        dbconn.Update(query, (related,newsid))
        
def getTitleSummary(tablename):
    query = "SELECT mtid,title,summary,ctime,source FROM " + tablename +' order by title desc,ctime desc'
    rows = dbconn.Select(query, ())
    return rows

def CreateTable(tablename):
    query = """CREATE TABLE """ + tablename + """(
               id serial primary key, 
               mtid integer,
               url varchar(2048),   
               title varchar(512),           
               newsid varchar(255),                              
               thumb varchar(2048),
               summary text,
               keywords varchar(512),  
               ctime bigint, 
               source varchar(255),
               author varchar(255),
               description text,
               mtype varchar(255),
               related varchar(4096))"""
    dbconn.CreateTable(query, tablename)      
    dbconn.CreateIndex('create index on %s (ctime)'%tablename)
    dbconn.CreateIndex('create index on %s (ctime,newsid)'%tablename)
    dbconn.CreateIndex('create index on %s (newsid)'%tablename)
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
            