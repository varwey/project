#!/usr/bin/env python
# plugin for <www.xici.net>
# by Kev++

from urllib2 import urlparse
from jinja2 import Template
from lxml import html
import json
import re

def parse(url, body, **kwargs):
    txt = re.findall(r'(<div id="ires"><ol eid=.*</ol></div>)',body)[0]
    return u'''
            <html>
            <head>
            <meta content="text/html; charset=utf-8" http-equiv="content-type">
            <title></title>
            </head>
            <body>
            {}
            </body>
            </html>
            '''.format(txt).encode('utf-8')


if __name__=='__main__':
    from urllib2 import urlopen
    url = 'http://www.google.com.hk/search?q=%E7%99%BE%E5%BA%A6&ie=utf-8&oe=utf-8&aq=t&rls=org.mozilla:zh-CN:official&client=firefox-a'
    body = urlopen(url).read()
    print body
    print parse(url, body)

