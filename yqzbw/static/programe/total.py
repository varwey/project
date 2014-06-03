#!/usr/local/bin/python
#coding:utf8

"""
one easy to catch the data of count from lucene
2014/04/01 by www
"""

import urllib
import json
import time
from urllib import urlencode

def ask_data(url):
    page = urllib.urlopen(url)
    dt = page.read()
    l, r = dt.find('<body>') + 10, dt.rfind('</body>') - 4
    dt = json.dumps({'total':int(dt[l:r])})
    fl = file('./total.txt','w')
    w = fl.write(dt)
    fl.close()
    return dt

if __name__ == "__main__":
    while True:	
        ask_data('http://192.168.85.18:8080/IndexSearch/total')
	time.sleep(2)
    print 'finshed!'
