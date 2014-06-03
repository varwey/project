#!/usr/bin/python
#coding:utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from blog.models import Redis_Count,Storage_Monitor
from blog.models import Spider_Minute_Count,Spider_Hour_Count,Spider_Day_Count,Time_Diff,Config_Mangers,Config_Topic
import MySQLdb
import json
import time
from datetime import datetime,timedelta

def now_time():
    return time.mktime(datetime.now().date().timetuple())

def now_date(num):
    return datetime.now().date() - timedelta(days=num)
    
#配置查询表单
class Conf_Search(forms.Form):
    conf_content = forms.CharField(label='查询内容')
    conf_option = forms.CharField(label='查询选项')

#展示入库统计数据
@login_required
def income_count(req):
    user = req.user
    dm = Spider_Minute_Count.objects.values('domain')
    domain = list(set([str(i['domain']) for i in dm]))
    if len(req.GET) > 0:
        conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='webot')
        conn.query("set names 'utf8'")
        cur  = conn.cursor()
        tp = req.GET['tp']
        if tp == '3':
            dt,dm = (str(req.GET['dt']),str(req.GET['dm']))
            sql = """select category,concat(sum(count),"") from
                     blog_spider_day_count where
                     date(from_unixtime(time))=%s and domain=%s group by
                     category"""
            value = (dt,dm)
            res = cur.execute(sql,value)
            dat = cur.fetchall()
            r = cur.execute("""select sld,concat(sum(count),'') from
                               blog_spider_day_count where
                               domain=%s and date(from_unixtime(time))=%s group by
                               sld order by sum(count) desc""",(dm,dt))
            tbls = cur.fetchall()
            result = json.dumps({'result':dat,'tables':tbls})
            cur.close()
            conn.close()
            return HttpResponse(result)
        elif tp == '1':
            dt,cg,dte = (req.GET['dt'],req.GET['cg'],req.GET['dte'])
            if cg == 'all':
                sql1 = """select site,domain,concat(sum(count),'') from
                         blog_spider_day_count where date(from_unixtime(time)) between %s and %s
                         group by domain order by sum(count) desc"""
                sql2 = """select site,domain,concat(sum(count),'') from
                         blog_spider_day_count where date(from_unixtime(time)) between %s and %s
                         group by site order by sum(count) desc"""
                value = (dt,dte)
            else:
                sql1 = """select site,domain,concat(sum(count),'') from
                         blog_spider_day_count where date(from_unixtime(time)) between %s and %s and category=%s
                         group by domain order by sum(count) desc"""
                sql2 = """select site,domain,concat(sum(count),'') from
                         blog_spider_day_count where date(from_unixtime(time)) between %s and %s and category=%s
                         group by site order by sum(count) desc"""
                value = (dt,dte,cg)
            res1 = cur.execute(sql1,value)
            dat1 = cur.fetchall()
            res2 = cur.execute(sql2,value)
            dat2 = cur.fetchall()
            result = json.dumps({'result':dat1,'site':dat2,'option':'old','cg':cg})
            cur.close()
            conn.close()
            return HttpResponse(result)
        elif tp == '2':
            dm,cg,dt,dte = (req.GET['dm'],req.GET['cg'],req.GET['dt'],req.GET['dte'])
            if cg == 'all':
                sql = """select time,concat(sum(count),""),domain from blog_spider_day_count where
                         domain=%s and date(from_unixtime(time))>=%s and date(from_unixtime(time))<=%s group by
                         date(from_unixtime(time))"""
                value = (dm,dt,dte)
            else:
                sql = """select time,concat(sum(count),"") from blog_spider_day_count where
                         domain=%s and category=%s and date(from_unixtime(time))>=%s and date(from_unixtime(time))<=%s
                         group by date(from_unixtime(time))"""
                value = (dm,cg,dt,dte)
            try:
                res = cur.execute(sql,value)
                dat = cur.fetchall()
                result = json.dumps({'result':dat,'num':'all','op':cg,'cg':cg})
            except:
                result = json.dumps({})
            cur.close()
            conn.close()
            return HttpResponse(result)
        elif tp == '0':
            dm,dt,tm,cg = (req.GET['dm'],req.GET['dt'],req.GET['tm'],req.GET['cg'])
            if cg == 'all':
                value = (dm,dt)
                if tm == '0':
                    sql = """select time,concat(sum(count),"") from
                             blog_spider_minute_count where domain=%s and date(from_unixtime(time))=%s
                             group by time"""
                else:
                    sql = """select time,concat(sum(count),"") from
                             blog_spider_minute_count where domain=%s and date(from_unixtime(time))=%s
                             group by floor(time/3600)"""
            else:
                value = (dm,dt,cg)
                if tm == '0':
                    sql = """select time,count from blog_spider_minute_count where
                             domain=%s and date(from_unixtime(time))=%s and category=%s"""
                else:
                    sql = """select time,concat(sum(count),"") from
                             blog_spider_minute_count where domain=%s and date(from_unixtime(time))=%s and category=%s
                             group by floor(time/3600)"""
            try:
                res = cur.execute(sql,value)
                dat = cur.fetchall()
                result = json.dumps({'result':dat,'num':tm,'op':'0','cg':cg})
            except:
                result = json.dumps({})
            cur.close()
            conn.close()
            return HttpResponse(result)
        elif tp == '4':
            cg,dt,dte = (req.GET['cg'],req.GET['dt'],req.GET['dte'])
            if cg == 'all':
                res = cur.execute("""select time,concat(sum(count),"") from
                                     blog_spider_day_count where
                                     date(from_unixtime(time)) between %s and %s group by
                                     date(from_unixtime(time))""",(dt,dte))
            else:
                res = cur.execute("""select time,concat(sum(count),"") from
                                     blog_spider_day_count where
                                     category=%s and date(from_unixtime(time)) between %s and %s group by
                                     date(from_unixtime(time))""",(cg,dt,dte))
            dat = cur.fetchall()
            result = json.dumps({'result':dat,'num':'all','op':'0','cg':cg})
            cur.close()
            conn.close()
            return HttpResponse(result)
    return render_to_response('income_count.html',{'user':user,'domain':domain})
    
