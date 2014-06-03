#/usr/bin/python
#coding:utf-8

"""
查询mongo持久库数据，进行展示
2013/11/14 www
"""

import pymongo
import re,time
from datetime import datetime
from bson.objectid import ObjectId

conn = pymongo.Connection('192.168.85.7',27019)
db   = conn.spider

def search(value,sk=0):
    sk = int(sk)*10
    count = db.item.find(value).count() 
    result= db.item.find(value).skip(sk).limit(10)
    res=[]
    for i in result:
        i['_id']=str(i['_id'])
        i['ctime']=times(i['ctime'])
        i['gtime']=times(i['gtime'])
        res.append(i)
    return (res,count)

def times(t):
    t = t.replace(microsecond=0)
    return time.mktime(time.strptime(str(t),'%Y-%m-%d %H:%M:%S'))
    
def tail(_id):
    res=[]
    value = {'_id':ObjectId(_id)}
    for i in db.item.find(value):
        res.append(i)
    if res == []:
        print 111
        for i in db.item_old.find(value):
            res.append(i)
    return res    

def total():
    return db.item.count()

if __name__ == "__main__":
    print 111111
   # val =re.escape('腾讯微博') 
   # print search({'siteName':'腾讯微博'}) 
    print tail('52df359f2704316736e01fca')
