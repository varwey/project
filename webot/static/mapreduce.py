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
            };
            return Y+'-'+zf(m)+'-'+zf(d)+' '+zf(H)+':00:00'
        }

        function shorten(url) {
            try
                {
                site = RegExp('//([^(/|:)]+)').exec(url)[1];
                }
            catch(err)
                {
                site = 'error.com';
                }

            if(/\.(com|gov|org|edu|net)\.cn$/.test(site)) {
                dm = site.split('.').slice(-3).join('.');
            }else if (/(\d)$/.test(site)) {
                dm = site.split('.').slice(-4).join('.');
            }else {
                dm = site.split('.').slice(-2).join('.');
            }
            return dm
        }

        function fun_sld(url) {
            try
                {
                site = RegExp('//([^(/|:)]+)').exec(url)[1];
                }
            catch(err)
                {
                site = 'error.com';
                }

            if(/\.(com|gov|org|edu|net)\.cn$/.test(site)) {
                sld = site.split('.').slice(-4).join('.').replace(/^(www)\./,'');
            }else if (/(\d)$/.test(site)) {
                sld = site.split('.').slice(-4).join('.');  
            }else {
                sld = site.split('.').slice(-3).join('.').replace(/^(www)\./,'');
            }
            return sld                
        }

        function category(tp) {
            var cg = {'01':'news','02':'bbs','03':'blog','04':'mblog'};
            tp = tp+'';
            if (cg[tp.substr(0,2)]) {
                res = cg[tp.substr(0,2)];
            }else{
                res = 'error';
            }
            return res
        }

        key = {
            'domain': shorten(this.url),
            'sld': fun_sld(this.url),
            'time': format(this.gtime),
            'category': category(this.info_flag),
        };

        val = {'sum':1,'site':this.siteName};
        emit(key, val);
    }
    """)

#reduce函数
r = Code("""
    function(key,values) {
        var sum=0;
        sld=new Object();
        values.forEach(function(x) {
            sum += x.sum;
            site = x.site.replace(/-.*/g,'')
        });
        return {'sum':sum,'site':site}
    }
    """)
def retime(dt):
    return time.mktime(time.strptime(str(dt),'%Y-%m-%d %H:%M:%S'))   

conn = pymongo.Connection('192.168.85.7',27019)
db = conn.spider
print datetime.now(),'start!'
now = datetime.utcnow().replace(hour=16,minute=0,second=0,microsecond=0)
now = now - timedelta(days=1)
ago = now - timedelta(days=1)
con = MySQLdb.connect(host='localhost',user='root',passwd='',db='webot',charset='utf8')
con.query("set names 'utf8'")
cur = con.cursor()
#入库
result = db.item.map_reduce(m,r,'myresult',query={'gtime':{'$gte':ago,'$lt':now}})

sql = 'insert into blog_spider_minute_count(site,domain,sld,category,time,count) values(%s,%s,%s,%s,%s,%s)'
for d in result.find():
    value = (d['value']['site'],d['_id']['domain'],d['_id']['sld'],d['_id']['category'],retime(d['_id']['time']),d['value']['sum'])
    s = cur.execute(sql,value)
con.commit()
print datetime.now(),"blog already!"

times = int(retime(ago))
data_h= cur.execute("""select site,domain,sld,category,time,sum(count) from
                    blog_spider_minute_count where
                    time>=%s group by
                    floor(time/3600),sld,category""",(times))
dt_h = list(cur.fetchall())
print len(dt_h)
income = cur.executemany("""insert into
                         blog_spider_hour_count(site,domain,sld,category,time,count)
                         values(%s,%s,%s,%s,%s,%s)""",dt_h)
print 'hour is ok'
con.commit()

data_d= cur.execute("""select site,domain,sld,category,time,sum(count) from
                    blog_spider_hour_count where
                    time>=%s group by
                    floor(time/86400),sld,category""",(times))
dt_d = list(cur.fetchall())
print len(dt_d)
income = cur.executemany("""insert into
                         blog_spider_day_count(site,domain,sld,category,time,count)
                         values(%s,%s,%s,%s,%s,%s)""",dt_d)

print 'day is ok'
con.commit()
cur.close()
con.close()
