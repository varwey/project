#!/usr/bin/python
#coding:utf-8
"""
将远程服务器上mysql数据按需求查询保存到本地mysql库
2013/10/23 www
"""
from __future__ import division
import MySQLdb
import time

now = time.strftime('%Y-%m-%d',time.localtime(time.time())) 
conn = MySQLdb.connect(host='111.73.45.118',user='root',passwd='130809',db='proxy')
cur  = conn.cursor()
scan = cur.execute("""select date(create_datetime) as a, count(*) from
                      proxy_server group by a order by a desc""")
sd   = cur.fetchall()
cur.close()
conn.close()

sql  = 'insert into blog_scan_count(date,rate,count) values(%s,%s,%s)'
dt = [(s[0],int(s[1]/30),s[1]) for s in sd]
con  = MySQLdb.connect(user='root',passwd="root",host='192.168.3.82',charset='utf8')
con.query("set names 'utf8'")
con.select_db('webot')
cursor = con.cursor()
cursor.execute('delete from blog_scan_count')
cursor.executemany(sql,dt)
con.commit()
cursor.close()
con.close()
print 'ok'
