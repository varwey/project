#!/bin/bash

rm -f tiebasearch-*-0.conf
cat tieling.txt | 
        while read NAME
        do
            echo "00-59/1 * * * * curl http://192.168.3.179:6800/schedule.json -d project=example -d spider=example  -d setting=CONCURRENT_REQUESTS=100 -d setting=CONCURRENT_REQUESTS_PER_DOMAIN=100 -d config=http://192.168.3.175/bbs/tieling_pd/tiebasearch-$NAME-0.conf"
            sed "s/#NAME#/$NAME/" tiebasearch.tpl > tiebasearch-$NAME-0.conf
            sed -i "s/$NAME/#NAME#/" tiebasearch.tpl
        done
