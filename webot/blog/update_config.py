#!/usr/bin/python
#coding:utf-8
"""
将前台修改的配置文件中部分展示数据修改保存至mysql
2013/10/18    王威威  
"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb
from datetime import datetime
import json

di = {1:'news',2:'bbs',3:'blog',4:'mblog'}
def uc(num,fp,config_file):
    dicts = json.loads(config_file)
    domain_name = dicts.get('site',None)
    if isinstance(domain_name,unicode):
        domain_name = domain_name.encode('utf-8')
    domain = dicts.get('domains',None)
    if domain != None:
        domain = domain[0]
    category = dicts['fields'].get('category',None)
    if category != None:
        if category >= 5:
            category_name = 'unknow'
        category_name = di[int(category['value'])]
         
    channel = dicts['fields'].get('channel',None)
    if channel != None:
        channel = channel['value']
    else :
        channel = '未创建'
    if isinstance(channel,unicode):
        channel = channel.encode('utf-8')
    if 'priority_seconds' not in dicts:
        sql  = """
               update blog_config_task set category_name=%s,
                                           domain=%s,
                                           domain_name=%s,
                                           channel=%s,
                                           update_datetime=%s
                                           where id=%s 
               """
        values = (category_name,str(domain),domain_name,channel,datetime.now(),int(num))
    else:
        sql  = """
               update blog_config_task set category_name=%s,
                                           domain=%s,
                                           domain_name=%s,
                                           channel=%s,
                                           priority_seconds=%s,
                                           update_datetime=%s
                                           where id=%s 
               """
        values = (category_name,str(domain),domain_name,channel,dicts['priority_seconds'],datetime.now(),int(num))
    conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='webot',charset='utf8')
    conn.query("set names 'utf8'")
    cur = conn.cursor()
    ud = cur.execute(sql,values)
    cur.close()
    conn.close()

    fil = file(fp,'w')
    wf  = fil.write(config_file)
    fil.close()

#if __name__ == '__main__':
#    uc(1,'/var/www/webot/blog/media/configss/news/other_news/fdw_163news_news.conf','')
