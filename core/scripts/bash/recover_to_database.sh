cur_file_path="$(cd `dirname $0`;pwd)"
psql -U postgres -f ${cur_file_path}/../sql/replace_database_from_file.sql -v database_name=stone_test -v owner_name=wgx -v template_name=stone_zero