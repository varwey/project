#!/bin/bash
rm -f tieba-*.conf
cat tieling.txt |
        while read NAME
        do
            echo "00-59/1 * * * * curl http://192.168.3.179:6800/schedule.json -d project=example -d spider=example  -d setting=CONCURRENT_REQUESTS=100 -d setting=CONCURRENT_REQUESTS_PER_DOMAIN=100 -d config=http://192.168.3.175/bbs/tieling_pd/tieba-$NAME.conf"
            sed "s/#NAME#/$NAME/" tieba.tpl > tieba-$NAME.conf
            sed -i "s/$NAME/#NAME#/" tieba.tpl
        done
