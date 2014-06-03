#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# by Kev++

from w3lib.url import safe_url_string
from twisted.internet import reactor, task
import cgi, hashlib, urllib, urlparse, logging, sys
import logging, logging.handlers

def hash_url(url):
    if isinstance(url, unicode):
        url = url.encode('utf-8')
    url = std_url(url)
    sha1 = hashlib.sha1()
    sha1.update(url)
    return sha1.hexdigest()

def std_url(url, keep_blank_values=True, keep_fragments=False):
    scheme, netloc, path, params, query, fragment = urlparse.urlparse(url)
    keyvals = cgi.parse_qsl(query, keep_blank_values)
    keyvals.sort()
    query = urllib.urlencode(keyvals)
    path = safe_url_string(path) or '/'
    fragment = '' if not keep_fragments else fragment
    return urlparse.urlunparse((scheme, netloc.lower(), path, params, query, fragment))

def setup_logger(log):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter('%(asctime)s\t[%(levelname)s]\t%(message)s', datefmt='%Y-%m-%dT%H:%M:%S')

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    fh = logging.handlers.TimedRotatingFileHandler(log, when='D')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

class LogStats(object):
    def __init__(self):
        self.tick = 60
        self.items_prev = self.items_curr = 0
        self.task = task.LoopingCall(self.log)
        self.task.start(self.tick)

    def log(self):
        speed = (self.items_curr-self.items_prev)*60//self.tick
        logging.info('received: {} items, speed: {} items/min'.format(self.items_curr, speed))
        self.items_prev = self.items_curr

    def inc(self):
        self.items_curr += 1

    def stop(self):
        self.task.stop()
