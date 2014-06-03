#!/bin/bash

rm -f tieba-*.conf
cat baidu_tieba_others.txt |
        while read NAME
        do
            echo "00-59/1 * * * * curl http://192.168.3.168:6800/schedule.json -d project=example -d spider=example  -d setting=CONCURRENT_REQUESTS=100 -d setting=CONCURRENT_REQUESTS_PER_DOMAIN=100 -d config=http://192.168.3.175/bbs/baidu_tieba_others/tieba-$NAME.conf"
            sed "s/#NAME#/$NAME/" baidu_tieba_others.tpl > tieba-$NAME.conf
            sed -i "s/$NAME/#NAME#/" baidu_tieba_others.tpl
        done
