{
    "site": "云云微博搜索",

    "domains": ["weibo.yunyun.com"],

    "urls": {
        "base": "http://weibo.yunyun.com/Ajax/Search.php?wbts=1&o=json&q=python&srt=mb&c=0&l=10&rsl=1&ts=1378427496640",

        "qstr": {
            "ts": "${UNOW}000",
            "l": 50
        },

        "keywords": {
            "name": "q",
            "file": "#FILENAME#",
            "sub": {"from":"^", "to":"site:weibo.com "},
            "enc": "utf-8"
        }
    },

    "loop": "$.data[0][*]",

    "fields": {
        "url":      {"name":"url",          "jpath":"$[0][0][0]"},
        "title":    {"name":"title",        "jpath":"$[0][0][2]",  "parse":[{"type":"text"}, {"type":"unesc"}]},
        "forum":    {"name":"siteName",     "value":"新浪微博"},
        "author":   {"name":"source",       "jpath":"$.0.0.1"},
        "date":     {"name":"ctime",        "jpath":"$[0][2]",     "parse":{"type":"date", "fmt":"unix"}, "filter":{"delta":3600}},
        "updated":  {"name":"gtime",        "value":"${NOW}",      "parse":{"type":"cst"}},
        "content":  {"name":"content",      "jpath":"$[0][0][2]",  "parse":[{"type":"text"}, {"type":"unesc"}]},
        "clicks"  : {"name":"visitCount",   "value": 0},
        "replies" : {"name":"replyCount",   "value": 0},
        "category": {"name":"info_flag",    "value":"04"}
    },

    "proxy": {
        "file": "http://192.168.3.175/proxy.txt",
        "rate": 1
    },

    "settings": {
        "download_delay": 0,
        "zmq": "tcp://192.168.3.196:10086"
    }
}

