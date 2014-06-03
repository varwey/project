#!/bin/bash

find -name *.conf > list.txt
sed -i s/.// list.txt
cat list.txt |

        while read LISTname
        do 
            curl http://192.168.3.128:6800/schedule.json -d project=example -d spider=example -d setting=CLOSESPIDER_TIMEOUT=900 -d config=http://192.168.3.175/lihao$LISTname
        done
