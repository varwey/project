#!/usr/bin/ evn python
#coding:utf-8

"""
获取redis数据库五分钟之前至六分钟之前的数据存入本机
2013/10/31 www
"""

import redis,MySQLdb
from datetime import datetime

r = redis.Redis(host='192.168.94.10',port=6379,db=0)
mins = r.time()[0] - 360
maxs = mins + 60
keys = r.zrangebyscore('urlset2',mins,'(%s'%maxs)
dicts = {}
for i in keys:
    ls = r.hgetall(i)
    if ls['flag'] == '1':
        dms = ls['url'].split('/')[2].split('.')
        if dms[-1] == 'cn' and dms[0] not in ['www','blog','bbs','mblog','news']:
            dm = '.'.join(dms[-3:])
        elif dms[0] in ['www','blog','bbs','mblog','news']:
            dm = '.'.join(dms[1:])
        else :
            dm = '.'.join(dms)
        if dicts.get(dm) > 0:
            dicts[dm]+=1
        else:
            dicts[dm]=1

print datetime.now(),'dicts is ok!'
lists = [(i,dicts[i],mins) for i in dicts]
conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='webot')
cur = conn.cursor()
s = cur.executemany('insert into blog_redis_count(domain,count,time) values(%s,%s,%s)',lists)
conn.commit()
cur.close()
conn.close()
print 'insert into %s rows is ok!'%(len(lists))
