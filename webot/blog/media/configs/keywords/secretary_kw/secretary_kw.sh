#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"
mysql -h 192.168.3.175 -uroot -proot keyword < secretary_kw.sql | tail -n +2 > secretary_kw.txt
