from django.db import models
from django.contrib.auth.models import User
import time

class Export_Record(models.Model):
    ex_username = models.CharField(max_length=16)
    ex_option = models.CharField(max_length=200)
    ex_type = models.CharField(max_length=10)
    ex_count = models.IntegerField()
    ex_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.ex_username
