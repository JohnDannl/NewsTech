#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import db
dbconn = db.pgdb()
import dbconfig
import time

def InsertItem(tablename, data):    
    if ChkExistRow(tablename, data[2]):
        return
    query = """INSERT INTO """ + tablename + """(
               url,title,newsid,thumb,summary,keywords,ctime,source,author,description)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.Insert(query, data)

def InsertItemMany(tablename, datas):
    for data in datas:
        InsertItem(tablename, data)

def InsertItems(tablename, datas):
    query = """INSERT INTO """ + tablename + """(
               url,title,newsid,thumb,summary,keywords,ctime,source,author,description)
               values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    dbconn.insertMany(query, datas)

def InsertItemDict(tablename, data):
    if ChkExistRow(tablename, data['newsid']):
        return 1
    query = "INSERT INTO " + tablename + """(
             url,title,newsid,thumb,summary,keywords,ctime,source,author,description) 
             values(%(url)s, %(title)s,%(newsid)s, %(thumb)s, %(summary)s, %(keywords)s,%(ctime)s, 
             %(source)s, %(author)s, %(description)s)"""
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

def getMaxId(tablename):
    query='select max(id) from '+tablename
    rows=dbconn.Select(query,())
    return rows[0][0]

def getBriefRecordsBiggerId(tablename,tid):
    query = "SELECT id,title,summary,ctime,source FROM " + tablename+' where id > %s'
    rows = dbconn.Select(query, (tid,))
    return rows

def getRecordsById(tablename,tid):
    query = "SELECT * FROM " + tablename+' where id = %s'
    rows = dbconn.Select(query, (tid,))
    return rows

def getRecordsByCtime(tablename, starttime, endtime):
    '''@param tablename: table name
    @param starttime: the start time of query in seconds from the Epoch
    @param endtime: the end time of query in seconds from the Epoch
    '''
    query = "SELECT * FROM " + tablename + """ WHERE ctime >= %s AND ctime <= %s order by ctime desc""" 
    rows = dbconn.Select(query, (starttime,endtime))   
    return rows

def getRecordsBiggerId(tablename,mId):
#     return records whose id > @param mId: 
    query='select * from '+tablename+' where id > %s order by id asc'
    rows=dbconn.Select(query,(mId,))
    return rows

def getUrlByNewsid(tablename,newsid):
#     return url by newsid
    query='select url from '+tablename+' where newsid = %s'
    rows=dbconn.Select(query,(newsid,))
    return rows

def getTopUrls(tablename,topnum=10):
#     return [(url,newsid),]
    query='select url,newsid from '+tablename+' order by ctime desc,newsid desc limit %s'
    rows=dbconn.Select(query,(topnum,))
    return rows

# def deleteRecord(tablename,abspath):
#     if not ChkExistRow(tablename, abspath):
#         return
#     else:
#         print 'delete the record:'+abspath
#     timeTuple=time.localtime()  
#     timeStr=time.strftime('%Y-%m-%d %H:%M:%S',timeTuple) 
#     query="update "+tablename+" set deletetime=%s,available=%s where abspath=%s"
#     dbconn.Update(query, [timeStr,'false',abspath])
     
# def UpdateStatus(tablename, column, data):
#     query = "UPDATE " + tablename + """ SET """+ column + """ = %s WHERE available = %s"""
#     dbconn.Update(query, data)
     
# def restoreRecord(tablename,data):
#     if ChkExistRow(tablename, data[2]):
#         query = """update """ + tablename + """ set size=%s,
#                 loadtime=%s, available=%s
#                 where abspath=%s"""
#         tmp=data[2:5]
#         tmp.append(data[2])
#     dbconn.Update(query, tmp)

# def vtypeStatistic(tablename):
#     query = "SELECT vtype,COUNT(*) FROM " + tablename + " group by vtype"
#     rows=dbconn.Select(query,())    
#     if rows!=-1 and len(rows)>0:
#         with open(r'./type.txt','a') as fout:
#             fout.write(tablename+':\n')
#             print tablename,':'
#             for row in rows:
#                 fout.write('{:<20s}{:>10d}\n'.format(row[0],row[1]))
#                 print '{:<20s}{:>10d}'.format(row[0],row[1])
                
def ChkExistRow(tablename, newsid):
    query = "SELECT COUNT(id) FROM " + tablename + " WHERE newsid = %s"
    row = dbconn.Select(query, (newsid,))[0][0]
    if row == 0:
        return False
    return True
                
def CreateNewsTable(tablename):
    query = """CREATE TABLE """ + tablename + """(
               id serial primary key, 
               url varchar(2048),   
               title varchar(512),           
               newsid varchar(1024),                              
               thumb varchar(2048),
               summary varchar(10240),
               keywords varchar(512),  
               ctime bigint,         
               source varchar(255),
               author varchar(255),
               description varchar(10240))"""
    dbconn.CreateTable(query, tablename)
    dbconn.CreateIndex('create index on %s (newsid)'%tablename)
    dbconn.CreateIndex('create index on %s (ctime)'%tablename)

def ReIndex(tablename):
    if dbconn.ReIndex(tablename)!=-1:
        print '%s reindex successfully!'%tablename
    else:
        print 'Failure:reindex %s'%tablename
    
if __name__ == "__main__":
    CreateNewsTable(dbconfig.tableName['huxiu'])
#     for tablename in dbconfig.tableName.itervalues():
#         CreateNewsTable(tablename)
    
#     rows=getTopETBVRecords(dbconfig.tableName[2],'2014-09-04 10:09:02','1310457')
#     if rows !=-1:
#         for item in rows:
#             print item[1],item[11]  
            
#     rows=getTopUrls(dbconfig.tableName[0],10)  
#     if rows !=-1:
#         for item in rows:
#             print item[1],item[0]  
     
#     rows=getUrlByVid(dbconfig.tableName[2],r'1310945')
#     if rows !=-1:
#         print rows[0][0] 
#     for web in dbconfig.tableName:
#         vtypeStatistic(web)