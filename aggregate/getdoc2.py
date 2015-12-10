#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-6-16

@author: dannl
'''
import jieba
from database import dbconfig,tablemerge,tablemerge2
from common.punckit import delpunc
import time

oldtime=time.time()

class Doc(object):
    def __init__(self,uid,ctime,source):
        self.uid=uid
        self.ctime=ctime        
        self.source=source
        
def get_records_dayago(dayago=30):        
    rows=tablemerge2.getTitleBriefRecords(dbconfig.mergetable2, dayago)
    if rows== -1:
        print 'error tablemerge2 getTitleBriefRecords'
        return   
    docs={}
    for row in rows:
        # newsid,title,ctime,source,using newsid for convenience to add related news
        title=row[1].strip()
        docs[Doc(row[0],row[2],row[3])]=delpunc(' '.join(jieba.cut(title)).lower()).split()
    return docs

def get_records_newadded():
    m2_maxid=tablemerge2.getMaxMtId(dbconfig.mergetable2)    
    if not m2_maxid:
        m2_maxid=-1
    m_maxid=tablemerge.getMaxId(dbconfig.mergetable)
    docs={}
    if m_maxid>m2_maxid:        
        rows=tablemerge.getTitleBriefRecordsBiggerId(dbconfig.mergetable, m2_maxid)
        if rows==-1:
            print 'error tablemerge getTitleBriefRecordsBiggerId'
            return
        if len(rows[0])>0:      # the first element is not null
            for row in rows:
                # newsid,title,ctime,source
                title=row[1].strip()
                if title:
                    docs[Doc(row[0],row[2],row[3])]=delpunc(' '.join(jieba.cut(title)).lower()).split()
    return docs
                    
if __name__=='__main__':
    docs=get_records_dayago(20)
#     docs=get_records_newadded()
    if docs:
        for doc,title in docs.iteritems():
            print doc.uid,doc.source,doc.ctime,' '.join(title)
    print len(docs)
        