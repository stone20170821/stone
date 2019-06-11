# coding:utf-8

from conn_utils import read_dataframe_from_sql
from core.models import ModelDicts, TableName

from django.core.management import BaseCommand

from account import InfoPool, HoldHorse, Account

import datetime
import time


def build_datetime(time_str):
    return datetime.datetime.strptime(time_str + ' 16:00:00', '%Y-%m-%d %H:%M:%S')


class Command(BaseCommand):
    def handle(self, *args, **options):
        """
        单元测试
        :param args: 
        :type args: 
        :param options: 
        :type options: 
        :return: 
        :rtype: 
        """

        day_1 = build_datetime('2019-03-04')
        day_2 = build_datetime('2019-03-05')
        day_3 = build_datetime('2019-03-06')
        day_4 = build_datetime('2019-03-07')

        # # HoldHorse
        # hold = HoldHorse('abc')
        #
        # print hold.buy(1, 100, day_1)
        # print hold
        # print hold.buy(2, 100, day_2)
        # print hold
        # print hold.sell(3, 100, day_3)
        # print hold
        # print hold.sell(4, 1000, day_4)
        # print hold

        # Account
        a = Account()
        print a.buy("abc", 1000, 100, day_1)
        print a
        print a.buy("abc", 1000, 100, day_2)
        print a
        print a.buy("abc", 1000, 100, day_3)
        print a
        print a.buy("abc", 1000, 100, day_4)
        print a
