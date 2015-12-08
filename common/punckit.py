#!/usr/bin/env python
#-*-coding:utf-8 -*-
'''
Created on 2014-12-27

@author: JohnDannl
'''
import re, string, timeit

##################### Speed test #####################
s = "string. With. Punctuation"
exclude = set(string.punctuation)
table = string.maketrans("","")
regex = re.compile('[%s]' % re.escape(string.punctuation))

def test_set(s):
    return ''.join(ch for ch in s if ch not in exclude)

def test_re(s):  # From Vinko's solution, with fix.
    return regex.sub('', s)

def test_trans(s):
    return s.translate(table, string.punctuation)

def test_repl(s):  # From S.Lott's solution
    for c in string.punctuation:
        s=s.replace(c,"")
    return s

# print "sets      :",timeit.Timer('f(s)', 'from __main__ import s,test_set as f').timeit(1000000)
# print "regex     :",timeit.Timer('f(s)', 'from __main__ import s,test_re as f').timeit(1000000)
# print "translate :",timeit.Timer('f(s)', 'from __main__ import s,test_trans as f').timeit(1000000)
# print "replace   :",timeit.Timer('f(s)', 'from __main__ import s,test_repl as f').timeit(1000000)
# print timeit.timeit('1+1', number=10000)
##################### Speed test #####################
def strF2H(ustring):
    """把字符串全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code==0x3000:
            inside_code=0x0020
        else:
            inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
            rstring += uchar
        rstring += unichr(inside_code)
    return rstring

def strH2F(ustring):
    """把字符串半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)       
        if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
            rstring += uchar
            continue
        if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
            inside_code=0x3000
        else:
            inside_code+=0xfee0
        rstring += unichr(inside_code)
    return rstring

def getord(ustring):
    '''Return the integer ordinal of a one-character string'''
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)  
        rstring += r'\U%s'%inside_code
    return rstring

# string.pun :!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
# half cn pun:！“”#￥%&‘’（）*+，-。、：：《=》？@【、】……——·『|』~
half_en=string.punctuation
full_en=strH2F(half_en)
half_cn='''！“”#￥%&‘’（）*+，-。、：；《=》？@【、】……——·『|』~'''.decode('utf-8')
# full_cn='''！“”＃￥％＆‘’（）＊，－。、：；《＝》？＠【、】……——·『｜』～'''.decode('utf-8')
full_cn=strH2F(half_cn)
pattern_full=re.compile('[%s]' % full_en)
pattern_half=re.compile('[%s]' % re.escape(half_cn))
def _merge(*ustrList):
    ''' Return the merged list of lists'''
    charList=[]
    for ustr in ustrList:
        charList.extend([uchar for uchar in ustr])
    return ''.join(set(charList))

all_punc=_merge(half_en,half_cn,full_en,full_cn)
pattern_all=re.compile('[%s]' % re.escape(all_punc))
def delpunc(s):
    '''
    Receive utf-8 or unicode
    Return unicode
    Delete all punctuation including en or cn in both of full or half mode
    '''    
    sutf8=s.decode('utf-8') if not isinstance(s, unicode) else s
#     sutf8=s
    return pattern_all.sub('',sutf8)

#     list1=[uchar for uchar in ustr1]
#     list2=[uchar for uchar in ustr2]
#     print len(list1)
#     list1.extend(list2)
#     print len(list1)
#     print len(list2)
#     print len(set(list1))
    
if __name__=='__main__':
#     print 'half_en:',half_en
#     print 'full_en:',full_en
#     print 'half_cn:',half_cn
#     print 'full_cn:',full_cn
#     print len(_merge(half_en,half_cn,full_en,full_cn))
#     print _merge(half_en,half_cn,full_en,full_cn)
#     print test_trans(s)
    s='中文标点:：，。！？，还有“”……。【】「 “”'.decode('utf-8')
#     print test_trans(s)
#     print string.punctuation
#     print re.escape(string.punctuation)
    print pattern_half.sub('',s)
    print pattern_full.sub('',s)
    print 'half:',pattern_half.sub('',s)
    print 'all:',delpunc(s)
    print getord('『「'.decode('utf-8'))
    