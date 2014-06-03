{
    "site": "西祠胡同",

    "domains": ["www.xici.net"],

    "urls": {
        "base": "http://www.xici.net/s/?k=hello&page=1&t=2&timesort=1",
        "keywords": {
            "name": "k",
            "file": "#FILENAME#",
            "enc": "gbk"
        }
    },

    "rules": {
        "#1": {
            "xpath": "//div[@class='showpagenum']/a[.='下一页']",
            "regex": "page=([0-9]+)",
            "pages": {
                "start": 1,
                "stop": 5,
                "enc": "gbk"
            }
        },
        "#2": {
            "follow": false,
            "xpath": "//ul[@class='result_list']/li[datetime-delta(concat('20', .//font[contains(@class, 'ml_15')]), '+08:00', 3*3600)]",
            "regex": "/d[0-9]+\\.htm"
        }
    },

    "fields": {
        "url":      {"name":"url",          "xpath":"//a[@id='title']/@href"},
        "title":    {"name":"title",        "xpath":"//a[@id='title']/text()"},
        "author":   {"name":"source",       "value":"${SITE}"},
        "forum":    {"name":"siteName",     "value":"${SITE}"},
        "content":  {"name":"content",      "xpath":"//div[@id='content']", "parse":{"type":"text"}},
        "date":     {"name":"ctime",        "xpath":"//p[@id='date']/text()", "parse":{"type":"cst"}},
        "updated":  {"name":"gtime",        "value":"${NOW}", "parse":{"type":"cst"}},
        "clicks":   {"name":"visitCount",   "value":0},
        "replies":  {"name":"replyCount",   "value":0},
        "category": {"name":"info_flag",    "value":"02"}
    },

    "proxy": {
        "rate": 5,
        "file": "http://192.168.3.175/proxy.txt"
    },

    "settings": {
        "zmq": "tcp://192.168.3.196:10086",
        "dedup": "redis://192.168.3.180:6379/0",
        "plugin": "http://192.168.3.175/plugins/xici_plugin.py",
        "download_delay": 1,
        "download_timeout": 60
    }
}
