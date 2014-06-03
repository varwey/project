#/usr/bin/python
#coding:utf8

"""
对采集前四的网站进行预警，如果设置时间内该域名的采集数据低于固定伐值，
进行每五分钟一次的报警通知，直到设置时间内该域名的采集数据高于固定伐值
，才停止预警通知
2014/03/14 www
"""

import MySQLdb

from datetime import datetime
import time

import smail

#预警通知mail
to_mail = ['heweigang', 'lichanghong', 'wangweiwei', 'fengmanman', 'liwei', 'qiaohaibo', 'chenjuan', 'baohaijing']
#to_mail = ['wangweiwei']
to_suffix = '@yqzbw.com'

#域名列表
domain_list = ['t.qq.com','weibo.com','tieba.baidu.com','sina.com.cn']
val_list = {
    't.qq.com': 350,
    'weibo.com': 200,
    'tieba.baidu.com': 300,
    'sina.com.cn': 50,
    }

#连接数据库
conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='webot')
cur = conn.cursor()

#获取时间
now_datetime = str(datetime.now()) 
now_time = time.time()
ago_time = now_time - 1800

#查询各域名半小时内采集数,判断预警
for i in domain_list:
    count = cur.execute('select sum(count) from blog_redis_count where domain=%s and time>%s',(i,ago_time))
    co = str(cur.fetchone()[0])
    if co == 'None':
        co = 0
    print i,co
    if int(co) < val_list[i]:
        fil = file('/var/www/webot/static/warn/'+i+'.txt','r')
        history_time = float(fil.read())
        fil.close()
       # print now_time - history_time
        if int(now_time - history_time) > 1800:
            content = 'warnning: 域名 '+i+'半小时内采集 '+str(co)+'条数据，预警时间 '+now_datetime
            [smail.send_mail(addr+to_suffix,'warnning!!!',content) for addr in to_mail]
            fl = file('/var/www/webot/static/warn/'+i+'.txt','w')
            wt = fl.write(str(now_time))
            fl.close()
            print now_datetime,content

print now_datetime
