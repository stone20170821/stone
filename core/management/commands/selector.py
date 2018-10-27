# encoding:utf-8

from django.core.management import BaseCommand
from core.models import HorseBasic, ClassName, ModelDicts, HorseKDataBase, CfsDongfangcaijing
from command_utils import basic_table_date_format
import traceback
import time
import random
import json


def sort_random(code_list):
    sort_list = list()
    for code in code_list:
        sort_list.append((code, random.randint(0, 1000)))

    sort_list.sort(key=lambda x: x[1])
    return sort_list


class Command(BaseCommand):
    # 不提供的时候参数的值，如果值为这个，应该不处理
    PARAM_EMPTY_KEY = 'empty'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--s20181013', nargs='?', default=self.PARAM_EMPTY_KEY,
                            help='')

        parser.add_argument('--s20181022', nargs='?', default=self.PARAM_EMPTY_KEY,
                            help='')

    def handle(self, *args, **options):
        if options['s20181013'] is None:
            self.selector20181013()

        if options['s20181022'] is None:
            self.selector20181022()

    def selector20181022(self):
        """
        pe <= 30
        profit > 0
        ...
        :return: 
        :rtype: 
        """
        objs = HorseBasic.objects.filter(pe__lte=30, pe__gt=0, profit__gt=0, npr__gt=0, gpr__gt=40)
        time_start = time.mktime(time.strptime('2014-1-1', '%Y-%m-%d'))
        res = list()
        x = 9
        for obj in objs:
            cfs = CfsDongfangcaijing.objects.filter(code=obj.code, report_date__gte=time_start, n_cashflow_act__gte=0)
            if len(cfs) > x:
                res.append(obj.code)

        # for code in res:
        #     print code

        print 'total', len(res)
        print res
        res = sort_random(res)
        print json.dumps(res, indent=4)

    def selector20181013(self):
        """
        pe <= 40
        profit > 0(增长率)
        price * 数量（总值）处于前5%（权重股）
        数量=undp / perundp
        :return: 
        :rtype: 
        """
        horses = HorseBasic.objects.filter(pe__lte=40, profit__gte=0)

        value_list = list()
        for horse in horses:
            horse_class = ModelDicts.k_data_default[ClassName.k_data_default(horse.code)]
            day_lines = horse_class.objects.all().order_by('-date')
            # if len(day_lines) > 0:
            try:
                last_day_line = day_lines[0]
                """:type: HorseKDataBase"""
                if last_day_line.date.strftime(basic_table_date_format) == '20181012':
                    cur_price = last_day_line.close
                    if horse.perundp != 0:
                        stock_count = horse.undp / horse.perundp

                        final_value = cur_price * stock_count
                        value_list.append((horse.code, final_value))
                    else:
                        print '%s perundp is 0' % horse.code
                else:
                    print '%s last day is not 1012' % horse.code
            except:
                print '%s except' % horse.code
                traceback.print_exc()
                # else:
                #     print '%s day lines is zero' % horse.code

        # print value_list
        print len(value_list)

        sh = list()
        sz = list()
        cy = list()
        for horse_detail in value_list:
            if horse_detail[0].startswith('6'):
                sh.append(horse_detail)
            elif horse_detail[0].startswith('3'):
                cy.append(horse_detail)
            elif horse_detail[0].startswith('0'):
                sz.append(horse_detail)

        # value_list.sort(key=lambda x: x[1], reverse=True)
        # cut_list = value_list[:len(value_list)*0.618]
        # print len(cut_list)
        # print cut_list
        def _sort_key(h_tuple):
            return h_tuple[1]

        sh.sort(key=_sort_key, reverse=True)
        sz.sort(key=_sort_key, reverse=True)
        cy.sort(key=_sort_key, reverse=True)

        def _print_list(h_list):
            print '---------------'
            print 'total', len(h_list)
            for h in h_list:
                print h
            print '---------------'

        # print len(sh)
        # print len(sz)
        # print len(cy)
        _print_list(sh[:int(len(sh) * 0.0618)])
        _print_list(sz[:int(len(sz) * 0.0618)])
        _print_list(cy[:int(len(cy) * 0.0618)])
