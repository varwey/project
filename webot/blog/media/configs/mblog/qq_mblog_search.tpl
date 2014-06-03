{
    "site": "腾讯微博搜索",

    "domains": ["open.t.qq.com"],

    "urls": {
        "base": "http://open.t.qq.com/api/search/t?openid=BB7E933EBBC4639D48C9BCB8B8487FA1&searchtype=8&format=json&oauth_version=2.a&msgtype=1&needdup=0&endtime=0&contenttype=0&keyword=%E6%B7%B1%E5%9C%B3&pagesize=30&access_token=c0fa935322e3e9f2c8bcdc1dac49ac18&oauth_consumer_key=801404868&starttime=0&scope=all&page=1",

        "qstr": {
            "openid": "00ed873d925ec47c59424ddc90da4d57",
            "access_token": "286549beda9b79cc3637165f74ed9465",
            "oauth_consumer_key": "801356664"
        },

        "keywords": {
            "name": "keyword",
            "file": "#FILENAME#",
            "enc": "utf-8"
        }
    },

    "loop": "$.data.info.*",

    "fields": {
        "url":      {"name":"url",          "jpath":"$.id",        "parse":{"type":"sub", "from":"^", "to":"http://t.qq.com/p/t/"}},
        "title":    {"name":"title",        "jpath":"$.origtext",  "parse":[{"type":"text"}, {"type":"unesc"}]},
        "forum":    {"name":"siteName",     "value":"腾讯微博"},
        "author":   {"name":"source",       "jpath":"$.nick"},
        "date":     {"name":"ctime",        "jpath":"$.timestamp", "parse":{"type":"date", "fmt":"unix"}, "filter":{"delta":3600}},
        "updated":  {"name":"gtime",        "value":"${NOW}",      "parse":{"type":"cst"}},
        "content":  {"name":"content",      "jpath":"$.origtext",  "parse":[{"type":"text"}, {"type":"unesc"}]},
        "clicks"  : {"name":"visitCount",   "value": 0},
        "replies" : {"name":"replyCount",   "value": 0},
        "category": {"name":"info_flag",    "value":"05"}
    },

    "settings": {
        "download_delay": 0,
        "zmq": "tcp://192.168.3.196:10086",
        "download_delay": 0
    }
}

