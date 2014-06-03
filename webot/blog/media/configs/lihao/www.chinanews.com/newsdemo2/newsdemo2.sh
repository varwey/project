#!/bin/bash

rm -f newsdemo2.json
cd /home/spider/github/webbot
scrapy crawl example -a config=/home/spider/configs/lihao/www.chinanews.com/newsdemo2/newsdemo2.seed -a debug=true -o /home/spider/configs/lihao/www.chinanews.com/newsdemo2/newsdemo2.json
cd /home/spider/configs/lihao/www.chinanews.com/newsdemo2

rm -f newsdemo2-*.conf
jq .url newsdemo2.json > newsdemo2.txt
CNnum2=`cat newsdemo2.txt | wc -l`
csplit -k -f list- -b %0d.txt newsdemo2.txt 1 {*}


for ((CNi2=1;CNi2<=$CNnum2;CNi2++))
do 
    cat list-$CNi2.txt |
        while read CNname2
        do
            sed "s@#NAME#@$CNname2@" newsdemo2.tpl > newsdemo2-$CNi2.conf
        done
done

rm -f  list-*.txt 
