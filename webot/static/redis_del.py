#!/usr/bin/evn python
#coding:utf-8

"""
删除blog_redis_count过时数据
2014/02/12 www
"""

import MySQLdb
import time
from datetime import datetime,timedelta

#获取要删除的日期时间戳
time_del = int(time.mktime(datetime.now().date().timetuple()))
date_del = str(datetime.now().date() - timedelta(days=1))

#连接mysql删除data
conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='webot')
cur  = conn.cursor()
d    = cur.execute('delete from blog_redis_count where time<%s',(time_del,))
conn.commit()
cur.close()
conn.close()
print '%s data del is ok'%date_del
