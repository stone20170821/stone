# coding:utf-8

from django.core.management import BaseCommand

from account import InfoPool

from avg_accounts import MASaveProfitAccount, MAStartAccount, MARepoShareAccount

import matplotlib.pyplot as plt

from core.models import BackResult
import datetime

import os
import json

colors = ['g', 'r', 'c', 'm', 'y', 'k', 'w']

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

# output_order = False

base_index_code = '000001'
base_index_is_index = True
start_date = '20100105'
# start_date = '20180107'

date_format = "%Y_%m_%d_%H_%M_%S"


def code_to_string(code, is_index):
    res = code
    if is_index:
        return res + '_0'
    else:
        return res + '_1'


def generator():
    """
    :param al_type: 
    :type al_type: 
    :return: 
    :rtype: 
    """
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
    return MARepoShareAccount.generator()


class Command(BaseCommand):

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        # parser.add_argument('-t', '--type', type=int, required=True)

    def handle(self, *args, **options):
        p = InfoPool()

        for a in generator():
            base_index = p.get_horse_frame(base_index_code, base_index_is_index)
            base_index_start_value = p.price(start_date, base_index_code, base_index_is_index)
            base_axis = list()
            date_axis = list()

            ds = base_index.ix[start_date:, ['close']].index
            for d in ds:
                date_axis.append(d.strftime(date_format))
                base_axis.append(p.price(d, base_index_code, True) / base_index_start_value)
                a.heartbeats(d, p)

            index_win = base_axis[-1] - 1
            final_win_percent = a.final_win_percent()
            print 'index : {}'.format(index_win)
            print 'final : {}'.format(final_win_percent)

            a.axis['date'] = date_axis
            a.axis['index'] = base_axis

            back_result = BackResult()
            back_result.base_line_result = index_win
            back_result.base_line_code = code_to_string(base_index_code, base_index_is_index)
            back_result.use_code = code_to_string(base_index_code, base_index_is_index)
            back_result.use_code_result = index_win
            back_result.final_win = final_win_percent
            back_result.win_records = json.dumps(a.axis)
            back_result.date_start = datetime.datetime.strptime(date_axis[0], date_format)
            back_result.date_end = datetime.datetime.strptime(date_axis[-1], date_format)
            back_result.run_time = datetime.datetime.now()
            back_result.algorithm_category = a.algorithm_category()
            back_result.algorithm_desc = a.algorithm_desc()
            back_result.param_string = a.param_string()
            back_result.save()
