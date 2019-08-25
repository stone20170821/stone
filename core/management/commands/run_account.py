# coding:utf-8

from django.core.management import BaseCommand

from account import InfoPool

from avg_accounts import MASaveProfitAccount, MAStartAccount, MARepoShareAccount, MACrossAccount
from boll_accounts import SimpleBollAccount
from macd_accounts import MacdGoldCrossAccount

import matplotlib.pyplot as plt

from core.models import BackResult
import datetime

import os
import json


# colors = ['g', 'r', 'c', 'm', 'y', 'k', 'w']

# output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

# output_order = False

# base_index_code = '000001'
# base_index_is_index = True
# start_date = '20100105'
# start_date = '20180107'

# date_format = "%Y_%m_%d_%H_%M_%S"
#
#
# def calculate_max_down(hold_prices, dates=None):
#     cur_max_down = 0
#     cur_max_value = -1
#     max_down_start = 0
#     max_down_end = 0
#     saved_max_index = 0
#
#     l = len(hold_prices)
#     for i in range(0, l):
#         hp = hold_prices[i]
#         if hp > cur_max_value:
#             cur_max_value = hp
#             saved_max_index = i
#
#         my_max_down = (cur_max_value - hp) / cur_max_value
#         if my_max_down > cur_max_down:
#             cur_max_down = my_max_down
#             max_down_start = saved_max_index
#             max_down_end = i
#
#     if dates:
#         return cur_max_down, \
#                datetime.datetime.strptime(dates[max_down_start], date_format), \
#                datetime.datetime.strptime(dates[max_down_end], date_format)
#     else:
#         return cur_max_down, None, None


# def code_to_string(code, is_index):
#     res = code
#     if is_index:
#         return res + '_0'
#     else:
#         return res + '_1'


def generator(pool):
    # if al_type == 0:
    #     pass
    #     # for i in range(300, 500):
    #     #     yield MAStartAccount(ma_length=i)
    # elif al_type == 1:
    #     pass
    #     # 单均线
    #     ds = range(5, 200, 5)
    #     for d in ds:
    #         yield MARepoShareAccount([d, ])
    # return MARepoShareAccount.generator()
    # return SimpleBollAccount.generator(pool)
    # return MAStartAccount.generator(pool)
    # return MACrossAccount.generator(pool)
    return MacdGoldCrossAccount.generator(pool)


class Command(BaseCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        # parser.add_argument('-t', '--type', type=int, required=True)

    def handle(self, *args, **options):
        p = InfoPool()

        for a in generator(p):
            # base_index = p.get_horse_frame(base_index_code, base_index_is_index)
            # base_index_start_value = p.price(start_date, base_index_code, base_index_is_index)
            # base_axis = list()
            # date_axis = list()

            # ds = base_index.ix[start_date:, ['close']].index
            for d in a.date_axis_origin:
                # date_axis.append(d.strftime(date_format))
                # base_axis.append(p.price(d, base_index_code, True) / base_index_start_value)

                if a.before_heartbeats(d):
                    a.heartbeats(d)
                    a.after_heartbeats(d)

            a.done_this_round()

            print 'final: {}'.format(a.final_win_percent())

            # index_win = base_axis[-1] - 1
            # final_win_percent = a.final_win_percent()
            # print 'index : {}'.format(index_win)
            # print 'final : {}'.format(final_win_percent)
            #
            # a.axis['date'] = date_axis
            # a.axis['index'] = base_axis
            #
            # md, md_s, md_e = calculate_max_down(a.axis['hold'], a.axis['date'])
            #
            # back_result = BackResult()
            # back_result.base_line_result = index_win
            # back_result.base_line_code = code_to_string(base_index_code, base_index_is_index)
            # back_result.use_code = code_to_string(base_index_code, base_index_is_index)
            # back_result.use_code_result = index_win
            # back_result.final_win = final_win_percent
            # back_result.win_records = json.dumps(a.axis)
            # back_result.date_start = datetime.datetime.strptime(date_axis[0], date_format)
            # back_result.date_end = datetime.datetime.strptime(date_axis[-1], date_format)
            # back_result.run_time = datetime.datetime.now()
            # back_result.algorithm_category = a.algorithm_category()
            # back_result.algorithm_desc = a.algorithm_desc()
            # back_result.param_string = a.param_string()
            # back_result.max_down = md
            # back_result.max_down_start = md_s
            # back_result.max_down_end = md_e
            # back_result.save()
