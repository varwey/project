#!/usr/bin/ env python
#coding:utf-8

import pymongo,MySQLdb
from bson.code import Code
import json
from datetime import datetime,timedelta
import time
no = time.time()

#map函数
m = Code("""
    function() {
        function format(dt) {
            Y = dt.getFullYear();
            m = (dt.getMonth()+1);
            d = dt.getDate();
            H = dt.getHours();
            M = dt.getMinutes();
            var zf = function(x) {
                x = x.toString();
                return x[1]?x:'0'+x
            }
            return Y+'-'+zf(m)+'-'+zf(d)+' '00:00:00'
        }


        key = {
            'time': format(this.gtime),
        };

        val = {'sum':1};
        emit(key, val);
    }
    """)

#reduce函数
r = Code("""
    function(key,values) {
        var sum=0;
        values.forEach(function(x) {
            sum += x.sum;
        });
        return {'sum':sum}
    }
    """)
def retime(dt):
    return time.mktime(time.strptime(str(dt),'%Y-%m-%d %H:%M:%S'))   

conn = pymongo.Connection('192.168.3.39',27019)
db = conn.spider
print datetime.now(),'start!'
now = datetime.utcnow().replace(hour=16,minute=0,second=0,microsecond=0)
now = now - timedelta(days=1)
ago = now - timedelta(days=1)
result = db.item.map_reduce(m,r,'myresult',query={'gtime':{'$gte':ago,'$lt':now}})
except:
    result = db.item.map_reduce(m,r,'myresult',query={'gtime':{'$gte':ago,'$lt':now}})
a=''
for d in result.find():
    a+=(str(d['_id']['time']),d['value']['sum'])
fi = open('/res.csv','w')
d=fi.write(a)
fi.close()
