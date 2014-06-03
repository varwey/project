#!/bin/bash
# 批量生成天涯贴吧搜索配置文件
# WARNING: RUN THIS SCRIPT IN CURRENT DIRECTORY

rm -f tianya_search-*.conf

for i in {00..09}
do
    KWFILE=http://192.168.3.175/keywords/b0b1b2-sorted/b0b1b2-sorted-$i.txt
    CONFIG=tianya_search-$i.conf
    MINUTE=$(printf '%02d' $((${i#0}*6%60)))
    sed "s@#FILENAME#@$KWFILE@g" tianya_search.tpl > $CONFIG
    echo "$MINUTE * * * * curl http://192.168.3.172:6800/schedule.json -d project=example -d spider=example -d setting=CLOSESPIDER_TIMEOUT=3600 -d config=http://192.168.3.175/bbs/tianya_search/$CONFIG"
done