#展示入库统计数据
@login_required
def income_today(req):
    user = req.user
    if 'tp' in req.GET:
        conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='webot')
        cur  = conn.cursor()
        tp =req.GET['tp']
        if tp == '0':
            dm,dt,tm = (req.GET['dm'],req.GET['dt'],req.GET['tm'])
            value = (dm,dt)
            if tm == '0':
                sql = """select time,count from blog_redis_count where
                         domain=%s and date(from_unixtime(time))=%s"""
            else:
                sql = """select time,concat(sum(count),"") from
                         blog_redis_count where domain=%s and date(from_unixtime(time))=%s
                         group by floor((time)/3600)"""
            try:
                res = cur.execute(sql,value)
                dat = cur.fetchall()
            except:
                dat = '' 
            cur.close()
            conn.close()
            result = json.dumps({'result':dat,'num':tm,'op':'0','cg':'all'})
            return HttpResponse(result)
        else:
            dt = req.GET['dt']
            sql = """select domain,concat(sum(count),'') from
                     blog_redis_count where date(from_unixtime(time))=%s
                     group by domain order by sum(count) desc"""
            value = (dt)
            res  = cur.execute(sql,value)
            dat  = cur.fetchall()
            result = json.dumps({'result':dat,'option':'now'})
            cur.close()
            conn.close()
            return HttpResponse(result)
            
    return render_to_response('income_count.html',{'user':user})


#展示入库监控情况
@login_required
def storage_monitor(req):
    user = req.user
    now  = time.mktime(datetime.now().replace(hour=0,minute=0,second=0,microsecond=0).timetuple())
    old  = now-24*3600
    tod  = Storage_Monitor.objects.filter(time__gte=now).order_by('time')
    yes  = Storage_Monitor.objects.filter(time__gte=old,time__lt=now).order_by('time')
    dtn  = [map(int,[tod[i].time,tod[i].news,tod[i].bbs,tod[i].blog,tod[i].mblog,tod[i].mblogs]) for i in xrange(len(tod))]
    dty  = [map(int,[yes[i].time,yes[i].news,yes[i].bbs,yes[i].blog,yes[i].mblog,yes[i].mblogs]) for i in xrange(len(yes))]
    return render_to_response('storage_monitor.html',{'user':user,'dtn':dtn,'dty':dty})

#返回点击后的table
@login_required
def income_tables(req):
    user = req.user
    if len(req.GET) > 0:
        conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='webot')
        conn.query("set names 'utf8'")
        cur  = conn.cursor()
        dt,dm,cg,tm = (req.GET['dt'],req.GET['dm'],req.GET['cg'],req.GET['tm'])
        if cg == 'all':
            if tm == '0':
                sql = """select sld,count from
                         blog_spider_minute_count where
                         domain=%s and time=%s group by
                         sld order by count desc"""
                value = (dm,dt)
            elif tm == '1':
                dt = int(int(dt)/3600)
                sql = """select sld,concat(sum(count),'') from
                         blog_spider_minute_count where
                         domain=%s and floor(time/3600)=%s group by
                         sld order by sum(count) desc"""
                value = (dm,dt)
            else:
                sql = """select sld,concat(sum(count),'') from
                         blog_spider_minute_count where
                         domain=%s and date(from_unixtime(time))=%s group by
                         sld order by sum(count) desc"""
                value = (dm,dt)
        else:
            if tm == '0':
                sql = """select sld,count from
                         blog_spider_minute_count where
                         domain=%s and time=%s and category=%s group by
                         sld order by count desc"""
                value = (dm,dt,cg)
            elif tm == '1':
                dt = int(int(dt)/3600)
                sql = """select sld,concat(sum(count),'') from
                         blog_spider_minute_count where
                         domain=%s and floor(time/3600)=%s and category=%s group by
                         sld order by sum(count) desc"""
                value = (dm,dt,cg)
            else:
                sql = """select sld,concat(sum(count),'') from
                         blog_spider_minute_count where
                         domain=%s and date(from_unixtime(time))=%s and category=%s group by
                         sld order by sum(count) desc"""
                value = (dm,dt,cg)
        res = cur.execute(sql,value)
        dat = cur.fetchall()
        result = json.dumps({'result':dat})
        cur.close()
        conn.close()
        return HttpResponse(result)
    return render_to_response('income_count.html',{'user':user})

