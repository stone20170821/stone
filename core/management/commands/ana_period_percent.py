#! encoding:utf-8

from django.core.management import BaseCommand
from argparse import ArgumentParser
from pandas import Series

from stone.stone_log_utls import *
from command_utils import *
from core.model_utils import *
from conn_utils import *


class Command(BaseCommand):
    def add_arguments(self, parser):
        """
        :param parser:
        :type parser: ArgumentParser
        """
        super(Command, self).add_arguments(parser)

        parser.add_argument('-n', '--period', type=int, required=True)
        parser.add_argument('-m', '--percent', type=float, required=True)
        # 代表大于m还是小于m
        parser.add_argument('-u', '--up', type=int, default=1)
        # 起始地址，
        # 如果指定，则是从这一天开始的后n天
        # 如果未指定，则是当前数据的最后n天
        parser.add_argument('-s', '--start-date', type=str, default='')
        # 最后的地址
        # parser.add_argument('-l', '--last_date', type=str, default=datetime.now().strftime(common_date_format))

    def handle(self, *args, **options):
        """
        :param args:
        :type args:
        :param options:
        :type options:
        """
        report_logger.info(divider_h1)
        self.handle_command(*args, **options)
        report_logger.info(divider_h1)

    @staticmethod
    def find_both_up_or_down(data_source, up=True):
        """
        找到最大上升或下降区间
        :param up:
        :type up: bool
        :param data_source: [(date, value), ...]
        :type data_source: list[tuple[str|float]]
        :return: tuple(max_value|min_value, start_date, end_date)
        :rtype: tuple
        """
        list_map = list()
        """
        :param: 元组的第一个元素表示最大的差值，第二个元素表示这个最大差值对应的起始位置
        :type: list[tuple[int]]
        """
        total_len = len(data_source)
        if total_len <= 0:
            return 0, datetime.now(), datetime.now()
        # 第一个值，为0
        list_map.append((0, 0))
        cur_max = data_source[0][1]
        cur_max_index = 0
        cur_min = data_source[0][1]
        cur_min_index = 0
        for i in range(1, total_len):
            if up:
                if data_source[i][1] < cur_min:
                    cur_min = data_source[i][1]
                    list_map.append((0, i))
                    cur_min_index = i
                else:
                    list_map.append((data_source[i][1] - cur_min, cur_min_index))
            else:
                if data_source[i][1] > cur_max:
                    cur_max = data_source[i][1]
                    list_map.append((0, i))
                    cur_max_index = i
                else:
                    list_map.append((data_source[i][1] - cur_max, cur_max_index))

        if up:
            index, value = max_index_and_value(list_map)
        else:
            index, value = min_index_and_value(list_map)

        percent = value[0] / (data_source[index][1] - value[0])
        return percent, data_source[value[1]][0], data_source[index][0]

    def handle_command(self, *args, **options):
        """
        ﻿过去n天出现过上涨m，也就是最大比最小上涨了m
        :param args:
        :type args:
        :param options:
        :type options:
        """
        # 搞定参数
        report_logger.info(self.handle_command.__doc__)
        n = options['period']
        m = options['percent']
        origin_u = options['up']
        u = True if origin_u == 1 else False
        start_date = options['start_date']
        start_date_stamp = datetime.strptime(start_date, common_date_format)

        # 打印参数
        param_str = 'param: n=%d m=%f u=%d start_date: %s' % (n, m, origin_u, start_date)
        report_logger.info(param_str)

        # 开始循环
        codes = get_all_codes_from_models()
        count = 0
        for code in codes:
            cur_model = ModelDicts.k_data_default[ClassName.k_data_default(code)]
            """:type: HorseKDataBase"""
            if start_date:
                data_source = cur_model.objects.filter(date__gt=start_date_stamp).values_list('date', 'close').order_by(
                    'date')[:n]
            else:
                # 取出最后n个数据，并按照date升序排列
                data_source = cur_model.objects.values_list('date', 'close').order_by('-date')[:n]
                data_source = sorted(data_source, key=lambda x: x[0])

            # 计算最大上升或下降及其区间
            extreme_value, res_start, res_end = self.find_both_up_or_down(data_source, u)

            print '       code=%s extreme_value=%f start_date=%s end_date=%s' % (
                code, extreme_value, res_start.strftime(common_date_format), res_end.strftime(common_date_format))

            if u:
                if extreme_value > m:
                    report_str = 'code=%s extreme=%f start_date=%s end_date=%s' % (
                        code, extreme_value, res_start.strftime(common_date_format),
                        res_end.strftime(common_date_format))
                    report_logger.info(report_str)
                    count += 1
            else:
                if extreme_value < m:
                    report_str = 'code=%s extreme=%f start_date=%s end_date=%s' % (
                        code, extreme_value, res_start.strftime(common_date_format),
                        res_end.strftime(common_date_format))
                    report_logger.info(report_str)
                    count += 1

        report_logger.info('total: %d' % count)

                    # res_list = list()
                    # count = 0
                    # for code in codes:
                    #     # print code
                    #     table_name = TableName.k_data_default(code)
                    #
                    #     df = read_dataframe_from_sql(table_name, index_col='date')['close'].sort_index()
                    #     # 数据不够
                    #     if len(df) < n:
                    #         continue
                    #     df = df.iloc[-n:]
                    #
                    #     # 如果最后的日期不是要求的，那么不考虑
                    #     # print str(df.index[-1])[:10]
                    #     # if str(df.index[-1])[:10] != cur_date:
                    #     #     continue
                    #
                    #     """:type: Series"""
                    #     res = df.max() / df.min() - 1
                    #     print code + ' ' + str(res)
                    #
                    #     if u:
                    #         if res >= m:
                    #             res_list.append({code: str(df.index[-1])})
                    #             count += 1
                    #     else:
                    #         if res <= m:
                    #             res_list.append({code: str(df.index[-1])})
                    #             count += 1
                    #
                    #     # 每五个输出一次
                    #     if len(res_list) == 5:
                    #         report_logger.info(str(res_list))
                    #         res_list = list()
                    #
                    # report_logger.info(count)
