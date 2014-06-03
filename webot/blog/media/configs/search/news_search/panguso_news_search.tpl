{
    "site": "盘古新闻搜索",

    "domains": ["news.panguso.com"],

    "urls": {
        "base":"http://news.panguso.com/newssearch.htm?n=50&orderType=2&searchType=&hasImage=&sname=&q=%E6%9B%B9%E5%8E%BF",
        "keywords": {
            "name":"q",
            "file": "#FILENAME#"
        }
    },

    "loop": "//ol[@id='result_ol']/li[datetime-delta(.//div[@class='url']/a, '+08:00', 24*3600)]",

    "fields": {
        "url":      {"name":"url",          "xpath":"./@rsurl"},
        "title":    {"name":"title",        "xpath":".//h3/a", "parse":{"type":"text"}},
        "content":  {"name":"content",      "xpath":"./p", "parse":{"type":"text"}},
        "author":   {"name":"source",       "xpath":".//div[@class='url']/cite/text()"},
        "forum":    {"name":"siteName",     "value":"${SITE}"},
        "date":     {"name":"ctime",        "xpath":".//div[@class='url']/a/text()", "parse":{"type":"cst"}},
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
