#!/bin/bash

rm -f newsdemo1.json
cd /home/spider/github/webbot
scrapy crawl example -a config=/home/spider/configs/lihao/www.chinanews.com/newsdemo1/newsdemo1.seed -a debug=true -o /home/spider/configs/lihao/www.chinanews.com/newsdemo1/newsdemo1.json
cd /home/spider/configs/lihao/www.chinanews.com/newsdemo1

rm -f newsdemo1-*.conf
jq .url newsdemo1.json > newsdemo1.txt
CNnum1=`cat newsdemo1.txt | wc -l`
csplit -k -f list- -b %0d.txt newsdemo1.txt 1 {*}

for ((CNi1=1;CNi1<=$CNnum1;CNi1++))
do 
    cat list-$CNi1.txt |
        while read CNname1
        do
            sed "s@#NAME#@$CNname1@" newsdemo1.tpl > newsdemo1-$CNi1.conf
        done
done

rm -f list-*.txt
