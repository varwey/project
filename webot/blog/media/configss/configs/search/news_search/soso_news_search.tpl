{
    "site": "搜搜新闻搜索",

    "domains": ["news.soso.com"],

    "urls": {
        "base": "http://news.soso.com/n.q?pid=n.result.sort.t&ty=c&sd=2&w=%B2%DC%CF%D8&st=t&qc=1&usort=on&interval=&ch=n.search.active",
        "keywords": {
            "name":"w",
            "file": "#FILENAME#",
            "enc": "gbk"
        },
        "pages": {
            "xpath":"//div[@id='pg_list']/a[@class='next']",
            "regex":"&pg=([0-9]+)",
            "start":1,
            "stop":5
        }
    },

    "loop": "//ol[@id='result_list']/li[datetime-delta(.//div[@class='info']/text()[last()], '+08:00', 24*3600)]",

    "fields": {
        "url":      {"name":"url",          "xpath":".//h3/a/@href"},
        "title":    {"name":"title",        "xpath":".//h3/a", "parse":{"type":"text"}},
        "content":  {"name":"content",      "xpath":".//span[contains(@class, 'res_abstract')]", "parse":{"type":"text"}},
        "author":   {"name":"source",       "xpath":".//div[@class='info']/cite/text()"},
        "forum":    {"name":"siteName",     "value":"${SITE}"},
        "date":     {"name":"ctime",        "xpath":".//div[@class='info']/text()[last()]", "parse":{"type":"cst"}},
        "updated":  {"name":"gtime",        "value":"${NOW}", "parse":{"type":"cst"}},
        "clicks":   {"name":"visitCount",   "value":0},
        "replies":  {"name":"replyCount",   "value":0},
        "category": {"name":"info_flag",    "value":"01"}
    },

    "settings" : {

        "zmq": "tcp://192.168.3.196:10086",
        "dedup": "redis://192.168.3.180:6379/0"
                                     }
    }
