{
    "site": "搜搜微博搜索",

    "domains": ["z.soso.com"],

    "urls": {
        "base": "http://z.soso.com/index.php?sort=weibohtml&w=python&na=946656000&time=946656000&flag=1&allnum=9676&qqnum=10242&sohunum=0&sorttype=1",
        "keywords": {
            "name": "w",
            "file": "#FILENAME#",
            "enc":  "gbk"
        },
        "pages": {
            "xpath": "//a[@class='next']",
            "regex": "&pg=([0-9]+)",
            "start": 1,
            "stop":  5
        }
    },

    "loop": "//ol[@id='result_ol']/li[datetime-delta(.//span[@class='timeL'], '+08:00', 1*3600)]",

    "fields": {
        "url":     {"name":"url",       "xpath":".//span[@class='infoR']/a[contains(., '评论')]/@href"},
        "title":   {"name":"title",     "xpath":".//div[@class='msgCnt']",                              "parse":{"type":"text"}},
        "content": {"name":"content",   "xpath":".//div[@class='msgCnt']",                              "parse":{"type":"text"}},
        "forum":   {"name":"siteName",  "value":"腾讯微博"},
        "author":  {"name":"source",    "xpath":".//div[@class='userName']/@rel"},
        "date":    {"name":"ctime",     "xpath":".//span[@class='timeL']/text()",                       "parse":{"type":"cst"}, "filter":{"delta":3600}},
        "updated": {"name":"gtime",     "value":"${NOW}", "parse":{"type":"cst"}},
        "clicks":  {"name":"visitCount","xpath":".//span[@class='infoR']/a[1]/text()",                  "parse":[{"type":"sub", "from":"[^0-9]", "to":""}, {"type":"int"}]},
        "replies": {"name":"replyCount","xpath":".//span[@class='infoR']/a[last()]/text()",             "parse":[{"type":"sub", "from":"[^0-9]", "to":""}, {"type":"int"}]},
        "category":{"name":"info_flag", "value":"04"}
    },

    "settings": {
        "zmq": "tcp://192.168.3.196:10086"
    }
}

