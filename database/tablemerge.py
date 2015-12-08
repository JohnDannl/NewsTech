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
    if ChkExistRow(tablename, data[3],data[10]):
        return
    query = """INSERT INTO """ + tablename + """(
               webid,url,title,newsid,thumb,summary,keywords,ctime,source,author,description,mid,mtype,click)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.Insert(query, data)

def InsertItemMany(tablename, datas):
    for data in datas:
        InsertItem(tablename, data)

def InsertItems(tablename, datas):
    query = """INSERT INTO """ + tablename + """(
               webid,url,title,newsid,thumb,summary,keywords,ctime,source,author,description,mid,mtype,click)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.insertMany(query, datas)

def InsertItemDict(tablename, data):
    if ChkExistRow(tablename, data['newsid'],data['source']):
        return 1
    query = "INSERT INTO " + tablename + """(
             webid,url,title,newsid,thumb,summary,keywords,ctime,source,author,description,mid,mtype,click) 
             values(%(webid)s, %(url)s, %(title)s,%(newsid)s, %(thumb)s, %(summary)s, %(keywords)s,%(ctime)s, 
             %(source)s, %(author)s, %(description)s, %(mid)s, %(mtype)s, %(click)s)"""
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

def getBriefRecords(tablename,dayago=30):
    starttime=time.time()-24*3600*dayago
    query = "SELECT id,title,summary,ctime,source FROM " + tablename+' where ctime > %s'
    rows = dbconn.Select(query, (starttime,))
    return rows

def getMaxWebId(tablename,web):
    query='select max(webid) from '+tablename+' where source = %s'
    rows=dbconn.Select(query,(web,))
    return rows[0][0]

def getTitleBriefRecords(tablename,dayago=30):
    starttime=time.time()-24*3600*dayago
    query = "SELECT mid,title,ctime,source FROM " + tablename+' where ctime > %s'
    rows = dbconn.Select(query, (starttime,))
    return rows

def getMaxId(tablename):
    query='select max(id) from '+tablename
    rows=dbconn.Select(query,())
    return rows[0][0]

def getTitleBriefRecordsBiggerId(tablename,tid):
    query = "SELECT mid,title,ctime,source FROM " + tablename+' where id > %s'
    rows = dbconn.Select(query, (tid,))
    return rows

def getRecordsByMid(tablename,mid):
    # return the user clicked news info,should be only one if no accident
    query = "SELECT * FROM " + tablename + """ WHERE mid = %s""" 
    rows = dbconn.Select(query, (mid,))   
    return rows

def getRecordsById(tablename,tid):
    query = "SELECT * FROM " + tablename+' where id = %s'
    rows = dbconn.Select(query, (tid,))
    return rows

def getRecordsByCtime(tablename, starttime, endtime):    
    query = "SELECT * FROM " + tablename + """ WHERE ctime >= %s AND ctime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def getTopClickRecords(tablename,topnum=10):
#     @attention: get top @param topnum: records from @param tablename:
#     order by click,that is,get hottest @param topnum: records  
    query='select * from '+tablename+' order by click desc,mid desc limit %s'
    rows=dbconn.Select(query,(topnum,))
    return rows

def getTopECSMRecords(tablename,click,mid,topnum=10):
#     return the topnum records whose click equals @param click: and newsid smaller than @param newsid: 
    query='select * from '+tablename+' where click = %s and mid < %s order by click desc,mid desc limit %s'
    rows=dbconn.Select(query,(click,mid,topnum))
    return rows

def getTopSCRecords(tablename,click,topnum=10):
#     return the topnum records smaller click  
    query='select * from '+tablename+' where click < %s order by click desc,mid desc limit %s'
    rows=dbconn.Select(query,(click,topnum))
    return rows

def getTitleByCtime(tablename,startday=30,enday=None):
    # return [(title,mid),]     
    starttime=time.time()-86400*startday
    endtime=time.time()
    query = "SELECT id,title,source FROM " + tablename + """ WHERE ctime >= %s AND ctime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def updateMtype(tablename,mtype,mid):
    query = "UPDATE " + tablename + """ SET mtype = %s WHERE mid = %s """
    dbconn.Update(query, (mtype,mid))

def increaseClick(tablename,mid):
    query = 'select click from '+tablename+""" WHERE mid = %s """
    rows=dbconn.Select(query,(mid,))
    if rows !=-1 and len(rows)>0:
        click=rows[0][0]
        click+=1
        query = "UPDATE " + tablename + """ SET click = %s WHERE mid = %s"""
        dbconn.Update(query, (click,mid))
        
def ChkExistRow(tablename, newsid,source):
    query = "SELECT COUNT(id) FROM " + tablename + " WHERE newsid = %s and source = %s"
    row = dbconn.Select(query, (newsid,source))[0][0]
    if row == 0:
        return False
    return True

def getTitleSummary(tablename):
    query = "SELECT id,title,summary,ctime,source FROM " + tablename +' order by title desc,ctime desc'
    rows = dbconn.Select(query, ())
    return rows

def CreateTable(tablename):
    query = """CREATE TABLE """ + tablename + """(
               id serial primary key, 
               webid integer,
               url varchar(2048),   
               title varchar(512),           
               newsid varchar(1024),                              
               thumb varchar(2048),
               summary varchar(10240),
               keywords varchar(512),  
               ctime bigint, 
               source varchar(255),
               author varchar(255),
               description varchar(10240),
               mid varchar(255),
               mtype varchar(255),
               click integer)"""
    dbconn.CreateTable(query, tablename)
    dbconn.CreateIndex('create index on %s (mid)'%tablename)
    dbconn.CreateIndex('create index on %s (ctime)'%tablename)
    dbconn.CreateIndex('create index on %s (newsid,source)'%tablename)    
    dbconn.CreateIndex('create index on %s (click,mid)'%tablename)

if __name__ == "__main__":
    CreateTable(dbconfig.mergetable) 
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
            