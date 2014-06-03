#!/bin/bash
# 批量生成[微博搜索]配置文件
# WARNING: RUN THIS SCRIPT IN CURRENT DIRECTORY

cd "$( dirname "${BASH_SOURCE[0]}" )"
rm -f *.conf
KWDIR=http://192.168.3.175/keywords

for site in {qq,yunyun,baidu,soso,sina,twitter}
do
    for kw in {test,official}
    do
        TEMPLATE=${site}_mblog_search.tpl
        CONFIG=${site}_mblog_search-${kw}.conf
        if [[ $site = yunyun ]]
        then
            SPIDER=jsonbot
        else
            SPIDER=example
        fi

        if [[ $kw = test ]]
        then
            KWFILE=$KWDIR/weibo_test/weibo_test.txt
        elif [[ $kw = official ]]
        then
            KWFILE=$KWDIR/weibo_official/weibo_official.txt
        fi

        MINUTE=$(printf '%02d-59/15' $(($RANDOM%10)))
        sed "s@#FILENAME#@$KWFILE@g" $TEMPLATE > $CONFIG
        echo "$MINUTE * * * * curl http://192.168.3.158:6800/schedule.json -d project=example -d spider=$SPIDER -d setting=CLOSESPIDER_TIMEOUT=900 -d setting=DOWNLOAD_DELAY=5 -d config=http://192.168.3.175/mblog/$CONFIG"
    done
done
