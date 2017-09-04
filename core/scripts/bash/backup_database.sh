#!/usr/bin/env bash
#set file_name "backup"(date +%m_%d_%H__%Y%m%d__%H%M%S)".psqldb"
#pg_dump -U postgres stone_zero > /Users/wgx/workspace/stone/save/$file_name

export file_name=backup`date +%m_%d_%H__%Y%m%d__%H%M%S`.psqldb
if [ -n "${file_name}" ]; then
    echo "save to ${file_name}"
    pg_dump -U postgres stone_zero > /Users/wgx/workspace/stone/save/${file_name}
fi