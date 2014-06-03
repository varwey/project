#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# plugin for <people.com.cn>
# by Kev++

import requests
from lxml import html

ENCODE = 'utf-8'
TMOUT = 30

def parse(url, body, **kwargs):
    txt = body.decode(ENCODE, errors='ignore')
    dom = html.fromstring(txt)
    es = dom.xpath('//div[starts-with(@id, "post_content_")]')
    if es:
        e = es[0]
        url = e.get('content_path')
        if url:
            text = requests.get(url, timeout=TMOUT).content.decode(ENCODE)
            e.append(html.fromstring(text))
            return html.tostring(dom, method='html', encoding=unicode).encode(ENCODE)
    return body

if __name__=='__main__':
    url = 'http://bbs1.people.com.cn/post/7/1/2/131884283.html'
    body = requests.get(url).content
    print parse(url, body)
