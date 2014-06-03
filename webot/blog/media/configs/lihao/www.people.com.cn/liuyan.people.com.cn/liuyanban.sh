#! /bin/bash

#rm -f liuyanban.json
#cd /home/spider/github/webbot
#scrapy crawl example -a config=/home/spider/configs/lihao/www.people.com.cn/liuyan.people.com.cn/liuyanban.seed -a debug=true -o /home/spider/configs/lihao/www.people.com.cn/liuyan.people.com.cn/liuyanban.json
#cd /home/spider/configs/lihao/www.people.com.cn/liuyan.people.com.cn

rm -f liuyanban-*.conf
jq .url liuyanban.json > liuyanban.txt
LYnum=`cat liuyanban.txt | wc -l`
csplit -k -f list- -b %0d.txt liuyanban.txt 1 {*}

for ((LYi=1;LYi<=$LYnum;LYi++))
do 
    cat list-$LYi.txt | 
        while read LYname
        do
            sed "s@#NAME#@$LYname@" liuyanban.tpl > liuyanban-$LYi.conf
        done
done

rm -f list-*.txt
