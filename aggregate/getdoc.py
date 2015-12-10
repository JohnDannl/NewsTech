#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-6-16

@author: dannl
'''
import jieba
from database import table,dbconfig,tablemerge
from common.punckit import delpunc
import time

oldtime=time.time()

class Doc(object):
    def __init__(self,uid,ctime,source):
        self.uid=uid
        self.ctime=ctime        
        self.source=source
        
def get_records_dayago(tablename,dayago=30):
    if dbconfig.mergetable == tablename:
        rows=tablemerge.getBriefRecords(tablename, dayago)
    else:
        rows=table.getBriefRecords(tablename,dayago)
    if rows== -1:
        print 'error table getBriefRecords'
        return   
    docs={}
    for row in rows:
        # id,title,summary,ctime,source
        summary=row[2].strip() if row[2] and row[2].strip() else row[1].strip()
        docs[Doc(row[0],row[3],row[4])]=delpunc(' '.join(jieba.cut(summary)).lower()).split()
    return docs

def get_records_newadded(web):
    m_maxid=tablemerge.getMaxWebId(dbconfig.mergetable, web)    
    if not m_maxid:
        m_maxid=-1
    w_maxid=table.getMaxId(web)    
    docs={}
    if w_maxid>m_maxid:
        rows=table.getBriefRecordsBiggerId(web, m_maxid)
        if rows==-1:
            print 'error table getBriefRecordsBiggerId'
            return
        if len(rows[0])>0:      # the first element is not null
            for row in rows:
                # id,title,summary,ctime,source
                summary=row[2].strip() if row[2] and row[2].strip() else row[1].strip()
                if summary:
                    docs[Doc(row[0],row[3],row[4])]=delpunc(' '.join(jieba.cut(summary)).lower()).split()
    return docs        
            
if __name__=='__main__':
#     docs=get_records_dayago(dbconfig.tableName['sohu'])
    docs=get_records_newadded(dbconfig.tableName['sohu'])
    if docs:
        for doc,summary in docs.iteritems():
            print doc.uid,doc.source,doc.ctime,' '.join(summary)
    print len(docs)
        