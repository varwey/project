#!/usr/bin/python
#coding:utf-8
"""
将配置文件保存到mysql数据库的脚本
2013/9/10  www
"""
import sys
import MySQLdb
import os
import json
import time
import urllib
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')

#con = file('/crontab-all.txt','r')
#total = len(con.readlines())
#con.seek(0,0)
#e = 1
#for i in xrange(total):
#    conf = con.readline().split(' ')[-1]
#    page = urllib.urlopen(conf[7:])
#    confi= page.read()
#    page.close()
#    fi = codecs.open('/confi/%s.conf'%e,'w','utf-8')
#    fi.write(confi)
#    fi.close()
#    e +=1
#con.close()
di = {1:'news',2:'bbs',3:'blog',4:'mblog'}
values = []
for root,dirs,files in os.walk('/configs'):
    for filepath in files:
        pathname = os.path.join(root,filepath)
        if str(pathname)[-4:] == 'conf': 
                fi=file(pathname,'r')
                fil = fi.read()
                try:
                    dicts = json.loads(fil)
                except ValueError,e:
                    print False,str(e),pathname 
                    continue
                fi.close()
                filename = dicts.get('site',None)
                if isinstance(filename,unicode):
                    filename = filename.encode('utf-8')
                domain = dicts.get('domains',None)
                if domain != None:
                    domain = domain[0]
                filetype = dicts['fields'].get('category',None)
                if filetype != None:
                    filetype = int(filetype['value'])
                    
                    if filetype >= 5:
                        print domain,filename,pathname
                        continue
                    cg = di[filetype]
                channel = dicts['fields'].get('channel',None) 
                if channel != None:
                    channel = channel['value']
                else :
                    channel = '未创建'
                #if isinstance(channel,unicode):
                #    channel = channel.encode('utf-8')
                value = (cg,str(domain),filename,channel,str(pathname)[1:],120,time.strftime('%Y-%m-%d %H-%M-%S'),'暂无更新','root')
                values.append(value)

conn = MySQLdb.connect(user='root',passwd="",host='localhost',charset='utf8')
conn.query("set names 'utf8'")
conn.select_db('webot')
cursor = conn.cursor()
cursor.executemany('insert into blog_config_task (category_name,domain,domain_name,channel,config_path,priority_seconds,create_datetime,update_datetime,user) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',values)
cursor.close()
conn.close()
print 'ok' 
