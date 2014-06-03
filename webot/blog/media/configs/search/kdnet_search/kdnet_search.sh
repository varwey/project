#!/bin/bash
# 批量生成百度贴吧搜索配置文件
# WARNING: RUN THIS SCRIPT IN CURRENT DIRECTORY

rm -f *.conf

for i in {00..09}
do
    KWFILE=http://192.168.3.175/keywords/b0b1b2-sorted/b0b1b2-sorted-$i.txt
    CONFIG=kdnet_search-$i.conf
    MINUTE=$(printf '%02d' $((${i#0}*6%60)))
    HOUR=$((${i#0}%2))-23/2
    sed "s@#FILENAME#@$KWFILE@g" kdnet_search.tpl > $CONFIG
    echo "*/30 * * * * curl http://192.168.3.170:6800/schedule.json -d project=example -d spider=example -d setting=CLOSESPIDER_TIMEOUT=1800 -d setting=DOWNLOAD_DELAY=1 -d config=http://192.168.3.175/search/kdnet_search/$CONFIG"
done
