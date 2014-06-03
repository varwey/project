#!/usr/bin/python
#coding:utf-8

import MySQLdb
import time
from datetime import datetime

#连接数据库，获取一分钟，一小时，12小时，24小时扫描进度
scan_data=()
while 1:
    conn = MySQLdb.connect(host='111.73.45.118',user='root',passwd='130809',db='proxy')
    cur  = conn.cursor()
    scan_count = cur.execute('select status,count(*) from hunter_list2 group by status')
    sc   = cur.fetchmany(3)
    cur.close()
    conn.close()
    now = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    print now
    if len(sc) == 3:
        scan_data=(now,int(sc[0][1]),int(sc[1][1]),int(sc[2][1]))
    elif len(sc) == 2:
        if sc[0][0] == 1:
            scan_data=(now,0,int(sc[0][1]),int(sc[1][1]))
        elif sc[0][0] == 0 and sc[1][0] == 2:
            scan_data=(now,int(sc[0][1]),0,int(sc[1][1]))
        else:
            scan_data=(now,int(sc[0][1]),int(sc[1][1]),0)
    elif len(sc) == 1:
        if sc[0][0] == 2:
            scan_data=(now,0,0,int(sc[0][1]))
        elif sc[0][0] == 0:
            scan_data=(now,int(sc[0][1],0,0))
        else:
            scan_data=(0,int(sc[0][1]),0)
    else:
        scan_data=(0,0,0)
          
    conn = MySQLdb.connect(host="localhost",user="root",passwd="",db="webot")
    cur  = conn.cursor()
    insert = cur.execute('insert into blog_scan_progress(scan_date,scan_status_0,scan_status_1,scan_status_2) values(%s,%s,%s,%s)',scan_data)
    conn.commit()
    cur.close()
    conn.close()
    print "data insert already!"
    break
    
    if len(scan_data) > 24:
        scan_data.remove(scan_data[-1])

    time.sleep(3600)

