#!/bin/bash
# 批量生成百度贴吧搜索配置文件
# WARNING: RUN THIS SCRIPT IN CURRENT DIRECTORY

rm -f *.conf

for FLAG in {0..1}
do
    for IDX in {00..09}
    do
        KWFILE=http://192.168.3.175/keywords/b0b1b2-sorted/b0b1b2-sorted-$IDX.txt
        CONFIG=tieba_search_$FLAG-$IDX.conf
        if ((FLAG==0))
        then
            PAGE=5
        else
            PAGE=2
        fi
        MINUTE=$(printf '%02d' $((${IDX#0}*6%60)))
        HOUR=$((${IDX#0}%2))-23/2
        sed -e "s@#FLAG#@$FLAG@g" -e "s@#FILENAME#@$KWFILE@g" -e "s@#PAGE#@$PAGE@g" tieba_search.tpl > $CONFIG
        echo "${IDX#0}-59/15 * * * * curl http://192.168.3.174:6800/schedule.json -d project=example -d spider=example -d setting=CLOSESPIDER_TIMEOUT=3600 -d setting=DOWNLOAD_DELAY=1 -d config=http://192.168.3.175/search/tieba_search/$CONFIG"
    done
done
