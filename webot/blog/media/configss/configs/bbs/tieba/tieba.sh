#!/bin/bash
# -*- encoding: utf-8 -*-
# Generate webbot config files for tieba.baidu.com
# by Kev++

jq -s 'group_by(.group) | map({key:(.[0].group), value:(sort_by(.members)|reverse|map({name, members}))}) | from_entries' tieba.json | python tieba.py
