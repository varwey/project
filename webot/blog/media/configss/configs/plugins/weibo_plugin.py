#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# plugin for <s.weibo.com>
# by Kev++

import re, json
from urllib2 import urlparse

def parse(url, body, **kwargs):
    page_num = re.search(r'(?<=page=)([0-9]+)', url).group(1)
    next_page = re.sub(r'(?<=page=)([0-9]+)', str(int(page_num)+1), url)
    for line in body.decode('utf-8', errors='ignore').splitlines():
        if line.startswith('<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_feedlist"'):
            l, r = line.find('{'), line.rfind('}')
            return u'''
                <html>
                <body>
                    <div id="content">{}</div>
                    <a id="page" href="{}">下一页</a>
                </body>
                </html>
                '''.format(json.loads(line[l:r+1]).get('html'), next_page).encode('utf-8')
    else:
        return '<html/>'

if __name__=='__main__':
    url = 'http://s.weibo.com/weibo/%25E6%259B%25B9%25E5%258E%25BF&xsort=time&scope=ori&timescope=custom:2013-07-21-8:2013-07-21-18&Refer=g&page=1'
    body = '<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_weibo_feedlist", "html":"..."})</script>'
    print parse(url, body)

