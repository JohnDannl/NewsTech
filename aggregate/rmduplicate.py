#!/usr/bin/env python
#-*- coding:utf-8 -*-
'''
Created on 2015-6-14

@author: dannl
'''
import logging
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from config import stop_file
from database import dbconfig,tablemerge
from collections import Counter
import getdoc
import time

oldtime=time.time()
# docs=getdoc.get_records_dayago(dbconfig.tableName['sohu'])
# for doc,summary in docs.iteritems():
#     print doc.uid,doc.source,doc.ctime,''.join(summary)

########### remove stop words
# def remove_stop_words(sdocs):
#     # remove common words and tokenize
#     stopwords=open(stop_file,'r')
#     stoplist = set(word.strip().decode('utf-8') for word in stopwords) # set is much faster than list
#     stopwords.close()
#     for doc,words in sdocs.iteritems():
#         newwords=[word for word in words if word not in stoplist]
#         sdocs[doc]=newwords
#     return sdocs
# rdocs=remove_stop_words(docs)
# for doc,summary in rdocs.iteritems():
#     print doc.uid,doc.source,doc.ctime,''.join(summary)   
 
########### remove words that appear only once
# all_tokens = sum(texts, [])
# tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
# texts = [[word for word in text if word not in tokens_once]
#          for text in texts]

class Depository(object):
    ''' usage example:
            depos=Depository(0.8) # 0.8 is a similarity threshold
            docs=getdoc.get_records_dayago(30) 
            for doc_id,summary in docs.iteritems(): # summary should be a word list
                depos.add_doc(doc_id,summary)
            new_docs=getdoc.get_new_records(web)
            for doc_id,summary in new_docs.iteritems():
                isnew,exist_doc =depos.add_doc(doc_id,summary)
                if isnew:
                    tablemerge.insert(records(doc_id))
            #after 24 hours ...
            ctime=time.time()-24*3600
            depos.remove_doc_before(ctime)
    '''
    def __init__(self,dup_thres=0.8,rmd_file=None):
        self.forindex={}
        self.invindex={}
        self.dup_thres=dup_thres
        if rmd_file:
            self.fout=open(rmd_file,'w')
        else:
            self.fout=None
        self.count=0
    def __add_doc(self,doc,summary):
        # add doc to forward index
        self.forindex[doc]=summary
        # add doc to inverse index
        for word in summary:            
            if word in self.invindex:
                self.invindex[word].add(doc)
            else:
                self.invindex[word]=set([doc,])
    def add_doc(self,doc,summary):
        simdocs=[]
        setsum=set(summary)
        for word in setsum:        
            if word in self.invindex:
                simdocs+=self.invindex[word]
        cnt=Counter(simdocs)
        maxsim=cnt.most_common(1)        
        #print maxsim
        if maxsim:  # maxsim maybe empty []
            len_sum=len(summary)
            len_sim=len(self.forindex[maxsim[0][0]])
            len_min,len_max=len_sum,len_sim
            if len_sum>len_sim:
                len_min,len_max=len_sim,len_sum
        if maxsim and (maxsim[0][1]>=self.dup_thres*len(setsum) or \
                       maxsim[0][1]>=self.dup_thres*len(set(self.forindex[maxsim[0][0]]))) and \
                       (len_max-len_min)<0.2*len_min:
            ##################### print duplicated result
            if self.fout:
                maxdoc,maxnum=maxsim[0]            
                self.count+=1
                msg='%s:%s duplicates with %s:%s-->%s/(%s,%s)'%(doc.source,doc.uid,maxdoc.source,maxdoc.uid,
                                                                 maxnum,len(setsum),len(set(self.forindex[maxdoc])))
                msg1='%s %s'%(self.count,msg)
                msg2='%s %s'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(doc.ctime)),' '.join(summary))
                msg3='%s %s'%(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(maxdoc.ctime)),' '.join(self.forindex[maxdoc]))
                print msg1
                print msg2
                print msg3
                self.fout.write(msg1.encode('utf-8')+'\n')
                self.fout.write(msg2.encode('utf-8')+'\n')
                self.fout.write(msg3.encode('utf-8')+'\n')
            ####################### print duplicated result
            return False,maxsim[0][0]
        else:
            self.__add_doc(doc, summary)
            return True,None
    def __remove_doc(self,doc):
        # remove from the inverse index
        if doc in self.forindex:
            _summary=self.forindex[doc]
            for word in _summary:
                if word in self.invindex and doc in self.invindex[word]:
                    self.invindex[word].remove(doc) 
            # remove from the forward index
            self.forindex.pop(doc)
    def remove_doc_before(self,ctime):
        rms=[]
        for doc in self.forindex:
            if doc.ctime<ctime:
                rms.append(doc)
        for doc in rms:
            self.__remove_doc(doc)
        msg='remove:%s,left:%s'%(len(rms),len(self.forindex))
        print msg
        logging.info(msg)        
    
if __name__=='__main__':        
    depos=Depository(0.8)
    for tablename in dbconfig.tableName.itervalues():
        docs=getdoc.get_records_dayago(tablename,30)
        for doc,summary in docs.iteritems():
            isnew,exist_doc=depos.add_doc(doc, summary)
            if isnew:
                pass
#                 print exist_doc.uid,exist_doc.source,'-->',doc.uid,doc.source
    print 'time costs:%.2f (s)'%(time.time()-oldtime,)

