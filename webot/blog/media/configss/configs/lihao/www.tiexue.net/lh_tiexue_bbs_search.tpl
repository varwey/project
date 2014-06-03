{
    "site"   : "铁血网",

    "domains": ["baidu.com","bbs.tiexue.net"],

    "urls"   : {
                    "base":"http://www.baidu.com/s?wd=hello&pn=0&ct=2097152&tn=bds&ie=utf-8&si=tiexue.net&rsv_page=1",
                    "keywords" : {
                                    "name": "wd",
                                    "file": "http://192.168.3.175/keywords/b0b1b2-sorted/b0b1b2-sorted-all.txt"
                                 }
               },
    "rules"  : {
             
                    "#2": {
                            "follow": false,
                            "regex" : "url",
                            "xpath" : "//td[contains(./div[@class='f13']/span[@class='g']/text(),'小时前')]/h3[@class='t']/a"
                          }
               },

    "fields": {
                "url"     : {"name": "url",         "value": "${URL}"},
                "title"   : {"name": "title",       "xpath": "//div[@class='dir']/a[last()]/text() | //div[@id='themer']//li/h1/text()", "parse": {"type": "text"}},
                "author"  : {"name": "source",      "xpath": "//li[@id='userMsg1']//strong/a/text() | //div[@id='themel']//table//a/text()"},
                "date"    : {"name": "ctime",       "xpath": "(//div[@class='postStart']//div[@class='date']/text())[1] | //div[@id='themel']/following-sibling::div[@class='gray']/text()", "parse": {"type":"cst"}},
                "updated" : {"name": "gtime",       "value": "${NOW}", "parse": {"type": "cst"}},
                "forum"   : {"name": "siteName",    "xpath": "concat('${SITE}-', //div[@class='dir']/a[last()-1]/text() | //div[@id='themer']//li/a/span[@class='red']/text())"},
                "content" : {"name": "content",     "xpath": "//div[@id='postContent'] | //div[@id='themer']/ul/li[@id='contentsbelowbar']/following-sibling::li[1]/div", "parse": [{"type":"clean"},{"type": "text"}]},
                "clicks"  : {"name": "visitCount",  "xpath": "//div[@class='postTit']/p[@class='float_R']/text() | //div[@id='tit']/div[@class='titr']/p/text()[1]", "regex": "([0-9]+)", "parse": {"type":"int"}},
                "replies" : {"name": "replyCount",  "xpath": "number(//div[@class='page']/p/span[last()]/text() | //div[@id='difanye']//strong[3]/text())-1", "parse": {"type":"int"}},
                "category": {"name": "info_flag",   "value": "02"}
               },
    
    "proxy": {  
                "rate": 1,
                "file": "http://192.168.3.175/proxy.txt"
             },
    
    "settings": {
        "dedup": "redis://192.168.3.180:6379/0",
        "zmq"  : "tcp://192.168.3.196:10086",
        "download_delay": 10,
        "download_timeout": 60
    }
           }
