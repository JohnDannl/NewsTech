#!/usr/bin/env python
#_*_ coding:utf-8 _*_
'''
Created on 2014-5-3

@author: JohnDannl
'''
# dbname = 'newstech1'
dbname = 'newstech'
user = 'postgres'

host = 'localhost'
# host = '202.38.81.25'
# host = '127.0.0.1'
# host = 'localhost'

password = 'ustcedu10'

tableName={'sina':'sina','sohu':'sohu','w163':'w163','huxiu':'huxiu','ittime':'ittime',
           'w36kr':'w36kr','leiphone':'leiphone','ifanr':'ifanr','zol':'zol','tmt':'tmt',
           'csdn':'csdn','ciweek':'ciweek','geekpark':'geekpark','donews':'donews','zhidx':'zhidx',
           'techweb':'techweb','bnet':'bnet','cnet':'cnet','techcrunch':'techcrunch','technews':'technews',
           'zdnet':'zdnet','pingwest':'pingwest','pintu360':'pintu360','hiapk':'hiapk','able2do':'able2do',
           'qq':'qq'}

mergetable='merge'
mergetable2='merge2'
requesttable='request'