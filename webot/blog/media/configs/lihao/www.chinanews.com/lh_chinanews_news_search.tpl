{
    "site"    : "中国新闻网",

    "domains" : ["chinanews.com"],

    "urls"    : {  
                        "base": "http://sou.chinanews.com/search.do?ps=10&time_scope=1&channel=all&sort=pubtime&adv=1&day1=&day2=&field=&direction=desc&pager=0",
                        "keywords": {
                        "name": "q",
                        "file": "http://192.168.3.175/keywords/b0b1b2-sorted/b0b1b2-sorted-all.txt",
                        "enc": "utf-8"
                    }
                },

    "rules"   : {
    
            "#1": {
            "follow": false,
            "xpath" : "//div[@id='news_list']/table[datetime-delta(substring-after(.//li[@class='news_other']/text(),' '),'+08:00',0.5*3600)]//li[@class='news_title']"
        }
    },                                       
	
    "fields": {
        "url"     : {"name": "url",         "value": "${URL}"},
        "title"   : {"name": "title",       "xpath": "//div[@id='cont_1_1_2']/h1|//div[@id='_playpic']/i[@class='title']|//div[@id='ssef']//h1", "parse": {"type": "text"}},
        "author"  : {"name": "source",      "value": "${SITE}"},
        "date"    : {"name": "ctime",       "xpath": "//div[@class='left-t']|//div[@id='mian']/div[@class='zxians']/div[contains(.,'时间')]|//div[@id='ssef']//p[@class='Submit_time']", "parse": {"type":"cst"}},
        "updated" : {"name": "gtime",       "value": "${NOW}", "parse": {"type": "cst"}},
        "forum"   : {"name": "siteName",    "value": "${SITE}"},
        "content" : {"name": "content",     "xpath": "//div[@class='left_zw']|//div[@id='mian']/div[@class='zxians']|//div[@class='video_con1']//div[@class='video_con1_text']", "parse": [{"type": "clean"},{"type": "text"}]},
        "clicks"  : {"name": "visitCount",  "value": "0"},
        "replies" : {"name": "replyCount",  "value": "0"},
        "category": {"name": "info_flag",   "value": "01"}
    },
    
    "settings": {
        "zmq": "tcp://192.168.3.196:10086",
        "dedup": "redis://192.168.3.180:6379/0"
    }

}
