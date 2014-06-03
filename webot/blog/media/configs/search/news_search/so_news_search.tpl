{
    "site": "360新闻搜索",    

    "domains": ["news.so.com"],

    "urls": {
        "base": "http://news.so.com/ns?rank=pdate&src=srp&q=曹县",
        "keywords": {
            "name": "q",
            "file": "#FILENAME#"
        },
        "pages": {
            "xpath": "//div[@id='page']/a[contains(., '下一页')]",
            "regex": "&pn=([0-9]+)",
            "start": 1,
            "stop": 5
        }
    },

    "loop": "//ul[@id='news']/li[@class='res-list' and datetime-delta(./h3/span, '+08:00', 24*3600)]",

    "fields": {
        "url":      {"name":"url",        "xpath":"./h3/a/@href"},
        "title":    {"name":"title",      "xpath":"./h3/a", "parse":{"type":"text"}},
        "content":  {"name":"content",    "xpath":"./p",    "parse":{"type":"text"}},
        "author":   {"name":"source",     "xpath":"substring-before(./h3/span, ' ')"},
        "forum":    {"name":"siteName",   "value":"${SITE}"},
        "date":     {"name":"ctime",      "xpath":"./h3/span/text()", "parse":{"type":"cst"}},
        "update":   {"name":"gtime",      "value":"${NOW}", "parse":{"type":"cst"}},
        "clicks":   {"name":"visitCount", "value":0},
        "replies":  {"name":"replyCount", "value":0},
        "category": {"name":"info_flag",  "value":"01"}
    },

    "settings" : {

        "zmq": "tcp://192.168.3.196:10086",
        "dedup": "redis://192.168.3.180:6379/0"
                                     }
   }
