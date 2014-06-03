{
    "site"    : "凯迪论坛",

    "domains" : ["kdnet.net"],

    "urls"    : {  
        "base": "http://search.kdnet.net/",
        "keywords": {
            "name": "q",
            "file": "#FILENAME#",
            "enc": "gbk"
        }
    },

    "rules"   : {

        "#1": {
            "xpath" : "//div[@class='pagesmodule']/a[.='下一页']",
            "regex" : "p=([0-9]+)",
            "pages" : {"start":0, "stop":5}
        },

        "#2": {
            "follow": false,
            "regex" : "id=([0-9]+)",
            "xpath" : "//div[@class='search-result-list' and datetime-delta(.//span[@class='c-sub'], '+08:00', 6*3600)]/a"
        }
    },                                       

    "fields": {
        "url"     : {"name": "url",         "value": "${URL}"},
        "title"   : {"name": "title",       "xpath": "//div[@class='posts-title']//text()"},
        "author"  : {"name": "source",      "value": "${SITE}"},
        "forum"   : {"name": "siteName",    "value": "${SITE}"},
        "date"    : {"name": "ctime",       "xpath": "(//div[@class='posts-posted'])[1]", "parse": {"type":"cst"}},
        "updated" : {"name": "gtime",       "value": "${NOW}", "parse": {"type": "cst"}},
        "content" : {"name": "content",     "xpath": "//div[@class='posts-cont']", "parse":{"type":"text"}},
        "clicks"  : {"name": "visitCount",  "xpath": "(//span[@class='f10px fB c-alarm'])[1]/text()", "parse":{"type":"int"}},
        "replies" : {"name": "replyCount",  "xpath": "(//span[@class='f10px fB c-alarm'])[2]/text()", "parse":{"type":"int"}},
        "category": {"name": "info_flag",   "value": "02"}
    },

    "proxy": {
        "file": "http://192.168.3.175/proxy.txt"
    },

    "settings": {
        "zmq":   "tcp://192.168.3.196:10086",
        "dedup": "redis://192.168.3.180:6379/0"
    }
}
