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
import getdoc2
from database import tablemerge,tablemerge2,dbconfig
from aggregate.rmduplicate import Depository
import time
import logging
from config import merge2_rmd_file
oldtime=time.time()
depos=Depository(0.8,merge2_rmd_file)
# depos=Depository(0.8)
docs=getdoc2.get_records_dayago(20)
for doc,title in docs.iteritems():
    depos.add_doc(doc, title)     # just add doc into the repository
msg='Depository title builds,time cost: %.2f (s)' % (time.time()-oldtime,) 
print msg
logging.info(msg)

def __addDoctoTable(doc):    
    rows=tablemerge.getRecordsByNewsid(dbconfig.mergetable, doc.uid)
    if rows==-1:
        print 'tablemerge getRecordsById error'
        return
    if len(rows[0])>0:
        exrecord=list(rows[0][:1]+rows[0][2:-1])
        related=''
        exrecord+=[related,]  
        tablemerge2.InsertItem(dbconfig.mergetable2, exrecord)    
def __addDoctoRelated(exist_doc,doc):
    tablemerge2.addRelated(dbconfig.mergetable2,exist_doc.uid, doc.uid)
    
def mergeWeb():
    docs=getdoc2.get_records_newadded()
    if not docs:
        msg='tablemerge has added no news'      
        print msg
        logging.info(msg)
        return 
    count=0
    for doc,title in docs.iteritems():
        isnew,exist_doc=depos.add_doc(doc, title)
        if isnew:
            __addDoctoTable(doc)
        else:
            __addDoctoRelated(exist_doc, doc)            
            count+=1
#             print count,'duplication:'
#             print doc.uid,''.join(title)
#             print exist_doc.uid,''.join(depos.forindex[exist_doc])
    msg='tablemerge has added news (%s/%s)'%(len(docs)-count,len(docs))
    print msg
    logging.info(msg)

def garbageDepos(dayago=20):
    keeptime=time.time()-24*3600*dayago
    depos.remove_doc_before(keeptime)
    
if __name__=='__main__':    
    mergeWeb()
    garbageDepos(2)
    
