{
    "site"    : "中国新闻网",

    "domains" : ["chinanews.com"],

    "urls"    : {
                    "base": "http://sou.bbs.chinanews.com/index.php?c=sou&m=search&time=one",
                    "keywords": {
                            "name": "keyword",
                            "file": "http://192.168.3.175/keywords/b0b1b2-sorted/b0b1b2-sorted-all.txt",
                            "enc" : "utf-8"
                    }
    
        
        },

    "rules"   : {

        "#1": {
            "follow": false,
            "regex" : "thread-([0-9]+)-1-1.html",
            "xpath": "//div[@id='news_list']/table[datetime-delta(.//div[@class='restore']/text(),'+08:00',0.5*3600)]//li[@class='news_title']"
        }
    },                                       

    "fields": {
        "url"     : {"name": "url",         "value": "${URL}"},
        "title"   : {"name": "title",       "xpath": "//a[@id='thread_subject']|//span[@id='thread_subject']", "parse": {"type": "text"}},
        "author"  : {"name": "source",      "xpath": "(//div[@class='pi']/div[@class='authi'])[1]","parse":{"type": "text"}},
        "date"    : {"name": "ctime",       "xpath": "(//em[contains(@id,'authorposton')])[1]", "parse": {"type":"cst"}},
        "updated" : {"name": "gtime",       "value": "${NOW}", "parse": {"type": "cst"}},
        "forum"   : {"name": "siteName",    "xpath": "concat('中新网论坛-',//div[@id='pt']//a[last()-1]/text())"},
        "content" : {"name": "content",     "xpath": "(//td[contains(@id,'postmessage')])[1]", "parse": [{"type": "clean"},{"type": "text"}]},
        "clicks"  : {"name": "visitCount",  "xpath": "//span[@class='xi1'][1]/text()","parse":{"type":"int"}},
        "replies" : {"name": "replyCount",  "xpath": "//span[@class='xi1'][2]/text()","parse":{"type":"int"}},
        "category": {"name": "info_flag",   "value": "02"}
    },
    
    "settings" : {
                
                "zmq": "tcp://192.168.3.196:10086",
                "dedup": "redis://192.168.3.180:6379/0"
    }
}
