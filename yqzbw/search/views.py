#!/usr/bin/python
#coding:utf-8

from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from search.models import Export_Record
import json
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from search import mongo_search
import urllib
import hashlib
from urllib import urlencode
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

def binary_segmentation(word):
    words = []
    for i in range(len(word),1,-1):
        for e in range(0,len(word)-i+1):
            wd = word[e:e+i]
            words.append(wd)
            if wd.islower():
               words.append(wd.upper())
            elif wd.isupper():
               words.append(wd.lower())
    return words

def slice_word(word):
    words = []
    for i in word.split(' '):
        words += binary_segmentation(i.split(':')[-1])
    return words


#持久库搜索引擎
def lasting_search(req):
#    if 'value' in req.GET:
#        value,sk,con=(json.loads(req.GET['value']),req.GET['sk'],req.GET['con'])
#        print value,con
#        res,count = mongo_search.search(value,sk)
#        result = json.dumps({'result':res,'count':count})
#        return HttpResponse(result)
#    total = '{:,}'.format(mongo_search.total())
#    return render_to_response('lasting_search.html',{'total':total})
    return render_to_response('lasting_search.html')

#获取每条信息详细情况
def tail(req,_id):
    print '_id', _id
    try:
        tail = mongo_search.tail(_id)[0]
    except:
        tail = {'title': 'error', 'siteName': 'error', 'content': 'error'}
    val = req.GET.get('val')
    if val[:4] not in ['url:http:']:
        for i in slice_word(val):
            for e in ['title','siteName','content']:
                tail[e] = tail[e].replace(i,'<b style="color:red;">'+i+'</b>')
        
    return render_to_response('lasting_search.html',{'tail':tail})

def hudie(req):
    if 'value' in req.GET:
        value,sk,con=(req.GET['value'],req.GET['sk'],req.GET['con'])
        print value
        pa = '&pages='+str(int(sk)+1)+'&pageNum=10'
        url = 'http://192.168.85.18:8080/IndexSearch/search?'+urlencode({"keyword":value})+pa
        page = urllib.urlopen(url)
        dt  = page.read()
        l, r = dt.find('{'), dt.rfind('}')
        dt = json.loads(dt[l:r+1])
        if dt['result']:
            result = json.dumps({'result':dt['data'][0]['items'],'count':dt['count'],'usetime':dt['useTime']})
        else:
            result = json.dumps({'result':[]})
        return HttpResponse(result)
    return render_to_response('lasting_search.html',{})

def total(req):
    fl = file('/var/www/yqzbw/static/programe/total.txt','r')
    result = fl.read()
    fl.close()
    return HttpResponse(result)


def jindu(req):
    f_n = req.GET['file_name']
    url = 'http://192.168.85.18:8080/IndexSearch/datalog/' + f_n + '.txt'
    page = urllib.urlopen(url)
    dt  = page.read()
    ex_count = dt.strip()
    return HttpResponse(ex_count)

def check(req):
    username,password,user_md5 = (req.GET['username'],req.GET['password'],req.GET['user_md5'])
    user = authenticate(username=username,password=password)
    usercode = hashlib.md5(user_md5).hexdigest().upper()
    if user:
        return HttpResponse(json.dumps({'username':username,'usercode':usercode}))
    return HttpResponse(json({'username':''}))

def save_record(req):
    u_n,o_n,g_s,e_s = (req.POST.get('username',None),req.POST.get('option',None),req.POST.get('geshi',None),req.POST.get('sum',None))
    record = Export_Record.objects.create(ex_username=u_n,ex_option=o_n,ex_type=g_s,ex_count=e_s)
    print record
    return HttpResponse('ok')
