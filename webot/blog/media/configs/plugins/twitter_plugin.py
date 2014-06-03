#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# plugin for <twitter.com> via <query.yahooapis.com>

from datetime import datetime
from urllib import urlencode
from urllib2 import urlparse
from lxml import html
from jinja2 import Template
import re, json, requests

tpl = Template(u'''
<html>
<head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type">
    <title>TWITTER SEARCH RESULT</title>
</head>

<body>

    <ul id="navigation">
    {% for i in items %}
        <li>
            <a id="url" href="{{ i.url }}"></a>
            <span id="author">{{ i.author }}</span>
            <span id="date">{{ i.date }}</span>
            <p id="content">{{ i.content }}</p>
        </li>
    {% endfor %}
    </ul>

    {% if next_page %}
        <a id="page" href="{{ next_page }}">下一页</a>
    {% endif %}

</body>
</html>

''')

def parse(url, body, **kwargs):
    base, qstr = url.split('?')
    qstr = dict(urlparse.parse_qsl(qstr))
    obj = json.loads(body)['query']['results']['json']
    dom = html.fromstring(obj['items_html'])
    items = []

    for e in dom.xpath('//li[@data-item-type="tweet"]'):
        url = 'https://twitter.com'+e.xpath('.//a[contains(@class, "detail")]/@href')[0]
        date = datetime.utcfromtimestamp(int(e.xpath('.//small[@class="time"]//span/@data-time')[0]))
        content = e.xpath('.//p[contains(@class, "tweet-text")]')[0].text_content()
        author = e.xpath('.//span[contains(@class, "username")]/b/text()')[0]
        items.append({
                        'url':url,
                        'date':date,
                        'author':author,
                        'content':content
                    })

    if obj['has_more_items']:
        cursor = obj['scroll_cursor']
        qstr['q'] = parse_yql(qstr['q'], cursor)
        next_page = base+'?'+urlencode(qstr)
    else:
        next_page = None

    return tpl.render(items=items, next_page=next_page)

def parse_yql(yql, cursor):
    url = re.search(r"""https://[^'"]*""", yql).group(0)
    base, qstr = url.split('?')
    qstr = dict(urlparse.parse_qsl(qstr))
    qstr.update({
            'scroll_cursor': cursor,
            'src': 'typd',
            'mode': 'relevance',
            'include_available_features': 1,
            'include_entities':1,
            'page':int(qstr.get('page', 1))+1
        })
    url = base+'?'+urlencode(qstr)
    yql = re.sub(r"""https://[^'"]*""", url, yql)
    return yql

if __name__=='__main__':
    url = 'https://twitter.com/i/search/timeline?q=%E6%9B%B9%E5%8E%BF'
    url = "http://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20json%20where%20url%3D'https%3A%2F%2Ftwitter.com%2Fi%2Fsearch%2Ftimeline%3Fq%3D%E6%9B%B9%E5%8E%BF%26page%3D1'&format=json&callback="
    body = requests.get(url).content
    print parse(url, body)
