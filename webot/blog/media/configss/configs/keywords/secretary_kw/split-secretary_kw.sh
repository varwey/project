#!/bin/bash
# split sorted keywords
# RUN THIS SCRIPT IN CURRENT DIRECTORY

cd "$( dirname "${BASH_SOURCE[0]}" )" 

rm -f secretary_kw_a*.txt

echo -e 'AUTO GENERATED BY SCRIPT.\nDO NOT EDIT THIS DIRECTORY' > README.txt

mysql -h 192.168.3.175 -uroot -proot keyword < secretary_kw.sql | tail -n +2  > secretary_kw.txt

sum_b=`wc -l < secretary_kw.txt`
avg_b=$((sum_b/5+1))

csplit -k -f secretary_kw_a -b %02d.txt secretary_kw.txt $avg_b {*}
