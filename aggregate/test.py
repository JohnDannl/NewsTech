#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-6-26

@author: dannl
'''
import sys
sys.path.append(r'..')
sys.path.append(r'../database')
import jieba
from common.punckit import delpunc
import time
from config import merge1_title_file,merge1_summary_file,merge2_title_file,merge2_summary_file
from config import title_rep,title_rep2,merge2_title_ori
import database.tablemerge as tablemerge
from database import table,dbconfig,tablemerge2

def getFirstRmDuplicationResult(split=True):
    rows=tablemerge.getTitleSummary(dbconfig.mergetable)
    if rows !=-1:
        f_summary=open(merge1_summary_file,'w')
        with open(merge1_title_file,'w') as fout:
            count=0
            for row in rows:
                # title,summary,ctime,source
                count+=1
                mtid,title,summary,ctime=row[0],row[1].strip(),row[2].strip(),row[3]
                if split:
                    title=' '.join(jieba.cut(delpunc(title.lower()))).encode('utf-8')
                    summary=' '.join(jieba.cut(delpunc(summary.lower()))).encode('utf-8')
                timeStr=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(ctime))
                msg_t='%s %s %s %s'%(count,mtid,timeStr,title)
                msg_s='%s %s %s %s'%(count,mtid,timeStr,summary)
                print msg_t
                print msg_s
                fout.write(msg_t+'\n')                
                f_summary.write(msg_s+'\n')
        f_summary.close()
                
def getSecondRmDuplicationResult(split=True):
    rows=tablemerge2.getTitleSummary(dbconfig.mergetable2)
    if rows !=-1:
        f_summary=open(merge2_summary_file,'w')
        with open(merge2_title_file,'w') as fout:
            count=0
            for row in rows:
                # title,summary,ctime,source
                count+=1
                mtid,title,summary,ctime=row[0],row[1].strip(),row[2].strip(),row[3]
                if split:
                    title=' '.join(jieba.cut(delpunc(title.lower()))).encode('utf-8')
                    summary=' '.join(jieba.cut(delpunc(summary.lower()))).encode('utf-8')
                timeStr=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(ctime))
                msg_t='%s %s %s %s'%(count,mtid,timeStr,title)
                msg_s='%s %s %s %s'%(count,mtid,timeStr,summary)
                print msg_t
                print msg_s
                fout.write(msg_t+'\n')                
                f_summary.write(msg_s+'\n')
        f_summary.close()

def getDuplicationRate():
    count=0
    for tablename in dbconfig.tableName.itervalues():
        count+=table.getAllCount(tablename)
    mcount=tablemerge.getAllCount(dbconfig.mergetable)
    m2count=tablemerge2.getAllCount(dbconfig.mergetable2)    
    print 'First Duplication Rate: %.4f (%d/%d)'%(float(count-mcount)/count,count-mcount,count)    
    print 'Second Duplication Rate: %.4f (%d/%d)'%(float(mcount-m2count)/mcount,mcount-m2count,mcount)
    
def getRep():
    title_ori=[]
    with open(merge2_title_ori,'r') as mto:
        for line in mto:
            line=line.strip()
            if not line:
                continue
            title_ori.append(line)   
    fin=open(title_rep2,'r')    
    with open(title_rep,'w') as fout:
        for line in fin:
            print line.strip()
            line=line.split()
            new_line=title_ori[int(line[0])-1]+'\n'
            print new_line
            fout.write(new_line)
    fin.close()
if __name__=='__main__':
#     getFirstRmDuplicationResult(True)
#     getSecondRmDuplicationResult(True)
#     getSecondRmDuplicationResult(False)
#     getDuplicationRate()
    getRep()
        