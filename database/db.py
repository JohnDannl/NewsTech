#!/usr/bin/env python
#_*_ coding:utf-8 _*_

import logging
from tornpg import pgconn

########################################################################
class pgdb():

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self._dbconn = pgconn
    """初始化数据库"""

    def CreateTable(self, query, tablename):
        # Note: table name could not act as parameter
        if self.CheckExistTable(tablename):
            logging.error('Table %s already exists.'%tablename)
            return
        rows_count=self._dbconn.execute(query, ())
        #print rows_count
        if rows_count != -1:
            print 'Create table %s successfully!'% tablename
            
    def CheckExistTable(self,tablename): 
        query='''select exists(select 1 from information_schema.tables where table_catalog= %s 
        and table_schema= 'public' and table_name= %s)'''  
        rows=self._dbconn.query(query, (self._dbconn.database,tablename)) 
        return rows[0][0] 
    
    def CreateIndex(self,query):
        # Creating multiple field index differs from creating multiple indexes on different fields.
        flag=self._dbconn.execute(query, ())
        return flag
    
    def ReIndex(self,tablename):
        query='reindex table %s'%tablename
        flag=self._dbconn.execute(query,())
        return flag
    
    def Insert(self, query, data):
        flag = self._dbconn.execute(query, data)
        return flag

    def Update(self, query, data):
        flag = self._dbconn.execute(query, data)
        return flag

    def Select(self, query, data):
        rows = self._dbconn.query(query, data)
        return rows
    
    def insertMany(self,query,datas):
        flag=self._dbconn.executemany(query, datas)
        return flag

if __name__ == "__main__":
    mydb = pgdb()
#     print pgdb().ReIndex('w163')
    print mydb.CheckExistTable('sina')
#     print mydb.CreateTable("create table a (name text,age int,loadtime timestamp)", 'a')
#     print mydb.Select("select * from a where name = %s AND age = %s", ('lily',20))
#     print mydb.Update('delete from a where name=%s',['lily'])
#     print mydb.Insert('insert into a(name, age) values(%s, %s)', ('lily','20'))
#     print mydb.Update('update b set loadtime=%s where name =%s', ('1993-5-6','liy'))
#     print mydb.insertMany('insert into a(name,age) values(%s,%s)', [('lucy',19),('lilei',21)])
