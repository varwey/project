#coding:utf-8
from django.db import models

class spider_count(models.Model):
    site   = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)
    category=models.CharField(max_length=10) 
    time   = models.DateTimeField()
    count  = models.IntegerField(max_length=10)
class redis_count(models.Model):
    domain = models.CharField(max_length=50)
    count  = models.IntegerField(max_length=10)
    time   = models.IntegerField(max_length=11)    
