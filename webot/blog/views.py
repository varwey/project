#!/usr/bin/python
#coding:utf-8

from __future__ import division
import sys
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django import forms
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from blog.models import Config_Search,Config_Task,Scan_Progress,List_Query,Scan_Count
from datetime import datetime,timedelta
from blog import update_config,list_query,sql_sd
import pymongo,json,re,time,sys,redis,MySQLdb
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib2,utils,calendar

def unixtime(dt):
    return int(calendar.timegm(dt.timetuple())*1000)

#用户登录验证表单
class UserLogin(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码',widget=forms.PasswordInput)

class ConfigAdd(forms.Form):
    configfile = forms.FileField(label='配置文件')

#用户登录处理函数
def userlogin(req):
    if req.method == "POST":
        userlogin = UserLogin(req.POST)
        if userlogin.is_valid():
            username = userlogin.cleaned_data['username']
            password = userlogin.cleaned_data['password']

            user = authenticate(username=username,password=password)
            if user:
                login(req,user)
                return HttpResponseRedirect('/')
            else :
                userlogin = UserLogin()
                errormsg = "用户名或密码错误！"
                return render_to_response('userlogin.html',{'userlogin':userlogin,'errormsg':errormsg})
    else :
        userlogin = UserLogin()
    return render_to_response('userlogin.html',{'userlogin':userlogin})

#用户登出处理
def userlogout(req):
    logout(req)
    return HttpResponseRedirect('/userlogin/')

#系统主页处理以及装饰器控制
@login_required
def index(req):
    user     = req.user
    if req.method == "GET" and 'num' in req.GET:
        num  = int(req.GET['num'])
        fl   = file('/var/www/webot/static/analysis/out.json','r')
        dt   = json.dumps(json.loads((fl.read().split('}'))[num]+'}'))
        fl.close()
        return HttpResponse(dt)
    elif req.method == "GET" and 'time' in req.GET:
        num  = int(req.GET['time'])
        fl   = file('/var/www/webot/static/analysis/out.json','r')
        dat  = fl.read().split('}')
        dat.remove(dat[-1])
        dt   = json.dumps({'result':[json.loads(i+'}') for i in dat]})
        fl.close()
        return HttpResponse(dt)
    return render_to_response('index.html',{'user':user})

#配置检索页面数据渲染
@login_required
def configsearch(req):
    user     = req.user
    configures=Config_Task.objects.all()
    return render_to_response('configsearch.html',{'configures':configures,'user':user})

#配置文件修改页面
@login_required
def configalter(req,num):
    user     = req.user
    config   = Config_Task.objects.get(id = num)   
    config_path = Config_Task.objects.get(id = num).config_path   
    config_file = config_path.read()
    if req.method == 'POST':
        cf = req.POST['cf']
        try:
            update_config.uc(num,config_path.path,cf)
        except:
            err = '修改有误，请重新操作！'
            return render_to_response('configalter.html',{'user':user,'config_file':config_file,'err':err})
        return HttpResponseRedirect('/configsearch/')
    return render_to_response('configalter.html',{'user':user,'config_file':config_file})

#配置文件删除
@login_required
def configdel(req,num,path):
    user     = req.user
    configure=Config_Task.objects.get(id=int(num))
   # configure.delete()
    configures=Config_Task.objects.all()
    return HttpResponse(path)
   # return render_to_response('configsearch.html',{'configures':configures,'user':req.user,'username':username})

#配置文件详细信息展示
@login_required
def configtail(req,num):
    user     = req.user
    config_path = Config_Task.objects.get(id = num).config_path    
    config_file = config_path.read()
    return render_to_response('configtail.html',{'user':user,'config_file':config_file,'num':num})

#添加配置文件
@login_required
def configadd(req):
    user     = req.user
    if req.method == 'POST':
        di = {1:'news',2:'bbs',3:'blog',4:'mblog'}
        configadd = ConfigAdd(req.POST,req.FILES)
        if configadd.is_valid():
            configfile = configadd.cleaned_data['configfile']
            a=configfile.read()
            info = json.loads(a)
            domain_name   = info['site']
            domain = info['domains']
            if info['fields'].get('category',None):
                category_name = di[int(info['fields']['category']['value'])]
            else:
                category_name = 'unknow'
            if info['fields'].get('channel',None):
                channel = info['fields']['channel']['value']
            else:
                channel = '未创建'
            
            cfg = Config_Task.objects.create(category_name=category_name,
                                             domain=domain,
                                             domain_name=domain_name,
                                             channel=channel,
                                             config_path=configfile,
                                             update_datetime=datetime.now(),
                                             user=user.username)
            cfg.save()
            return HttpResponseRedirect('/configsearch/')
    else :
        configadd=ConfigAdd()
    return render_to_response('configadd.html',{'configadd':configadd,'user':user})


#问题配置数据渲染，采用前台局部刷新    
def problemconfig(req):
    user     = req.user
    return render_to_response('problemconfig.html',{'user':user})


#清单查询，mongo数据，GETJSON处理
def listquery(req):
    user     = req.user
    if req.method == 'GET'and 'config' in req.GET:
        conf = req.GET['config']
        msg  = list_query.l_q(conf)
        return HttpResponse(msg)
    return render_to_response('listquery.html',{'user':user})

#url查询，redis数据，GET方式处理
def urlquery(req):
    user     = req.user
    if req.method == 'GET' and 'config'in req.GET:
        urlq = req.GET['config']
        udb  = req.GET['udb']
        if int(udb) == 0:
            r= redis.StrictRedis(host='192.168.94.3',port=6379)
        elif int(udb) == 1:
            r= redis.StrictRedis(host='192.168.94.2',port=6379, db=1)
        elif int(udb) == 2:
            r= redis.StrictRedis(host='192.168.94.10',port=6379, db=1)
        elif int(udb) == 3:
            r= redis.StrictRedis(host='192.168.94.13',port=6379)
        result = r.hgetall(utils.hash_url(urlq))
        if len(result)==0:
            urldt = json.dumps({})
            return HttpResponse(urldt)
        urldt= json.dumps({
                         'message':'ok',
                         'result':result,
                         'code':0, 
                         'time':unixtime(datetime.utcnow())
                          })
        return HttpResponse(urldt)
    else:
        return render_to_response('urlquery.html',{'user':user})

#采集状态，外部引入
@login_required
def collectorstate(req):
    user     = req.user
    return render_to_response('collectorstate.html',{'user':user})

#入库统计，图形展示，外部引入
@login_required
def storagecount(req):
    user     = req.user
    return render_to_response('storagecount.html',{'user':user})

#扫描统计，图表展示，MYSQLDB处理
@login_required
def scan_count(req):
    user     = req.user
    sd       = Scan_Count.objects.all().order_by('-date')[0:30]
    return render_to_response('scan_count.html',{'user':user,'scan_data':sd})

#扫描进度,googlecharts处理
@login_required
def scan_progress(req):
    user     = req.user
    sd       = Scan_Progress.objects.all().order_by('-scan_date')[0:7]
    scd      = []
    for s in sd:
        co   = s.scan_status_0+s.scan_status_1+s.scan_status_2
        s1   = '%.2f'%(s.scan_status_0/co)
        s2   = '%.2f'%(s.scan_status_1/co)
        s3   = '%.2f'%(s.scan_status_2/co)
        scd.append([s.scan_date,s1,s2,s3])
    return render_to_response('scan_progress.html',{'user':user,'sd':sd,'scd':scd})

#爬虫服务处理
@login_required
def spider_server(req):
    user     = req.user
    server_list = sql_sd.select('192.168.3.130','task','spider_server','status')
    ssl      = [[s[1],s[2],s[3],s[4],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(int(s[5]))),s[0]] for s in server_list]
    return render_to_response('spider_server.html',{'user':user,'ssl':ssl})

