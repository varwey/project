#!/bin/bash
# generate config files for tianya
# WARNING: RUN THIS SCRIPT IN CURRENT DIRECTORY

x=(10 20 30 40 50 100 150 200 250 300 350 400 450 500 600)
y=( 1  1  1  1  1   2   2   2   2   2   2   2   2   2   3   3)

rm -f tianya_*.txt tianya_*.conf

jq -s -r 'sort_by(.postcount + .replcount) | reverse | .[] | .id' tianya_bbs.json |
    csplit -kf 'tianya_bbs-' -b '%02d.txt' - ${x[*]} >/dev/null

for i in tianya_bbs-*.txt
do
    sed "s@#FILENAME#@http://192.168.3.175/bbs/tianya/$i@" tianya_bbs.tpl > ${i%.txt}.conf
    [[ $i =~ bbs-0*([0-9]*) ]]
    idx=${BASH_REMATCH[1]}
    echo "$((idx%60)) */${y[$idx]} * * * curl http://192.168.3.173:6800/schedule.json -d project=example -d spider=example -d setting=CLOSESPIDER_TIMEOUT=$((y[idx]*3600)) -d setting=DEPTH_LIMIT=5 -d config=http://192.168.3.175/bbs/tianya/${i%.txt}.conf"
done

