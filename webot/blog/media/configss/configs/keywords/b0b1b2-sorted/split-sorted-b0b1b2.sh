#!/bin/bash
# split sorted keywords
# RUN THIS SCRIPT IN CURRENT DIRECTORY

cd "$( dirname "${BASH_SOURCE[0]}" )" 

rm -f b0b1b2-sorted-*.txt

echo -e 'AUTO GENERATED BY SCRIPT.\nDO NOT EDIT THIS DIRECTORY' > README.txt

mysql -h 192.168.3.175 -uroot -proot keyword < b0b1b2.sql | tail -n +2  > b0b1b2-sorted-all.txt

sum_b=`wc -l < b0b1b2-sorted-all.txt`
avg_b=$((sum_b/10+1))

csplit -k -f b0b1b2-sorted- -b %02d.txt b0b1b2-sorted-all.txt $avg_b {*}
