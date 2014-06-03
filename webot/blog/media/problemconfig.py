#!/usr/bin/python
#coding:utf-8
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import pymongo
from datetime import datetime
import time

conn = pymongo.Connection()
db   = conn.result
datas= db.data
time_1=[]
time_1out=[]
time_1null=[]
time_24=[]
time_24out=[]
time_48=[]
time_48null=[]
for data in datas.find():
    if 'start_time'in data:
        le=(time.time()-time.mktime(data['start_time'].timetuple()))/3600
        if int(le) < 1:
            if data['finish_reason']=='closespider_timeout':
                time_1out.append(data)
            elif 'item_scraped_count' not in data and 'item_dropped_count' not in data :
                time_1null.append(data)
            elif 'item_dropped_count' in data :
                time_1.append(data)
        elif int(le) < 24:
            if data['finish_reason']=='closespider_timeout' and 'item_dropped_count'in data:
                time_24out.append(data)
            elif 'item_dropped_count' in data:
                time_24.append(data)
        elif int(le) < 36 :
            if 'item_scraped_count' not in data and 'item_dropped_count' not in data :
                time_48null.append(data)
            elif 'item_dropped_count' in data :
                time_48.append(data)

files = file('./time_1.txt','w+')
files.write('<tr><th>丢失数</th><th>采集数</th><th>丢失率/%</th><th>完成原因</th><th>查看日志</th><th>配置文件</th></tr>')
for dt in time_1:
    if 'item_scraped_count' not in dt:
        tr_td = '<tr><td>%s</td><td>0</td><td>100</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['item_dropped_count'],dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])     
        files.write(tr_td)
    else :
        sum = eval('%s/(%s+%s)'%(int(dt['item_dropped_count']),int(dt['item_dropped_count']),int(dt['item_scraped_count'])))*100
        tr_td = '<tr><td>%s</td><td>%s</td><td>%.2f</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['item_dropped_count'],dt['item_scraped_count'],sum,dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])
        files.write(tr_td)
files.close()
files = file('./time_1out.txt','w+')
files.write('<tr><th>丢失数</th><th>采集数</th><th>丢失率/%</th><th>完成原因</th><th>查看日志</th><th>配置文件</th></tr>')
for dt in time_1out:
    if 'item_scraped_count' not in dt:
        tr_td = '<tr><td>%s</td><td>0</td><td>100</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['item_dropped_count'],dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])     
        files.write(tr_td)
    elif 'item_dropped_count' not in dt :
        #sum = eval('%s/%s+%s'%(int(dt['item_dropped_count']),int(dt['item_dropped_count']),int(dt['item_scraped_count'])))*100
        tr_td = '<tr><td>0</td><td>%s</td><td>null</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['item_scraped_count'],dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])
        files.write(tr_td)
    else :
        sum = eval('%s/(%s+%s)'%(int(dt['item_dropped_count']),int(dt['item_dropped_count']),int(dt['item_scraped_count'])))*100
        tr_td = '<tr><td>%s</td><td>%s</td><td>%.2f</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['item_dropped_count'],dt['item_scraped_count'],sum,dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])
        files.write(tr_td)
files.close()
files = file('./time_1null.txt','w+')
files.write('<tr><th>丢失数</th><th>采集数</th><th>丢失率/%</th><th>完成原因</th><th>查看日志</th><th>配置文件</th></tr>')
for dt in time_1null:
        tr_td = '<tr><td>0</td><td>0</td><td>null</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])     
        files.write(tr_td)
files.close()
files = file('./time_24.txt','w+')
files.write('<tr><th>丢失数</th><th>采集数</th><th>丢失率/%</th><th>完成原因</th><th>查看日志</th><th>配置文件</th></tr>')
for dt in time_24:
    if 'item_scraped_count' not in dt:
        tr_td = '<tr><td>%s</td><td>0</td><td>100</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['item_dropped_count'],dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])     
        files.write(tr_td)
    else :
        sum = eval('%s/(%s+%s)'%(int(dt['item_dropped_count']),int(dt['item_dropped_count']),int(dt['item_scraped_count'])))*100
        tr_td = '<tr><td>%s</td><td>%s</td><td>%.2f</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['item_dropped_count'],dt['item_scraped_count'],sum,dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])
        files.write(tr_td)
files.close()
files = file('./time_24out.txt','w+')
files.write('<tr><th>丢失数</th><th>采集数</th><th>丢失率/%</th><th>完成原因</th><th>查看日志</th><th>配置文件</th></tr>')
for dt in time_24out:
    if 'item_scraped_count' not in dt:
        tr_td = '<tr><td>%s</td><td>0</td><td>100</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['item_dropped_count'],dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])     
        files.write(tr_td)
    elif 'item_dropped_count' not in dt :
        #sum = eval('%s/%s+%s'%(int(dt['item_dropped_count']),int(dt['item_dropped_count']),int(dt['item_scraped_count'])))*100
        tr_td = '<tr><td>0</td><td>%s</td><td>null</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['item_scraped_count'],dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])
        files.write(tr_td)
    else :
        sum = eval('%s/(%s+%s)'%(int(dt['item_dropped_count']),int(dt['item_dropped_count']),int(dt['item_scraped_count'])))*100
        tr_td = '<tr><td>%s</td><td>%s</td><td>%.2f</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['item_dropped_count'],dt['item_scraped_count'],sum,dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])
        files.write(tr_td)
files.close()
files = file('./time_48.txt','w+')
files.write('<tr><th>丢失数</th><th>采集数</th><th>丢失率/%</th><th>完成原因</th><th>查看日志</th><th>配置文件</th></tr>')
for dt in time_48:
    if 'item_scraped_count' not in dt:
        tr_td = '<tr><td>%s</td><td>0</td><td>100</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['item_dropped_count'],dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])     
        files.write(tr_td)
    else :
        sum = eval('%s/(%s+%s)'%(int(dt['item_dropped_count']),int(dt['item_dropped_count']),int(dt['item_scraped_count'])))*100
        if int(sum)>50 :
            tr_td = '<tr><td>%s</td><td>%s</td><td>%.2f</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['item_dropped_count'],dt['item_scraped_count'],sum,dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])
        files.write(tr_td)
files.close()
files = file('./time_48null.txt','w+')
files.write('<tr><th>丢失数</th><th>采集数</th><th>丢失率/%</th><th>完成原因</th><th>查看日志</th><th>配置文件</th></tr>')
for dt in time_48null:
        tr_td = '<tr><td>0</td><td>0</td><td>null</td><td>%s</td><td><a href=http://%s:6800/logs/%s/%s/%s.log>%s</a></td><td><a href=http://%s>%s</a></td></tr>\n'%(dt['finish_reason'],dt['bot_ip'],dt['spider_name'],dt['bot_name'],dt['job_id'],dt['bot_ip'],dt['config_path'],dt['config_path'])     
        files.write(tr_td)
files.close()
conn.close()

