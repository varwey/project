#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#

import json, sys, codecs
from collections import defaultdict
from pprint import pprint

def fun(tpl, keys, max_members=100000, max_size=15, pages=(1, 3)):
    obj = json.load(sys.stdin)
    out = defaultdict(list)

    for k,v in obj.iteritems():
        if k not in keys:
            continue
        j = m = 0
        for i in v:
            key = u'{}-{:02}.conf'.format(k, j)
            out[key].append(i['name'])
            m += i['members']
            if m>=max_members or len(out[key])>=max_size:
                j += 1
                m = 0

    tpl = codecs.open(tpl, encoding='utf-8').read()
    for i, kv in enumerate(out.iteritems()):
        k, v = kv
        with codecs.open(k, mode='w', encoding='utf-8') as f:
            keywords = json.dumps([x.rstrip(u'吧') for x in v], ensure_ascii=False)
            page = pages[0] if len(v)==max_size else pages[1]
            f.write(tpl.replace('#KEYWORDS#', keywords).replace('#PAGE#', str((page-1)*50)))
            print u'{}-59/5 * * * * curl http://192.168.3.194:6800/schedule.json -d project=example -d spider=example -d setting=CONCURRENT_REQUESTS=32 -d setting=CONCURRENT_REQUESTS_PER_DOMAIN=16 -d config=http://192.168.3.175/bbs/tieba/{}'.format(i%5, k).encode('utf-8')

if __name__=='__main__':
    keys = [u'河南', u'河北', u'山东', u'安徽', u'内蒙古']
    fun('tieba.tpl', keys)
