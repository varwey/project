#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# generate start url

from lxml import html, etree
from urllib2 import urlparse
from pprint import pprint

home_url = 'http://bbs.hefei.cc'
get_url = 'search.php?mod=forum'
url_xpath = u'//ul[@class="tabs"]//a[.="按时间排序"]/@href'

dom = html.parse(home_url).getroot()
form = dom.xpath('//form[@id="scbar_form"]')[0]
form.set('action', get_url)
form.set('method', 'post')
form.fields.update({
	'srchtxt':'',

})

dom2 = html.parse(html.submit_form(form)).getroot()
form2 = dom2.xpath('//form[@id="topSearchBar"]')[0]
form2.fields.update({'q':'hello'})

dom3 = html.parse(html.submit_form(form2)).getroot()
parsed = urlparse.urlparse(get_url)
print '{0.scheme}://{0.netloc}{1}'.format(parsed, dom3.xpath(url_xpath)[0])

