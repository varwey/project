{
    "site": "人民网",

    "domains": ["people.com.cn"],

    "urls":     [
                    #NAME#
                ],

    "rules": {
        
        "#1": {
            "follow": false,
            "regex" : "tid=",
            "xpath": "//*[@id='d_1']/h2[datetime-delta(.//em[2]/text(),'+08:00',0.5*3600)]/b[@class='red']"
        }

    },

    "fields": {
        "url"     : {"name": "url",   	    	"value": "${URL}" },
        "title"   : {"name": "title", 	    	"xpath": "//div[@class='c1']//em", "parse": {"type": "text"}},
        "author"  : {"name": "source",	    	"xpath": "//div[@class='c1']//i", "regex":"网友：(.*)（", "parse": {"type": "text"}},
        "date"    : {"name": "ctime",   	    "xpath": "//div[@class='c1']//i", "parse": {"type": "cst" }},
        "updated" : {"name": "gtime",		    "value": "${NOW}", "parse": { "type": "cst"}},
        "forum"   : {"name": "siteName",    	"xpath": "concat('地方领导留言版-',//h6[@class='gray']/a[last()]/text())" },
        "content" : {"name": "content",     	"xpath": "//div[@class='c1']//p", "parse": [{"type": "clean"},{"type": "text"}]},
        "clicks"  : {"name": "visitCount",      "value": 0},
        "replies" : {"name": "replyCount",      "value": 0},
        "category": {"name": "info_flag",       "value": "02"}


    },
   
    "proxy": {
        "file": "http://192.168.3.175/proxy.txt",
        "rate": 1
    },

    "settings" : {

        "zmq": "tcp://192.168.3.196:10086",
        "dedup": "redis://192.168.3.180:6379/0",
        "download_timeout": 60
    }
}
