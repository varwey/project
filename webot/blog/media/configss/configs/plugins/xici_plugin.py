#!/usr/bin/env python
# plugin for <www.xici.net>
# by Kev++

from urllib2 import urlparse
from jinja2 import Template
from lxml import html
import json

def parse(url, body, **kwargs):
    for line in body.decode('gbk', errors='ignore').splitlines():
        if line.lstrip().startswith('var docData'):
            l, r = line.find('{'), line.rfind('}')
            obj = json.loads(line[l:r+1])
            doc = obj['result']['docinfo'][0]['foolrinfo']
            doc['title'] = obj['result']['sDocTitle']
            doc['url'] = urlparse.urljoin('http://www.xici.net', obj['result']['strPageUrl'])
            doc['date'] = '20'+doc['LongDate']
            doc['content'] = html.fromstring(doc['floorcontent']).text_content()

            tpl = Template('''
                <html>
                <head>
                    <meta content="text/html; charset=utf-8" http-equiv="content-type">
                    <title>{{doc['title']}}</title>
                </head>
                <body>
                    <a id="title" href="{{doc['url']}}">{{doc['title']}}</a>
                    <p id="date">{{doc['date']}}</p>
                    <div id="content">{{doc['content']}}</div>
                </body>
                </html>''')

            return tpl.render(doc=doc).encode('gbk', errors='ignore')
    else:
        return '<html/>'

if __name__=='__main__':
    from urllib2 import urlopen
    url = 'http://www.xici.net/d191559894.htm'
    body = urlopen(url).read()
    print parse(url, body)
