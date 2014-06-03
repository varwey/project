#!/usr/bin/python
#coding:utf-8
#将采集数据情况进行分类统计
#2013/12/3 by www

from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import pymongo
from datetime import datetime,timedelta
import time
import json
from operator import itemgetter, attrgetter

conn = pymongo.Connection('192.168.85.1',27019)
print conn
db   = conn.result
datas= db.data
time_1     = []
time_1out  = []
time_1null = []
time_24    = []
time_24out = []
time_48    = []
time_48null= []
now = datetime.utcnow()
ago = now - timedelta(days=3)
for data in datas.find({'start_time':{'$gt':ago,'$lt':now},'finish_time':{'$gt':ago,'$lt':now}}):
    if 'start_time'in data and 'finish_time' in data:
        if 'item_dropped_count' not in data:
            rate = 0
        elif 'item_scraped_count' not in data:
            rate = 100
        else:
            rate = eval('%s/(%s+%s)'%(int(data.get('item_dropped_count',1)),
                                      int(data.get('item_dropped_count',1)),
                                      int(data.get('item_scraped_count',0))))*100
        
        le   = (time.mktime(now.timetuple())-time.mktime(data['start_time'].timetuple()))/3600
        if le < 1:
            if data['finish_reason']=='closespider_timeout':
                drop =data.get('item_dropped_count',0)
                scrap=data.get('item_scraped_count',0)
                
                dat={'drop':drop,
                     'scrap':scrap,
                     'rate':rate,
                     'reason':data['finish_reason'],
                     'bot_ip':data['bot_ip'],
                     'spider_name':data['spider_name'],
                     'bot_name':data['bot_name'],
                     'job_id':data['job_id'],
                     'config_path':data['config_path']}
                time_1out.append(dat)
            elif 'item_scraped_count' not in data and 'item_dropped_count' not in data :
                time_1null.append({'drop':data.get('item_dropped_count',0),
                                   'scrap':data.get('item_scraped_count',0),
                                   'rate':rate,'reason':data['finish_reason'],
                                   'bot_ip':data['bot_ip'],
                                   'spider_name':data['spider_name'],
                                   'bot_name':data['bot_name'],
                                   'job_id':data['job_id'],
                                   'config_path':data['config_path']})
            elif 'item_dropped_count' in data :
                time_1.append({'drop':data.get('item_dropped_count',0),
                               'scrap':data.get('item_scraped_count',0),
                               'rate':rate,'reason':data['finish_reason'],
                               'bot_ip':data['bot_ip'],
                               'spider_name':data['spider_name'],
                               'bot_name':data['bot_name'],
                               'job_id':data['job_id'],
                               'config_path':data['config_path']})
        elif le < 24:
            if data['finish_reason']=='closespider_timeout':
                time_24out.append({'drop':data.get('item_dropped_count',0),
                                   'scrap':data.get('item_scraped_count',0),
                                   'rate':rate,'reason':data['finish_reason'],
                                   'bot_ip':data['bot_ip'],
                                   'spider_name':data['spider_name'],
                                   'bot_name':data['bot_name'],
                                   'job_id':data['job_id'],
                                   'config_path':data['config_path']})
            else:
                time_24.append({'drop':data.get('item_dropped_count',0),
                                'scrap':data.get('item_scraped_count',0),
                                'rate':rate,'reason':data['finish_reason'],
                                'bot_ip':data['bot_ip'],
                                'spider_name':data['spider_name'],
                                'bot_name':data['bot_name'],
                                'job_id':data['job_id'],
                                'config_path':data['config_path']})
        elif le < 48 :
            if 'item_scraped_count' not in data and 'item_dropped_count' not in data:
                time_48null.append({'drop':data.get('item_dropped_count',0),
                                    'scrap':data.get('item_scraped_count',0),
                                    'rate':rate,'reason':data['finish_reason'],
                                    'bot_ip':data['bot_ip'],
                                    'spider_name':data['spider_name'],
                                    'bot_name':data['bot_name'],
                                    'job_id':data['job_id'],
                                    'config_path':data['config_path']})
            else:
                time_48.append({'drop':data.get('item_dropped_count',0),
                                                'scrap':data.get('item_scraped_count',0),
                                                'rate':rate,'reason':data['finish_reason'],
                                                'bot_ip':data['bot_ip'],
                                                'spider_name':data['spider_name'],
                                                'bot_name':data['bot_name'],
                                                'job_id':data['job_id'],
                                                'config_path':data['config_path']})

files = file('./time_1.json','w')
files.write(json.dumps(sorted(time_1[0:10000], key=itemgetter('rate'),reverse=True)))
files.close()

files = file('./time_1out.json','w')
files.write(json.dumps(sorted(time_1out[0:10000], key=itemgetter('rate'),reverse=True)))
files.close()

files = file('./time_1null.json','w')
files.write(json.dumps(sorted(time_1null[0:10000], key=itemgetter('rate'),reverse=True)))
files.close()

files = file('./time_24.json','w')
files.write(json.dumps(sorted(time_24[0:10000], key=itemgetter('rate'),reverse=True)))
files.close()

files = file('./time_24out.json','w')
files.write(json.dumps(sorted(time_24out[0:10000], key=itemgetter('rate'),reverse=True)))
files.close()

files = file('./time_48.json','w')
files.write(json.dumps(sorted(time_48[0:10000], key=itemgetter('rate'),reverse=True)))
files.close()

files = file('./time_48null.json','w')
files.write(json.dumps(sorted(time_48null[0:10000], key=itemgetter('rate'),reverse=True)))
files.close()

print "finished: %s"%datetime.now()
