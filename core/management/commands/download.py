#! encoding:utf-8
from django.core.management import BaseCommand
from django.db.models import Max
from argparse import ArgumentParser
import tushare
from pandas import DataFrame
from datetime import datetime, timedelta

from core.models import *
from conn_utils import *
from core_time_utils import *


class Command(BaseCommand):
    help = u"下载数据并存入数据库"

    def add_arguments(self, parser):
        """

        :param parser:
        :type parser: ArgumentParser
        :return:
        """
        super(Command, self).add_arguments(parser)

        parser.add_argument('--get_stock_basics', action='store_true', default=False,
                            dest='get_stock_basics', help='download get_stock_basics and save')

        parser.add_argument('--get_index', action='store_true', default=False,
                            dest='get_index', help='update get_index and save')

        parser.add_argument('--get_k_data', action='store_true', default=False,
                            dest='get_k_data', help='update k data')

    def handle(self, *args, **options):
        if options['get_stock_basics']:
            self.handle_get_stock_basices()

        if options['get_index']:
            self.handle_get_index()

        if options['get_k_data']:
            self.handle_get_k_data()

    def handle_get_k_data(self):
        """
        get_k_data: 历史数据，默认前复权，检查旧数据，自动更新
        """
        print self.handle_get_k_data.__doc__

        def write_to_table(code, final_start, final_end):
            """
            :param code:
            :type code: str
            :param final_start:
            :type final_start: str
            :param final_end:
            :type final_end: str
            """
            df = tushare.get_k_data(code, start=final_start, end=final_end)
            write_dataframe_to_sql(df, TableName.k_data_default(code), index=False)

        basics = HorseBasic.objects.all()[:5]
        codes = basics.values_list('code')
        for code_tuple in codes:
            code = code_tuple[0]
            cur_model = ModelDicts.k_data_default[code]
            """:type: HorseKDataBase"""
            cur_max_date = cur_model.objects.aggregate(Max('date'))['date__max']
            start = cur_max_date + timedelta(days=1) if cur_max_date else datetime.strptime(
                str(HorseBasic.objects.get(code=code).timeToMarket), basic_table_date_format)
            """:type: datetime"""
            end = datetime.now()
            if end > start:
                write_to_table(code, start.strftime(common_date_format), end.strftime(common_date_format))

    def handle_get_index(self):
        """
        更新大盘指数，目前不存
        """
        print self.handle_get_index.__doc__
        df = tushare.get_index()
        """:type : DataFrame"""
        clean_table(IndexInTimeList)
        write_dataframe_to_sql(df, TableName.index_in_time, index=False)

    def handle_get_stock_basices(self):
        """处理股票列表"""
        print self.handle_get_stock_basices.__doc__
        df = tushare.get_stock_basics()
        """:type : DataFrame"""
        backup_table_to_table(TableName.horse_basic, TableName.horse_basic_backup)
        clean_table(HorseBasic)
        write_dataframe_to_sql(df, TableName.horse_basic)
