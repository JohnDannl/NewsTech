#!/usr/bin/env python
#_*_ coding:utf-8 _*_

'''
Created on 2014-5-6

@author: JohnDannl
'''
def writeFileBinary(filePath, content):
    fp = open(filePath, 'wb')
    fp.write(content)
    fp.close()
def readFileBinary(filePath):
    with open(filePath,'rb') as fin:
        return fin.read()    
    
if __name__=="__main__":
    fileContent=r'�ļ�����'
    filePath=r'e:\tmp\fileTest.txt'
    writeFileBinary(filePath,fileContent)
    
    #The default coding is Ascii for text
    try:
        fin=open(filePath,'r')
        print fin.read()
    finally:
        if fin:
            fin.close()
            
    # with ... will close the opened file automationally
    with open(filePath, 'r') as fin:
        print fin.read()
    
    try:    
        fin=open(filePath,'rb')
        fContent=fin.read().decode('GBK')
        print fContent
    finally:
        fin.close()
