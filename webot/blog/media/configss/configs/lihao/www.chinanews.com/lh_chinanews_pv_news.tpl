{
    "site"    : "中国新闻网",

    "domains" : ["chinanews.com"],

    "urls"    : [   
                    "http://www.chinanews.com/common/footer/sitemap.shtml"
                ],

    "rules"   : {
        "#1":{
                "follow": true,
                "xpath" : "//div[@class='txt_2_4']/p[position()>last()-4 and position()<last()-1]|//ul[@class='cns_nav']"
        },
        
       
        "#2":{
                "follow": false,
                "xpath" : "//div[@class='img-kuang4' and datetime-delta(./div[@class='text-172']/p[last()]/text(),'+08:00',0.5*3600)]|//ul[@id='wypl']/li[datetime(./p/text(),'+08:00',1*3600)]"
        }



    },

    "fields": {
                "url"     : {"name": "url",         "value": "${URL}"},
                "title"   : {"name": "title",       "xpath": "//div[@id='cont_1_1_2']/h1|//div[@id='_playpic']/i[@class='title']|//div[@id='ssef']//h1", "parse": {"type": "text"}},
                "author"  : {"name": "source",      "value": "${SITE}"},  
                "forum"   : {"name": "siteName",    "value": "${SITE}"},
                "date"    : {"name": "ctime",       "xpath": "//div[@class='left-t']|//div[@id='mian']/div[@class='zxians']/div[contains(.,'时间')]|//div[@id='ssef']//p[@class='Submit_time']", "parse": {"type": "cst"}},
                "updated" : {"name": "gtime",       "value": "${NOW}", "parse": { "type": "cst"}},
                "content" : {"name": "content",     "xpath": "//div[@class='left_zw']|//div[@id='mian']/div[@class='zxians']|//div[@class='video_con1']//div[@class='video_con1_text']", "parse": [{"type": "clean"},{"type": "text"}]},
                "clicks"  : {"name": "visitCount",  "value": 0},
                "replies" : {"name": "replyCount",  "value": 0},
                "category": {"name": "info_flag",   "value": "01"}
    },

    "settings" : {
                
                "zmq": "tcp://192.168.3.196:10086",
                "dedup": "redis://192.168.3.180:6379/0"
    }
}
