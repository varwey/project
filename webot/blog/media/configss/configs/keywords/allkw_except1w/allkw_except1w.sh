#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"
mysql -h 192.168.3.175 -uroot -proot keyword < allkw_except1w.sql | tail -n +2 > allkw_except1w.txt
