#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"
mysql -h 192.168.3.175 -uroot -proot keyword < secretary_kw_1.sql | tail -n +2 > secretary_kw_1.txt
