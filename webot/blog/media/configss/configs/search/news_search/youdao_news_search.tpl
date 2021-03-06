{
    "site": "有道新闻搜索",    

    "domains": ["news.youdao.com"],

    "urls": {
        "base": "http://news.youdao.com/search?q=%E4%B8%AD%E5%9B%BD&tr=1d&s=bytime&keyfrom=search.timerange&tl",
        "keywords": {
            "name": "q",
            "file": "#FILENAME#"
        },
        "pages": {
            "xpath":"//div[@class='c-pages']",
            "regex":"&start=([0-9]+)",
            "start":0,
            "stop":100
        }
    },

    "loop": "//ul[@id='results']/li[datetime-delta(./h3/nobr/span, '+08:00', 24*3600)]",

    "fields": {
        "url":      {"name":"url",        "xpath":"./h3/a/@href"},
        "title":    {"name":"title",      "xpath":"./h3/a", "parse":{"type":"text"}},
        "content":  {"name":"content",    "xpath":"./p",    "parse":{"type":"text"}},
        "author":   {"name":"source",     "xpath":"substring-before(./h3/nobr/span, ' ')"},
        "forum":    {"name":"siteName",   "value":"${SITE}"},
        "date":     {"name":"ctime",      "xpath":"./h3/nobr/span/text()", "parse":{"type":"cst"}},
        "updated":  {"name":"gtime",      "value":"${NOW}", "parse":{"type":"cst"}},
        "clicks":   {"name":"visitCount", "value":0},
        "replies":  {"name":"replyCount", "value":0},
        "category": {"name":"info_flag",  "value":"01"}
    },

    "settings" : {

        "zmq": "tcp://192.168.3.196:10086",
        "dedup": "redis://192.168.3.180:6379/0"
                                     }
  }
