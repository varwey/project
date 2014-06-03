#!/bin/bash
# Webbot Status Analysis
# by Kev++ @ 2013-08-15

YEAR=2013
MONTH=9
DAYS=(3,4)

SCRIPT=({define,utils,count}.js)

KEYS=(
http://192.168.3.143/div/tiexue_new
http://192.168.3.143/div/sina_new
http://192.168.3.143/div/sohu_new
)

VALS=(
铁血网
新浪网
搜狐网
)

declare -A SITES

for((i=0;i<${#KEYS[@]};i++))
do
    SITES[${KEYS[$i]}]=${VALS[$i]}
done

for DAY in ${DAYS[@]}
do
    for KEY in ${KEYS[@]}
    do
        mongo --quiet --nodb --eval "site=RegExp('$KEY');name='${SITES[$KEY]}';from=new Date($YEAR, $((MONTH-1)), $DAY);to=new Date($YEAR, $((MONTH-1)), $((DAY+1)));" define.js utils.js count.js | sed -n '/{/,/}/p'
    done
done > out.json

echo '"日期","名称","网站","运行次数","请求次数","请求字节","回复次数","回复字节","错误次数","采集","丢失","重复","最小时间","最长时间","平均时间"' > out.csv
cat out.json |
    jq -r '[.date, .name, .site, .count, .rx_count, .rx_bytes, .tx_count, .tx_bytes, .err_count, .scraped, .dropped, .duplicated, .elapsed_min, .elapsed_max, .elapsed_avg]|@text' |
        sed 's/[][]//g' >> out.csv

