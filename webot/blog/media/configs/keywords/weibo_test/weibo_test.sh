#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"
mysql -h 192.168.3.175 -uroot -proot keyword < weibo_test.sql | tail -n +2 > weibo_test.txt
