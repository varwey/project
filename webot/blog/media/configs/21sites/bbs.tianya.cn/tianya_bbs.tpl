{
    "site"    : "天涯论坛",

    "domains" : ["bbs.tianya.cn", "192.168.3.182"],

    "urls"    : {
                    "base": "http://bbs.tianya.cn/list.jsp?order=1&item=free",
                    "keywords": {
                        "name": "item",
                        "list": #LIST#
                    }
                },

    "rules"   : {
        "#1": {
            "follow": true,
            "xpath" : "//div[@class='links']/a[.='下一页']",
            "regex" : "/list.jsp"
        },
        "#2": {
            "follow": false,
            "xpath" : "//div[@class='mt5']//tr[datetime-delta(td[last()]/@title, '+08:00', 3*3600)]",
            "regex" : "/post-.*shtml"
        }
    },

    "fields": {
        "url"     : {"name": "url",         "value": "${URL}"},
        "title"   : {"name": "title",       "xpath": "//span[@class='s_title']", "parse": {"type": "text"}},
        "author"  : {"name": "source",      "value": "${SITE}"},
        "forum"   : {"name": "siteName",    "value": "${SITE}"},
        "date"    : {"name": "ctime",       "xpath": "//div[@id='post_head']//span[starts-with(., '时间')]", "regex": "时间：([0-9].+[0-9])", "parse": {"type":"cst"}},
        "updated" : {"name": "gtime",       "value": "${NOW}", "parse": {"type": "cst"}},
        "content" : {"name": "content",     "xpath": "(//div[contains(@class, 'bbs-content')])[1]", "parse": {"type": "text"}},
        "clicks"  : {"name": "visitCount",  "xpath": "//div[@id='post_head']//span[starts-with(., '点击')]", "regex": "点击：([0-9]+)", "parse": {"type":"int"}},
        "replies" : {"name": "replyCount",  "xpath": "//div[@id='post_head']//span[starts-with(., '回复')]", "regex": "回复：([0-9]+)", "parse": {"type":"int"}},
        "category": {"name": "info_flag",   "value": "02"}
    },

    "settings": {
        "zmq": "tcp://192.168.3.196:10086",
        "dedup": "redis://192.168.3.180:6379/0"
    }
}
