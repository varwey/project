#!/usr/bin/python
#coding:utf-8

"""
将其他服务器上mysql导库数据统计保存本地mysql
2013/11/07 www
"""

import MySQLdb
import time
import smail
from datetime import datetime

to_mail = ['heweigang@yqzbw.com','lanyu@yqzbw.com','910317157@qq.com','chenjuan@yqzbw.com']
#to_mail = ['910317157@qq.com']

monitors = [['192.168.200.30','news',15000],
            ['192.168.200.145','bbs',10000],
            ['192.168.200.212','blog',10000],
            ['192.168.200.202','weibo',25000],
            ['192.168.200.49','weibo',30000]]

sql = 'select count(*) from '
now = time.time()
date_time = datetime.now()
values = [now,]
for i in monitors:
    try:
        conn = MySQLdb.connect(host=i[0],user='root',passwd='root',port=3306,db='spider')
        cur = conn.cursor()
        cu = cur.execute(sql+i[1])
        dt = cur.fetchone()
        values.append(dt[0])
        cur.close()
        conn.close()
    except:
        values.append(100000)
    num = int(dt[0])
    #导库报警代码
    if num >= i[2]:
        fil = file('/var/www/webot/static/warn/warn.txt','r')
        tim = float(fil.read())
        fil.close()
        if (int(tim) + 300) < int(now):
            fil = file('/var/www/webot/static/warn/warn.txt','w')
            wri = fil.write(str(now))
            fil.close()
            comment = 'warn: 库ip: %s,类型：%s,时间：%s,导库数量:%s,表现为拥堵！'%(i[0],i[1],date_time,dt[0])
            [smail.send_mail(addr,'warnning!!!',comment) for addr in to_mail]           
            print comment
value = tuple(values)    
con  = MySQLdb.connect(host='localhost',user='root',passwd='',port=3306,db='webot')
curs = con.cursor()
de   = curs.execute('delete from blog_storage_monitor where time<%s',(now-48*3600))
imp  = curs.execute('insert into blog_storage_monitor(time,news,bbs,blog,mblog,mblogs) values(%s,%s,%s,%s,%s,%s)',value)
con.commit()
curs.close()
con.close()

