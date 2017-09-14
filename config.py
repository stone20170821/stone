#! encoding:utf-8

# 是否线上

ONLINE = True

database_name = 'stone_zero'
if not ONLINE:
    database_name = 'stone_test'

info_log_name = 'info.log'
if not ONLINE:
    info_log_name = 'info_test.log'

report_log_name = 'report.log'
if not ONLINE:
    report_log_name = 'report_test.log'

error_log_name = 'error.log'
if not ONLINE:
    error_log_name = 'error_test.log'
