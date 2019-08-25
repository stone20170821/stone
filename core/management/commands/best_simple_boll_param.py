# coding: utf-8

from django.core.management import BaseCommand
from django.db.models import Count, Avg, Sum
from core.models import BackResult
from command_utils import iterate_for_all

from decimal import Decimal


class Command(BaseCommand):
    def handle(self, *args, **options):
        res_win_dict = dict()
        """:type:dict[unicode, list]"""
        res_rate_dict = dict()
        """:type:dict[unicode, list]"""

        objs = iterate_for_all(BackResult, True)
        """:type:list[BackResult]"""

        BackResult.objects.filter(buy_count__gt=5) \
            .annotate(avg_win=Avg('final_win')) \
            .values('id', 'use_code', 'use_code_result', 'param_string', 'final_win',
                    'mac_down', 'buy_sell_success_rate', 'buy_count', 'sell_count')

        for obj in objs:
            if obj.buy_count > 3:
                param_string = obj.param_string

                if param_string.find('simple_boll') >= 0:
                    if param_string not in res_rate_dict:
                        res_rate_dict[param_string] = list()
                    if param_string not in res_win_dict:
                        res_win_dict[param_string] = list()

                    res_rate_dict[param_string].append(obj.buy_sell_success_rate)
                    res_win_dict[param_string].append(obj.final_win)

        def __avg(res_dict):
            res = list()
            for key in res_dict.keys():
                l = res_dict[key]
                sub = 0
                for v in l:
                    sub += v

                avg = sub / Decimal(len(l))

                res.append((key, avg))
            return res

        win_list = __avg(res_win_dict)
        rate_list = __avg(res_rate_dict)

        swr = sorted(win_list, key=lambda x: x[1], reverse=True)
        srr = sorted(rate_list, key=lambda x: x[1], reverse=True)

        print '----------'
        for i in range(0, 100):
            print swr[i]
        print '----------'
        for i in range(0, 100):
            print srr[i]
        print '----------'

        print '----------'
        for i in range(1, 101):
            print swr[-i]
        print '----------'
        for i in range(1, 101):
            print srr[-i]
        print '----------'

            # objs = iterate_for_all(BackResult, True)
            # for obj in objs:
            #     if obj.base_line_code != obj.use_code:
            #         obj.delete()
