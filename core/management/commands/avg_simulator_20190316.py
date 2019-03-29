# coding: utf-8

from django.core.management import BaseCommand

from core.models import ModelDicts, ClassName, HorseKDataBase
from stone.stone_log_utls import *
from command_utils import *

import numpy as np
import pandas as pd


class Command(BaseCommand):
    """
    回测目标：看每次指数index上升超过s天均线之后，截至下降低于e天均线之后，最大的上涨幅度
    """

    def add_arguments(self, parser):
        """
        :param parser:
        :type parser: ArgumentParser
        
        python manage.py avg_simulator_20190316 -i 000001 -s 20 -e 20 
        (在每次close上升超过20天线时，开始记录，直到下降20超过最大的上升) 
        """
        super(Command, self).add_arguments(parser)

        parser.add_argument('-i', '--index', type=str, required=True)
        parser.add_argument('-s', '--start', type=int, required=True)
        parser.add_argument('-e', '--end', type=int, default=1)

    def handle(self, *args, **options):
        """
        :param args:
        :type args:
        :param options:
        :type options:
        """
        report_logger.info(divider_h1)
        c = options['index']
        s = options['start']
        e = options['end']

        cur_model = ModelDicts.k_data_default_index[ClassName.k_data_default_index(c)]
        count_start_time = datetime.strptime('2010-01-01', '%Y-%m-%d')
        """:type: HorseKDataBase"""
        lines = cur_model.objects.filter(date__gte=count_start_time)
        dates = [line.date for line in lines]
        closes = [line.close for line in lines]
        # print dates
        # print closes
        dp = pd.DataFrame(closes, index=dates)

        start_day = max([s, e])
        total_days = len(dp)

        large_than_s = False  # s线上
        large_than_e = False  # e线上
        is_hold = False  # 是否持有

        # 统计内容
        current_max = 0  # 当前最大值，从hold开始计算
        buy_value = 0  # 买点
        sell_value = 0  # 卖点
        cur_property = 1  # 最终盈利

        statement_account = list()

        for day in range(start_day, total_days):
            mean_s = dp[day - s + 1: day].mean()[0]
            mean_e = dp[day - e + 1: day].mean()[0]
            cur = dp.iloc[day][0]
            cur_date = dp.index[day]
            pre_large_than_s = large_than_s
            pre_large_than_e = large_than_e
            large_than_s = cur >= mean_s
            large_than_e = cur >= mean_e
            if not is_hold:
                if not pre_large_than_s and large_than_s:
                    # 买点
                    # 记录买点要统计的内容
                    current_max = cur
                    buy_value = cur
                    is_hold = True
                    # 买点对账单
                    statement_line = {
                        'opt': 'buy',
                        'value': cur,
                        'date': cur_date
                    }
                    statement_account.append(statement_line)

            else:
                if (pre_large_than_s and not large_than_s) or (pre_large_than_e and not large_than_e) \
                        or (not large_than_s and not large_than_e):
                    # 卖点
                    # 记录卖点要统计的内容
                    sell_value = cur
                    is_hold = False
                    max_up_percent = (current_max - buy_value) / buy_value * 100
                    # win_percent = (sell_value - buy_value) / buy_value * 100
                    win_percent = 0
                    if max_up_percent > 0:
                        if max_up_percent > 4:
                            win_percent = max_up_percent / 2
                        elif max_up_percent > 2:
                            win_percent = max_up_percent - 2
                        else:
                            win_percent = (sell_value - buy_value) / buy_value * 100

                    cur_property = cur_property * (1 + win_percent / 100)
                    statement_line = {
                        'opt': 'sell',
                        'value': cur,
                        'date': cur_date,
                        'win_percent': win_percent,
                        'total_win_percent': (cur_property - 1) * 100,
                        'max_up': current_max,
                        'max_up_percent': max_up_percent,
                    }
                    statement_account.append(statement_line)
                else:
                    # 持有状态
                    if cur > current_max:
                        current_max = cur

        # 统计2010年之后，各种次数
        buy_count = 0
        sell_count = 0
        max_up_percent_large_than_0 = 0
        max_up_percent_large_than_1 = 0
        max_up_percent_large_than_2 = 0
        max_up_percent_large_than_3 = 0
        max_up_percent_large_than_4 = 0
        max_up_percent_large_than_5 = 0
        max_up_percent_large_than_6 = 0
        max_up_percent_large_than_7 = 0
        max_up_percent_large_than_8 = 0
        max_up_percent_large_than_9 = 0
        max_up_percent_large_than_10 = 0
        max_up_percent_large_than_11 = 0
        max_up_percent_large_than_12 = 0
        max_up_percent_large_than_13 = 0
        max_up_percent_large_than_14 = 0
        max_up_percent_large_than_15 = 0
        max_up_percent_large_than_16 = 0
        max_up_percent_large_than_17 = 0
        max_up_percent_large_than_18 = 0
        max_up_percent_large_than_19 = 0
        max_up_percent_large_than_20 = 0

        total_win_percent = 0
        for statement in statement_account:
            if statement['date'] > count_start_time:
                print statement

                if statement['opt'] == 'buy':
                    buy_count += 1
                elif statement['opt'] == 'sell':
                    if statement['max_up_percent'] > 0: max_up_percent_large_than_0 += 1
                    if statement['max_up_percent'] > 1: max_up_percent_large_than_1 += 1
                    if statement['max_up_percent'] > 2: max_up_percent_large_than_2 += 1
                    if statement['max_up_percent'] > 3: max_up_percent_large_than_3 += 1
                    if statement['max_up_percent'] > 4: max_up_percent_large_than_4 += 1
                    if statement['max_up_percent'] > 5: max_up_percent_large_than_5 += 1
                    if statement['max_up_percent'] > 6: max_up_percent_large_than_6 += 1
                    if statement['max_up_percent'] > 7: max_up_percent_large_than_7 += 1
                    if statement['max_up_percent'] > 8: max_up_percent_large_than_8 += 1
                    if statement['max_up_percent'] > 9: max_up_percent_large_than_9 += 1
                    if statement['max_up_percent'] > 10: max_up_percent_large_than_10 += 1
                    if statement['max_up_percent'] > 11: max_up_percent_large_than_11 += 1
                    if statement['max_up_percent'] > 12: max_up_percent_large_than_12 += 1
                    if statement['max_up_percent'] > 13: max_up_percent_large_than_13 += 1
                    if statement['max_up_percent'] > 14: max_up_percent_large_than_14 += 1
                    if statement['max_up_percent'] > 15: max_up_percent_large_than_15 += 1
                    if statement['max_up_percent'] > 16: max_up_percent_large_than_16 += 1
                    if statement['max_up_percent'] > 17: max_up_percent_large_than_17 += 1
                    if statement['max_up_percent'] > 18: max_up_percent_large_than_18 += 1
                    if statement['max_up_percent'] > 19: max_up_percent_large_than_19 += 1
                    if statement['max_up_percent'] > 20: max_up_percent_large_than_20 += 1

                    total_win_percent = statement['total_win_percent']
                    sell_count += 1

        print 'buy count: %d' % buy_count
        print 'sell count: %d' % sell_count
        print 'max up large than 0: %d' % max_up_percent_large_than_0
        print 'max up large than 1: %d' % max_up_percent_large_than_1
        print 'max up large than 2: %d' % max_up_percent_large_than_2
        print 'max up large than 3: %d' % max_up_percent_large_than_3
        print 'max up large than 4: %d' % max_up_percent_large_than_4
        print 'max up large than 5: %d' % max_up_percent_large_than_5
        print 'max up large than 6: %d' % max_up_percent_large_than_6
        print 'max up large than 7: %d' % max_up_percent_large_than_7
        print 'max up large than 8: %d' % max_up_percent_large_than_8
        print 'max up large than 9: %d' % max_up_percent_large_than_9
        print 'max up large than 10: %d' % max_up_percent_large_than_10
        print 'max up large than 11: %d' % max_up_percent_large_than_11
        print 'max up large than 12: %d' % max_up_percent_large_than_12
        print 'max up large than 13: %d' % max_up_percent_large_than_13
        print 'max up large than 14: %d' % max_up_percent_large_than_14
        print 'max up large than 15: %d' % max_up_percent_large_than_15
        print 'max up large than 16: %d' % max_up_percent_large_than_16
        print 'max up large than 17: %d' % max_up_percent_large_than_17
        print 'max up large than 18: %d' % max_up_percent_large_than_18
        print 'max up large than 19: %d' % max_up_percent_large_than_19
        print 'max up large than 20: %d' % max_up_percent_large_than_20
        print 'total win percent %f' % total_win_percent
