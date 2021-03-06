{
    "site": "推特微博",

    "domains": ["query.yahooapis.com"],

    "urls": {
        "base": "http://query.yahooapis.com/v1/public/yql?q=&format=json&callback=",
        "keywords": {
            "name": "q",
            "file": "#FILENAME#",
            "sub": {
                "from":".*",
                "to": "select * from json where url='https://twitter.com/i/search/timeline?q=\\g<0>'"
            }
        },
        "pages": {
            "xpath": "//a[@id='page']",
            "regex": "%26page%3D([0-9]+)",
            "start": 1,
            "stop": 1
        }
    },

    "loop": "//li",

    "fields": {
        "url":      {"name":"url",          "xpath":".//a[@id='url']/@href"},
        "title":    {"name":"title",        "xpath":".//p[@id='content']/text()"},
        "content":  {"name":"content",      "xpath":".//p[@id='content']/text()"},
        "forum":    {"name":"siteName",     "value":"${SITE}"},
        "author":   {"name":"source",       "xpath":".//span[@id='author']/text()"},
        "date":     {"name":"ctime",        "xpath":".//span[@id='date']/text()", "parse":{"type":"date"}, "filter":{"delta": 10000}},
        "updated":  {"name":"gtime",        "value":"${UTCNOW}", "parse":{"type":"date"}},
        "clicks":   {"name":"visitCount",   "value":0},
        "replies":  {"name":"replyCount",   "value":0},
        "category": {"name":"info_flag",    "value":"04"}
    },

    "settings": {
        "download_delay": 5,
        "plugin": "http://192.168.3.175/plugins/twitter_plugin.py",
        "mysql" : "mysql://root:root@192.168.3.148:3309/spider.jingwai"
    }
}
