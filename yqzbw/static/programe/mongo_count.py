#!/usr/bin/python
#coding:utf-8

"""
将3.39mongo数据总量保存到文本
2014/02/21 www
"""

import pymongo
import time
import json

conn = pymongo.Connection('192.168.3.39',27019)
db = conn.spider
def total():
    total = json.dumps({'total':db.item.count()})
    fl = file('./total.txt','w')
    wt = fl.write(total)
    fl.close()

def main():
    while 1:
        total()
        time.sleep(2)

if __name__ == "__main__":
    main()


