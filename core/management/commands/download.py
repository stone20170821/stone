#! encoding:utf-8
from django.core.management import BaseCommand
from argparse import ArgumentParser
from conn_utils import *
import tushare
from pandas import DataFrame
from core.models import *


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

    def handle(self, *args, **options):
        if options['get_stock_basics']:
            self.handle_get_stock_basices()

        if options['get_index']:
            self.handle_get_index()

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
