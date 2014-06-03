#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# plugin for <phantomjs>
# by Kev++

from scrapy.http import FormRequest
from random import choice

PHANTOMJS = 'http://192.168.3.182:{}'
TIMEOUT = 10000
PORTS = [8080, 8081, 8082, 8083]

def parse(url, body, **kwargs):
    meta = kwargs.get('meta', {})
    meta['url'] = url

    if hasattr(spider, 'magic'):
        MAGIC = spider.magic
    else:
        MAGIC = ''

    if 'proxy' in meta:
        del meta['proxy']

    return FormRequest(PHANTOMJS.format(choice(PORTS)), formdata={'html':body, 'url':url, 'timeout':str(TIMEOUT), 'magic':MAGIC}, meta=meta)