#采集监控排名
@login_required
def income_ranking(req):
    user = req.user
    dm   = Redis_Count.objects.values('domain')
    domain = list(set([str(i['domain']) for i in dm]))
    if 'dm' in req.GET:
        dm   = req.GET['dm']
        con  = MySQLdb.connect(host='localhost',user='root',passwd='',db='webot')
        con.query("set names 'utf8'")
        cur  = con.cursor()
        res  = cur.execute("""select concat(sum(count),''),time from blog_redis_count where domain=%s and time>%s group by time""",(dm,now_time()))
        dt   = cur.fetchall()
        result = json.dumps({'result':dt,'dm':dm})
        cur.close()
        con.close()
        return HttpResponse(result)
    conn = MySQLdb.connect(host='localhost',user='root',passwd='',db='webot')
    conn.query("set names 'utf8'")
    cur  = conn.cursor()
    res  = cur.execute("""select domain,concat(sum(count),'') from blog_redis_count where time>%s group by domain order by sum(count) desc limit 100""",(now_time()))
    dat  = cur.fetchall()
    income_count = cur.execute("""select concat(sum(count),''),time from blog_redis_count where time>%s group by time""",(now_time(),))
    ic   = cur.fetchall()
    cur.close()
    conn.close()
    ic = [map(int,[i[0],i[1]]) for i in ic]
    return render_to_response('income_ranking.html',{'user':user,'dat':dat,'domain':domain,'ic':ic})

#采发时间差处理函数
@login_required
def time_diff(req):
    user  = req.user 
    t_d_1 = Time_Diff.objects.filter(date_time=now_date(0)).order_by('-time_out')
    t_d_2 = Time_Diff.objects.filter(date_time=now_date(1)).order_by('-time_out')
    t_d_3 = Time_Diff.objects.filter(date_time=now_date(2)).order_by('-time_out')
    t_d_4 = Time_Diff.objects.filter(date_time=now_date(3)).order_by('-time_out')
    t_d_5 = Time_Diff.objects.filter(date_time=now_date(4)).order_by('-time_out')
    t_d_6 = Time_Diff.objects.filter(date_time=now_date(5)).order_by('-time_out')
    t_d_7 = Time_Diff.objects.filter(date_time=now_date(6)).order_by('-time_out')
    return render_to_response('time_diff.html',{'user':user,'t_d_1':t_d_1,'t_d_2':t_d_2,'t_d_3':t_d_3,'t_d_4':t_d_4,'t_d_5':t_d_5,'t_d_6':t_d_6,'t_d_7':t_d_7})


#秘书配置查询
def config_secretary(req):
    user = req.user
    conf_msg = Config_Mangers.objects.all()
    conf_count = len(conf_msg)
    co = conf_count
    if req.method == "POST":
        if req.POST.get('conf_content',None):
            content = req.POST.get('conf_content',None)
            option = req.POST.get('conf_option',None)
            if option == 'conf_site':
                conf_msg = Config_Mangers.objects.filter(conf_site__icontains=content)
            elif option == 'conf_domain':
                conf_msg = Config_Mangers.objects.filter(conf_domain__icontains=content)
            elif option == 'conf_url':
                conf_msg = Config_Mangers.objects.filter(conf_url__icontains=content)
            elif option == 'conf_link':
                conf_msg = Config_Mangers.objects.filter(conf_link__icontains=content)
        elif req.POST.get('conf_option') == 'ERROR':
            conf_msg = Config_Mangers.objects.filter(conf_site='ERROR')
        co = len(conf_msg)
    return render_to_response('config_mangers.html',{'user':user,'msg':conf_msg,'cou':conf_count,'co':co,'ip':8})


#话题配置查询
def config_topic(req):
    user = req.user
    conf_msg = Config_Topic.objects.all()
    conf_count = len(conf_msg)
    co = conf_count
    if req.method == "POST":
        if req.POST.get('conf_content',None):
            content = req.POST.get('conf_content',None)
            option = req.POST.get('conf_option',None)
            if option == 'conf_site':
                conf_msg = Config_Topic.objects.filter(conf_site__icontains=content)
            elif option == 'conf_domain':
                conf_msg = Config_Topic.objects.filter(conf_domain__icontains=content)
            elif option == 'conf_url':
                conf_msg = Config_Topic.objects.filter(conf_url__icontains=content)
            elif option == 'conf_link':
                conf_msg = Config_Topic.objects.filter(conf_link__icontains=content)
        elif req.POST.get('conf_option') == 'ERROR':
            conf_msg = Config_Topic.objects.filter(conf_site='ERROR')
        co = len(conf_msg)
    return render_to_response('config_mangers.html',{'user':user,'msg':conf_msg,'cou':conf_count,'co':co,'ip':7})
