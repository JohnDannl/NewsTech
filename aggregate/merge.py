#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-6-17

@author: dannl
'''
import sys
sys.path.append('..')
sys.path.append('../common')
from common.logger import log
import getdoc
from database import table,tablemerge,dbconfig
from aggregate.rmduplicate import Depository
import time
import logging
from common import toolpit
from config import merge1_rmd_file

oldtime=time.time()
depos=Depository(0.8,merge1_rmd_file) # for debug
# depos=Depository(0.8)
docs=getdoc.get_records_dayago(dbconfig.mergetable,20)
for doc,summary in docs.iteritems():
    depos.add_doc(doc, summary)     # just add doc into the repository
msg='Depository summary builds,time cost: %.2f (s)' % (time.time()-oldtime,) 
print msg
logging.info(msg)

def __addDoctoTable(doc):
    rows=table.getRecordsById(doc.source, doc.uid)
    if rows==-1:
        print '%s getRecordsById error'%(doc.source)
        return
    if len(rows[0])>0:
        exrecord=list(rows[0])
        mtype,click='',0
        exrecord+=[mtype,click]  
        tablemerge.InsertItem(dbconfig.mergetable, exrecord)    
        
def mergeWeb(tablename):
    docs=getdoc.get_records_newadded(tablename)
    if not docs:
        msg='%s has no new news'%(tablename,)        
        print msg
        logging.info(msg)
        return 
    count=0
    for doc,summary in docs.iteritems():
        if depos.add_doc(doc, summary)[0]:
            __addDoctoTable(doc)
            count+=1
    msg='%s has added news (%s/%s)'%(tablename,count,len(docs))
    print msg
    logging.info(msg)

def garbageDepos(dayago=20):
    keeptime=time.time()-24*3600*dayago
    depos.remove_doc_before(keeptime)
    
if __name__=='__main__':
    for web in dbconfig.tableName.itervalues():
        mergeWeb(web)
    garbageDepos(2)
    
