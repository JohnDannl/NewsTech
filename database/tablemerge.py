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
               webid,url,title,newsid,thumb,summary,keywords,ctime,source,author,description,mtype,click)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.Insert(query, data)

def InsertItemMany(tablename, datas):
    for data in datas:
        InsertItem(tablename, data)

def InsertItems(tablename, datas):
    query = """INSERT INTO """ + tablename + """(
               webid,url,title,newsid,thumb,summary,keywords,ctime,source,author,description,mtype,click)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.insertMany(query, datas)

def InsertItemDict(tablename, data):
    if ChkExistRow(tablename, data['newsid']):
        return 1
    query = "INSERT INTO " + tablename + """(
             webid,url,title,newsid,thumb,summary,keywords,ctime,source,author,description,mtype,click) 
             values(%(webid)s, %(url)s, %(title)s,%(newsid)s, %(thumb)s, %(summary)s, %(keywords)s,%(ctime)s, 
             %(source)s, %(author)s, %(description)s, %(mtype)s, %(click)s)"""
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
    if rows!=-1:
        return rows[0][0]
    else:
        return rows

def getTitleBriefRecords(tablename,dayago=30):
    starttime=time.time()-24*3600*dayago
    query = "SELECT newsid,title,ctime,source FROM " + tablename+' where ctime > %s'
    rows = dbconn.Select(query, (starttime,))
    return rows

def getMaxId(tablename):
    query='select max(id) from '+tablename
    rows=dbconn.Select(query,())
    return rows[0][0]

def getTitleBriefRecordsBiggerId(tablename,tid):
    query = "SELECT newsid,title,ctime,source FROM " + tablename+' where id > %s'
    rows = dbconn.Select(query, (tid,))
    return rows

def getRecordsByNewsid(tablename,newsid):
    # return the user clicked news info,should be only one if no accident
    query = "SELECT * FROM " + tablename + """ WHERE newsid = %s""" 
    rows = dbconn.Select(query, (newsid,))   
    return rows

def getRecordsById(tablename,mtid):
    query = "SELECT * FROM " + tablename+' where id = %s'
    rows = dbconn.Select(query, (mtid,))
    return rows

def getRecordsByCtime(tablename, starttime, endtime):    
    query = "SELECT * FROM " + tablename + """ WHERE ctime >= %s AND ctime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def getTopClickRecords(tablename,topnum=10):
#     @attention: get top @param topnum: records from @param tablename:
#     order by click,that is,get hottest @param topnum: records  
    query='select * from '+tablename+' order by click desc,newsid desc limit %s'
    rows=dbconn.Select(query,(topnum,))
    return rows

def getTopECSNRecords(tablename,click,newsid,topnum=10):
#     return the topnum records whose click equals @param click: and newsid smaller than @param newsid: 
    query='select * from '+tablename+' where click = %s and newsid < %s order by click desc,newsid desc limit %s'
    rows=dbconn.Select(query,(click,newsid,topnum))
    return rows

def getTopSCRecords(tablename,click,topnum=10):
#     return the topnum records smaller click  
    query='select * from '+tablename+' where click < %s order by click desc,newsid desc limit %s'
    rows=dbconn.Select(query,(click,topnum))
    return rows

def getTitleByCtime(tablename,startday=30,enday=None):
    # return [(title,newsid),]     
    starttime=time.time()-86400*startday
    endtime=time.time()
    query = "SELECT id,title,source FROM " + tablename + """ WHERE ctime >= %s AND ctime <= %s""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def updateMtype(tablename,mtype,newsid):
    query = "UPDATE " + tablename + """ SET mtype = %s WHERE newsid = %s """
    dbconn.Update(query, (mtype,newsid))

def increaseClick(tablename,newsid):
    query = 'select click from '+tablename+""" WHERE newsid = %s """
    rows=dbconn.Select(query,(newsid,))
    if rows !=-1 and len(rows)>0:
        click=rows[0][0]
        click+=1
        query = "UPDATE " + tablename + """ SET click = %s WHERE newsid = %s"""
        dbconn.Update(query, (click,newsid))
        
def ChkExistRow(tablename, newsid):
    query = "SELECT COUNT(id) FROM " + tablename + " WHERE newsid = %s"
    row = dbconn.Select(query, (newsid,))[0][0]
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
               newsid varchar(255),                              
               thumb varchar(2048),
               summary text,
               keywords varchar(512),  
               ctime bigint, 
               source varchar(255),
               author varchar(255),
               description text,
               mtype varchar(255),
               click integer)"""
    dbconn.CreateTable(query, tablename)
    dbconn.CreateIndex('create index on %s (ctime)'%tablename)
    dbconn.CreateIndex('create index on %s (newsid)'%tablename)    
    dbconn.CreateIndex('create index on %s (click,newsid)'%tablename)

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
            