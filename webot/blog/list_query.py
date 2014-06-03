#!/usr/bin/python
#coding:utf-8
"""
将mongo数据筛选后展现
2013/10/23 www
"""
#连接mongo筛选数据

from datetime import datetime,timedelta
import pymongo,MySQLdb
import re,calendar,json



def unixtime(dt):
    return int(calendar.timegm(dt.timetuple())*1000)

def l_q(conf):    
    ago  = datetime.utcnow() - timedelta(days=1)
    now  = datetime.utcnow()
    conn = pymongo.Connection(host='192.168.85.1',port=27019)
    tbl  = conn.result.data
    cur  = tbl.find({'config_path':{'$regex':re.compile(conf)},
                     'start_time':{'$gt':ago,'$lt':now},
                     'finish_time':{'$gt':ago,'$lt':now}
                    }).sort('config_path')
    conn.close()
    
    result = [{'config':dt['config_path'],
               'scraped':dt.get('item_scraped_count',0),
               'dropped':dt.get('item_dropped_count',0),
               'duplicated':dt.get('item_duplicated_count',0),
               'start':unixtime(dt['start_time']),
               'finish':unixtime(dt['finish_time']),
               'reason':dt['finish_reason']
              } for dt in cur]
    msg = json.dumps({'size':len(result),'code':0,'message':'ok','result':result,'time':unixtime(datetime.utcnow())})
    return msg

if __name__ == "__main__":
    print l_q('mop')