#爬虫服务管理，增加，修改，以及删除功能处理函数    
@login_required
def spider_server_manger(req,im,it):
    user     = req.user
    if req.method == 'POST':
        if int(im) == 0:
            warn = '必填项不能为空或者填写格式有误，请重试！'
            if req.POST.get('ip') =="" or req.POST.get('name') =="" or req.POST.get('server_id') =="" or req.POST.get('last_ping_datetime') =="":
                return render_to_response('spider_server_add.html',{'user':user,'warn':warn})
            try:
                ssnd = (req.POST.get('server_id'),
                        int(req.POST.get('type') or 0),
                        req.POST.get('ip'),
                        req.POST.get('name'),
                        int(req.POST.get('status') or 0),
                        int(req.POST.get('last_ping_datetime'))
                       )
                conn = MySQLdb.connect(host='192.168.3.130',user='root',passwd='root',db='task')
                cur  = conn.cursor()
                s    = cur.execute('insert into spider_server(server_id,type,ip,name,status,last_ping_datetime) values(%s,%s,%s,%s,%s,%s)',ssnd)
                conn.commit()
                cur.close()
                conn.close()    
                return HttpResponseRedirect('/spider_server/')
            except:
                return render_to_response('spider_server_add.html',{'user':user,'warn':warn})
           
        conn = MySQLdb.connect(host='192.168.3.130',user='root',passwd='root',db='task')
        cur  = conn.cursor()
        s    = cur.execute('select * from spider_server where server_id=%s',it)
        ssod = cur.fetchone()
        types= int(req.POST.get('type') or ssod[1])
        status=int(req.POST.get('status') or ssod[4])
        lpd  = int(req.POST.get('last_ping_datetime') or ssod[5])
        ip   = req.POST.get('ip') or ssod[2]
        name = req.POST.get('name') or ssod[3]
        ssnd = (types,ip,name,status,lpd,it)
        sql  = 'update spider_server set type=%s,ip=%s,name=%s,status=%s,last_ping_datetime=%s where server_id=%s'
        ssd  = cur.execute(sql,ssnd)
        conn.commit()
        cur.close()
        conn.close()
        return HttpResponseRedirect('/spider_server/')
    if int(im) == 0:
        return render_to_response('spider_server_add.html',{'user':user})
    elif int(im) == 1:
        conn     = MySQLdb.connect(host='192.168.3.130',user='root',passwd='root',db='task')
        conn.query("set names 'utf8'")
        cur      = conn.cursor()
        s    = cur.execute('select * from spider_server where server_id=%s',it)
        ssd  = cur.fetchone()
        cur.close()
        conn.close() 
        return render_to_response('spider_server_alter.html',{'user':user,'ssd':ssd})
    elif int(im) == 2:
        conn     = MySQLdb.connect(host='192.168.3.130',user='root',passwd='root',db='task')
        cur      = conn.cursor()
        s        = cur.execute('delete from spider_server where server_id=%s',it)
        conn.commit()
        cur.close()
        conn.close()
        return HttpResponseRedirect('/spider_server/') 

