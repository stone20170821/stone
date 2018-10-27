#! encoding:utf-8
from django.core.management import BaseCommand
from django.db.models import Max
from argparse import ArgumentParser
import tushare
from pandas import DataFrame
from datetime import datetime, timedelta

from core.models import *
from conn_utils import *
from command_utils import *
from stone.stone_log_utls import *
from core.model_utils import *


class Command(BaseCommand):
    help = u"下载数据并存入数据库"

    # 不提供的时候参数的值，如果值为这个，应该不处理
    PARAM_EMPTY_KEY = 'empty'
    # 指数
    PARAM_INDEX_KEY = 'index'

    def add_arguments(self, parser):
        """

        :param parser:
        :type parser: ArgumentParser
        :return:
        """
        super(Command, self).add_arguments(parser)
        # 这种传参方式，有以下几种情况：
        # 不提供"--"参数，则为empty
        # 提供"--"参数，但是没有后续，则为None
        # 提供"--"参数，并追加参数，则为追加参数的值
        parser.add_argument('--get_stock_basics', nargs='?', default=self.PARAM_EMPTY_KEY,
                            help='download get_stock_basics and save')

        parser.add_argument('--get_index', nargs='?', default=self.PARAM_EMPTY_KEY, help='update get_index and save')

        parser.add_argument('--get_k_data', nargs='?', default=self.PARAM_EMPTY_KEY, help='update k data')

    def handle(self, *args, **options):
        if options['get_stock_basics'] is None:
            self.handle_get_stock_basices()

        if options['get_index'] is None:
            self.handle_get_index()

        if options['get_k_data'] is None:
            self.handle_get_k_data()
        elif options['get_k_data'] == self.PARAM_INDEX_KEY:
            self.handle_get_k_data(index=True)

    def handle_get_k_data(self, index=False):
        """
        get_k_data: 历史数据，默认前复权，检查旧数据，自动更新
        """
        info_logger.info(self.handle_get_k_data.__doc__)
        info_logger.info('index = ' + str(index))

        def write_to_table(code, final_start, final_end, index=False):
            """
            :param code:
            :type code: str
            :param final_start:
            :type final_start: str
            :param final_end:
            :type final_end: str
            """
            df = tushare.get_k_data(code, start=final_start, end=final_end, index=index)
            table_name = TableName.k_data_default(code) if not index else TableName.k_data_default_index(code)
            write_dataframe_to_sql(df, table_name, index=False)

        codes = get_all_codes_from_models(index=index)
        for code in codes:
            if not index:
                cur_model = ModelDicts.k_data_default[ClassName.k_data_default(code)]
            else:
                cur_model = ModelDicts.k_data_default_index[ClassName.k_data_default_index(code)]
            """:type: HorseKDataBase"""
            cur_max_date = cur_model.objects.aggregate(Max('date'))['date__max']

            # 搞定起始日期
            if cur_max_date:
                start = cur_max_date + timedelta(days=1)
            elif index:
                start = datetime(1990, 1, 1, 0, 0, 0)
            else:
                time_to_market = HorseBasic.objects.get(code=code).timeToMarket
                if time_to_market != 0:
                    start = datetime.strptime(str(time_to_market), basic_table_date_format)
                else:
                    info_logger.info('Time to market is 0. Set to 2000-01-01')
                    start = datetime(2000, 1, 1, 0, 0, 0)

            end = datetime.now()
            start_str = start.strftime(common_date_format)
            end_str = end.strftime(common_date_format)
            if end_str > start_str:
                info_logger.info('Start to download code: %s. from %s to %s.' % (code, start_str, end_str))
                write_to_table(code, start_str, end_str, index=index)
            else:
                info_logger.info('Code %s passed.' % code)

    def handle_get_index(self):
        """
        更新大盘指数，目前不存
        """
        info_logger.info(self.handle_get_index.__doc__)
        df = tushare.get_index()
        """:type : DataFrame"""
        clean_table(IndexInTimeList)
        write_dataframe_to_sql(df, TableName.index_in_time, index=False)

    def handle_get_stock_basices(self):
        """处理股票列表"""
        info_logger.info(self.handle_get_stock_basices.__doc__)
        df = tushare.get_stock_basics()
        """:type : DataFrame"""
        backup_table_to_table(TableName.horse_basic, TableName.horse_basic_backup)
        clean_table(HorseBasic)
        write_dataframe_to_sql(df, TableName.horse_basic)
