#!/usr/bin/python
#coding:utf-8

"""
调用MySQLdb模块做查询函数
2013/10/24 www
"""

import MySQLdb

def select(cip,db,chart,order='',**kwargs):
    conn = MySQLdb.connect(host=cip,user='root',passwd='root',db=db)
    conn.query("set names 'utf8'")
    cur  = conn.cursor()
    if order:
        sql = cur.execute('select * from %s order by %s'%(chart,order))
        result = cur.fetchall()
    elif kwargs:
        key = list(kwargs)[0]
        if key == 'id':
            sql = cur.execute('select * from %s where %s=%s'%(chart,key,kwargs[key]))
        sql = cur.execute('select * from %s where %s="%s"'%(chart,key,kwargs[key]))
        result = cur.fetchone()
    else:
        sql = cur.execute('select * from %s'%(chart))
        result = cur.fetchall()
    cur.close()
    conn.close()
    return result
if __name__ == "__main__":
    print select('192.168.3.109','task','task_list','end_datetime')