#任务列表展示处理函数        
@login_required
def task_list(req):
    user     = req.user
    task     = sql_sd.select('192.168.3.109','task','task_list','start_datetime')[::-1]
    task_list= [i+(int(i[17]) - int(i[16]),time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(i[16]))) for i in task]
    return render_to_response('task_list.html',{'user':user,'task_list':task_list})

#任务详细状况        
@login_required
def task_list_tail(req,num):
    user     = req.user
    conn     = MySQLdb.connect(host='192.168.3.120',user='root',passwd='root',db='run_log')
    cur      = conn.cursor()
    s        = cur.execute('select * from task_start_log where task_id=%s',(int(num)))
    start    = cur.fetchone()
    uuid     = start[0]
    domain   = start[5]
    e        = cur.execute('select * from task_end_log where uuid=%s',(uuid))
    end      = cur.fetchone()
    hour_data= cur.execute('select * from scrapy where uuid=%s',(uuid))
    hd       = cur.fetchone()
    datas    = cur.execute('select * from scrapy where domain=%s order by response_count',(domain))
    dts      = cur.fetchall()
    cur.close()
    conn.close()
    try:
        h_d = list(hd[14:26])
        if not hd[24]:
            h_d[-2] = 0 
        sd   = json.dumps({'result':h_d}) 
        start= start + (end[2],(end[1]-start[9]))
        hd   = hd[10:12]
    except:
        sd   = json.dumps({})
        hd   = ()
    return render_to_response('task_list_tail.html',{'user':user,'start':start,'sd':sd,'hd':hd,'dts':dts})

