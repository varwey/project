#!/bin/bash

find -name *.conf > list.txt
sed -i s/.// list.txt
cat list.txt |

        while read NAME 
        do 
            echo "00-59/30 * * * * curl http://192.168.3.108:6800/schedule.json -d project=example -d spider=example -d setting=CLOSESPIDER_TIMEOUT=1800 -d config=http://192.168.3.175/caolei$NAME"
        done
rm -f list.txt
