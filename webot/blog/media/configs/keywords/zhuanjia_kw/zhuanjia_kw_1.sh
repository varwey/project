#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"
mysql -h 192.168.3.175 -uroot -proot keyword < zhuanjia_kw_1.sql | tail -n +2 > zhuanjia_kw_1.txt