#任务列表管理，曾加，批量导入，修改，以及删除功能处理
@login_required
def task_list_manger(req,tlo,tlid):
    user     = req.user
    if req.method == "POST":
        em = '输入有误请重试！'
        if int(tlo) == 0:
            if int(tlid) == 0:
                try:
                    tlad = (req.POST.get('category_name'),
                            req.POST.get('domain'),
                            req.POST.get('domain_name').encode('utf-8'),
                            req.POST.get('channel').encode('utf-8'),
                            req.POST.get('config_url'),
                            req.POST.get('project_name'),
                            req.POST.get('spider_name'),
                            req.POST.get('spider_params'),
                            req.POST.get('priority_seconds') or 120,
                            req.POST.get('create_datetime'),
                            req.POST.get('update_datetime'),
                            req.POST.get('tag'),
                            req.POST.get('status'),
                            req.POST.get('server_id'),
                            req.POST.get('thread_id'),
                            req.POST.get('start_datetime'),
                            req.POST.get('end_datetime'),
                            req.POST.get('uuid'),
                            req.POST.get('node_id') or 0,
                            req.POST.get('is_sync')
                            )
                    sql      = """insert into task_list(category_name,domain,domain_name,channel,config_url,
                                  project_name,spider_name,spider_params,priority_seconds,create_datetime,
                                  update_datetime,tag,status,server_id,thread_id,start_datetime,end_datetime,
                                  uuid,node_id,is_sync) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    conn     = MySQLdb.connect(host='192.168.3.130',user='root',passwd='root',db='task')
                    conn.query("set names 'utf8'")
                    cur      = conn.cursor()
                    s        = cur.execute(sql,tlad)
                    conn.commit()
                    cur.close()
                    conn.close()
                    return HttpResponseRedirect('/task_list/')
                except Exception as e:
                    return render_to_response('task_list_add.html',{'user':user,'em':em,'e':e})
            if req.POST.get('tag') and req.FILES.get('cf'):
                tag = req.POST.get('tag')
                cf  = req.FILES.get('cf').read()
                f   = open('/var/www/webot/crontab.txt','w')
                f.write(cf)
                f.close()
                import_crontab("/var/www/webot/crontab.txt", tag)
                return HttpResponseRedirect('/task_list/')
            return render_to_response('task_list_addmany.html',{'user':user,'em':em})
        conn     = MySQLdb.connect(host='192.168.3.130',user='root',passwd='root',db='task')
        conn.query("set names 'utf8'")
        cur      = conn.cursor()
        s        = cur.execute('select * from task_list where id=%s',tlid)
        sld      = cur.fetchone()
        try:
            tlad = (req.POST.get('category_name') or sld[1],
                    req.POST.get('domain') or sld[2],
                    req.POST.get('domain_name').encode('utf-8') or sld[3],
                    req.POST.get('channel').encode('utf-8') or sld[4],
                    req.POST.get('config_url') or sld[5],
                    req.POST.get('project_name') or sld[6],
                    req.POST.get('spider_name') or sld[7],
                    req.POST.get('spider_params') or sld[8],
                    req.POST.get('priority_seconds') or sld[9],
                    req.POST.get('create_datetime') or sld[10],
                    req.POST.get('update_datetime') or sld[11],
                    req.POST.get('tag') or sld[12],
                    req.POST.get('status') or sld[13],
                    req.POST.get('server_id') or sld[14],
                    req.POST.get('thread_id') or sld[15],
                    req.POST.get('start_datetime') or sld[16],
                    req.POST.get('end_datetime') or sld[17],
                    req.POST.get('uuid') or sld[18],
                    req.POST.get('node_id') or sld[19],
                    req.POST.get('is_sync') or sld[20],sld[0]
                    )
            sql  = """update task_list set category_name=%s,domain=%s,domain_name=%s,channel=%s,
                      config_url=%s,project_name=%s,spider_name=%s,spider_params=%s,priority_seconds=%s,
                      create_datetime=%s,update_datetime=%s,tag=%s,status=%s,server_id=%s,thread_id=%s,
                      start_datetime=%s,end_datetime=%s,uuid=%s,node_id=%s,is_sync=%s where id=%s"""
            s    = cur.execute(sql,tlad)
            conn.commit()
            cur.close()
            conn.close()
            return HttpResponseRedirect('/task_list/')
        except Exception as e:
            return render_to_response('task_list_alter.html',{'user':user,'sld':sld,'em':em,'e':e})
                
    if int(tlo) == 0:
        if int(tlid) ==1:
            return render_to_response('task_list_addmany.html',{'user':user})
        return render_to_response('task_list_add.html',{'user':user,})
    elif int(tlo) == 1:
        conn     = MySQLdb.connect(host='192.168.3.130',user='root',passwd='root',db='task')
        conn.query("set names 'utf8'")
        cur      = conn.cursor()
        s        = cur.execute('select * from task_list where id=%s',tlid)
        sld      = cur.fetchone()
        cur.close()
        conn.close()
        return render_to_response('task_list_alter.html',{'user':user,'sld':sld})
    elif int(tlo) == 2:
        conn     = MySQLdb.connect(host='192.168.3.130',user='root',passwd='root',db='task')
        cur      = conn.cursor()
        s        = cur.execute('delete from task_list where id=%s',tlid)
        cur.close()
        conn.close()
        return HttpResponseRedirect('/task_list/')


def txt(req):
    return render_to_response('proxy.txt')

#配置错误信息
@login_required
def config_error(req):
    user     = req.user
    ce       = sql_sd.select('192.168.3.120','run_log','config_error')[::-1]
    return render_to_response('config_error.html',{'user':user,'config_error':ce})
 
#任务分发总情况
@login_required
def task_distribution(req):
    user     = req.user
    if req.method == 'GET' and 'val' in req.GET:
        val      = req.GET['val']
        num      = int(req.GET['num'])
        tp       = req.GET['type']
        conn     = MySQLdb.connect(host='192.168.3.120',user='root',passwd='root',db='run_log')
        conn.query("set names 'utf8'")
        cur      = conn.cursor()
        try:
            hour_data= cur.execute('''select floor(unix_timestamp(start_datetime)/%s) as start,
                                      sum(unix_timestamp(end_datetime)-unix_timestamp(start_datetime))/count(id) from scrapy where
                                      %s="%s" group by start'''%(num,tp,val))
            hd   = cur.fetchall()
            all_data = [list(map(int, i)) for i in hd]
            ad   = json.dumps({'result':all_data,'num':num})
        except:
            ad   = json.dumps({})
        cur.close()
        conn.close()
        return HttpResponse(ad)
    if req.method == 'GET' and 'dt' in req.GET:
        dt = req.GET['dt']
        num = req.GET['num']
        conn     = MySQLdb.connect(host='192.168.3.120',user='root',passwd='root',db='run_log')
        conn.query("set names 'utf8'")
        cur      = conn.cursor()
       # try:
        hour_data= cur.execute("""select sum(exception_count),
                                         sum(timeout_count),
                                         sum(request_count),
                                         sum(response_count),
                                         sum(status_200_count),
                                         sum(dropped_count),
                                         sum(duplicated_count),
                                         sum(scraped_count) from
                                         scrapy where floor(unix_timestamp(start_datetime)/%s)=%s"""%(num,dt))
        hd       = cur.fetchone()
        s        = cur.execute("""select *,unix_timestamp(start_datetime),unix_timestamp(end_datetime) from
                                  scrapy where floor(unix_timestamp(start_datetime)/%s)=%s"""%(num,dt))
        chart    = cur.fetchall()
        chart    = [list(i[:10]+i[12:]) for i in chart]
        h_d      = [int(i) for i in hd]
        sd       = json.dumps({'result':h_d,'chart':chart})
       # except:
        #    sd       = json.dumps({})
        cur.close()
        conn.close()
        return HttpResponse(sd)
    return render_to_response('task_distribution.html',{'user':user})


#统计任务分发
@login_required
def task_situation(req):
    user     = req.user
    conn     = MySQLdb.connect(host='192.168.3.120',user='root',passwd='root',db='run_log')
    cur      = conn.cursor()
    hour_data= cur.execute("""select start.uuid,category_name,domain,domain_name, config_url,priority_seconds,
                              from_unixtime(start_datetime),tag,from_unixtime(end_datetime),result_code from
                              task_start_log as start join task_end_log as end on start.uuid=end.uuid
                              order by result_code""")
    hd       = cur.fetchall()
    cur.close()
    conn.close()
    return render_to_response('task_situation.html',{'user':user,'hd':hd})

#统计每个网站的请求，返回，超时等情况
@login_required
def http_status(req):
    user     = req.user
    hd       = sql_sd.select('192.168.3.120','run_log','scrapy','response_count')
    return render_to_response('http_status.html',{'user':user,'hd':hd})

#任务详情表
@login_required
def task_tail(req,domain):
    user     = req.user
    if req.method == 'GET' and 'uuid' in req.GET:
        uid = req.GET['uuid']
        try:
            hd = sql_sd.select('192.168.3.120','run_log','scrapy',uuid=uid)
            h_d = list(hd[14:26])
            if not hd[24]:
                h_d[-2] = 0 
            sd   = json.dumps({'result':h_d}) 
        except:
            sd   = json.dumps({}) 
        return HttpResponse(sd)
    conn     = MySQLdb.connect(host='192.168.3.120',user='root',passwd='root',db='run_log')
    cur      = conn.cursor()
    hour_data= cur.execute("""select start.uuid,category_name,domain,domain_name, config_url,priority_seconds,
                            from_unixtime(start_datetime+(3600*8)),tag,from_unixtime(end_datetime+(3600*8)),
                            result_code,(end_datetime - start_datetime),start_datetime from
                            task_start_log as start join task_end_log as end on start.uuid=end.uuid where domain=%s""",(domain))
    hd       = cur.fetchall()
    cur.close()
    conn.close()
    uuid     = [i[0] for i in hd]
    h_d      = json.dumps([[h[-1],h[-2],h[0]] for h in hd])
    return render_to_response('task_tail.html',{'user':user,'hd':hd,'h_d':h_d,'domain':domain})
