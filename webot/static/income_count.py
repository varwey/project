
#coding:utf-8


import MySQLdb

conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='webot',charset='utf8')
cur = conn.cursor()
data_h= cur.execute("""select site,domain,sld,category,time,sum(count) from
                    blog_spider_minute_count group by
                    floor(time/3600),sld,category""")
dt_h = list(cur.fetchall())
print len(dt_h)
res_h = cur.execute('delete from blog_spider_hour_count')
income = cur.executemany("""insert into 
                 blog_spider_hour_count(site,domain,sld,category,time,count)
                 values(%s,%s,%s,%s,%s,%s)""",dt_h)
print 'ok'
conn.commit()





data_d= cur.execute("""select site,domain,sld,category,time,sum(count) from
                    blog_spider_hour_count group by
                    floor(time/86400),sld,category""")
dt_d = list(cur.fetchall())
print len(dt_d)
res_d = cur.execute('delete from blog_spider_day_count')
income = cur.executemany("""insert into
    blog_spider_day_count(site,domain,sld,category,time,count)
    values(%s,%s,%s,%s,%s,%s)""",dt_d)
print 'ok'
conn.commit()

cur.close()
conn.close()
