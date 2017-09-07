#!/usr/bin/env bash
if [ $# -lt 2 ]; then
    echo "usage: recover_from_file [database_name] [backup_file_path]"
    exit
fi
psql -U postgres $1 < $2