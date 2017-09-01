#! encoding:utf-8

# 是否线上

ONLINE = True

database_name = 'stone_zero'
if not ONLINE:
    database_name = 'stone_test'
