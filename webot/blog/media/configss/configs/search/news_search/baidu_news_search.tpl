{
    "site": "百度新闻搜索",

    "domains": ["news.baidu.com"],

    "urls": {
        "base": "http://news.baidu.com/ns?bt=0&et=0&si=&rn=80&tn=news&ie=gb2312&ct=0&word=%B2%DC%CF%D8&pn=0&cl=2",
        "keywords": {
            "name": "word",
            "file": "#FILENAME#",
            "enc": "gbk"
        }
    },

    "loop": "//div[@id='r']/table[datetime-delta(.//nobr/text(), '+08:00', 24*3600)]",

    "fields": {
        "url":      {"name":"url",          "xpath":".//td[@class='text']/a[1]/@href"},
        "title":    {"name":"title",        "xpath":".//td[@class='text']/a[1]/span/b",         "parse":{"type":"text"}},
        "content":  {"name":"content",      "xpath":".//font[@size='-1']",                      "parse":{"type":"text"}},
        "author":   {"name":"source",       "xpath":"substring-before(.//nobr/text(), ' ')",    "default":"未知"},
        "forum":    {"name":"siteName",     "value":"${SITE}"},
        "date":     {"name":"ctime",        "xpath":".//nobr/text()",                           "parse":{"type":"cst"}},
        "updated":  {"name":"gtime",        "value":"${NOW}",                                   "parse":{"type":"cst"}},
        "clicks":   {"name":"visitCount",   "value":0},
        "replies":  {"name":"replyCount",   "value":0},
        "category": {"name":"info_flag",    "value":"01"}
    },

    "proxy": {
        "file": "http://192.168.3.175/proxy.txt"
    },
    
    "settings" : {

        "zmq": "tcp://192.168.3.196:10086",
        "dedup": "redis://192.168.3.180:6379/0"
                                     }
    }
