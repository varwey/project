#!/bin/bash
# 批量生成百度贴吧搜索配置文件
# WARNING: RUN THIS SCRIPT IN CURRENT DIRECTORY

rm -f *.conf

IPS=(113 147 107 108 128 137 75 76 80 99)

for j in *.tpl
do
    
    for i in {00..09}
    do
        KWFILE=http://192.168.3.175/keywords/10000keywords/10000-sorted-$i.txt
        CONFIG=${j%.tpl}-$i.conf
        MINUTE=$(printf '%02d' $((RANDOM%60)))
        HOUR=$((RANDOM%2))-23/2
        
        sed "s@#FILENAME#@$KWFILE@g" $j > $CONFIG
        echo "$MINUTE $HOUR * * * curl http://192.168.3.${IPS[${i#0}]}:6800/schedule.json -d project=example -d spider=example -d setting=CLOSESPIDER_TIMEOUT=7200 -d setting=DOWNLOAD_DELAY=1 -d config=http://192.168.3.175/search/news_search/$CONFIG"
    
    done
done
