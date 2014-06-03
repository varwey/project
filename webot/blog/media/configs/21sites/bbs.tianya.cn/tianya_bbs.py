#!/usr/bin/env python

import json
from collections import namedtuple


Item = namedtuple('Item', 'key, val')
items = []


def load():
    for line in open('./tianya_bbs.json'):
        obj = json.loads(line)
        items.append(Item(obj['id'], obj['postcount']))

def split(n=10):
    count = len(items)
    size = 
    pass


if __name__=='__main__':
    load()

