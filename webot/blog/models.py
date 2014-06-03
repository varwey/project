from django.db import models
import time
from django.contrib.auth.models import User
#coding:utf-8

class Config_Search(models.Model):
    file_name   = models.CharField(max_length=20)
    domain_name = models.CharField(max_length=50)
    config_name = models.FileField(upload_to='configs/')
    writer_time = models.DateTimeField(auto_now=True)
    write_name  = models.CharField(max_length=10)

class Config_Mangers(models.Model):
    conf_site   = models.CharField(max_length=50)
    conf_domain = models.CharField(max_length=150)
    conf_url    = models.TextField()
    conf_link   = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.conf_site

class Config_Topic(models.Model):
    conf_site   = models.CharField(max_length=50)
    conf_domain = models.CharField(max_length=150)
    conf_url    = models.TextField()
    conf_link   = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.conf_site

class Config_Task(models.Model):
    id         = models.AutoField(max_length=11,primary_key=True)
    category_name = models.CharField(max_length=10)
    domain     = models.CharField(max_length=50)
    domain_name= models.CharField(max_length=30,blank=True)
    channel    = models.CharField(max_length=300,blank=True)
    config_path= models.FileField(upload_to='configs/')
    priority_seconds = models.IntegerField(max_length=20,default=120)
    create_datetime = models.DateTimeField(auto_now=True)
    update_datetime = models.DateTimeField(blank=True)
    user       = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.domain

class Config_Update(models.Model):
    altertime  = models.DateTimeField(auto_now=True)
    mender     = models.CharField(max_length=10)
 
    update     = models.ForeignKey(Config_Search)

    def __unicode__(self):
        return self.mender
class Scan_Progress(models.Model):
    scan_date     = models.DateField()
    scan_status_0 = models.IntegerField(max_length=20)
    scan_status_1 = models.IntegerField(max_length=20)
    scan_status_2 = models.IntegerField(max_length=20)

    def __unicode__(self):
        return self.scan_date
 
class List_Query(models.Model):
    config_path   = models.CharField(max_length=250)
    scraped_count = models.IntegerField(max_length=10)
    dropped_count = models.IntegerField(max_length=10)
    duplicated    = models.IntegerField(max_length=10)
    start_time    = models.DateTimeField(blank=True)
    finish_time   = models.DateTimeField(blank=True)
    finish_reason = models.CharField(max_length=50)

class Scan_Count(models.Model):
    date  = models.DateField()
    rate  = models.IntegerField(max_length=3)
    count = models.IntegerField(max_length=10)  

class Redis_Count(models.Model):
    domain = models.CharField(max_length=50)
    count  = models.IntegerField(max_length=10)
    time   = models.IntegerField(max_length=11)

class Storage_Monitor(models.Model):
    time  = models.IntegerField(max_length=11)
    news  = models.IntegerField()
    bbs   = models.IntegerField()
    blog  = models.IntegerField()
    mblog = models.IntegerField()
    mblogs= models.IntegerField()

class Spider_Minute_Count(models.Model):
    site   = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    sld    = models.CharField(max_length=50)
    category=models.CharField(max_length=10)
    time   = models.IntegerField()
    count  = models.IntegerField()

class Spider_Hour_Count(models.Model):
    site   = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    sld    = models.CharField(max_length=50)
    category=models.CharField(max_length=10)
    time   = models.IntegerField()
    count  = models.IntegerField()

class Spider_Day_Count(models.Model):
    site   = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    sld    = models.CharField(max_length=50)
    category=models.CharField(max_length=10)
    time   = models.IntegerField()
    count  = models.IntegerField()

class Time_Diff(models.Model):
    domain   = models.CharField(max_length=100)
    time_5   = models.IntegerField()
    time_10  = models.IntegerField()
    time_15  = models.IntegerField()
    time_30  = models.IntegerField()
    time_60  = models.IntegerField()
    time_out = models.IntegerField()
    date_time= models.DateField()
 
    def __unicode__(self):
       return self.domain
