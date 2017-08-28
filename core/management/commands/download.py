#! encoding:utf-8
from django.core.management import BaseCommand
from argparse import ArgumentParser
from conn_utils import write_dataframe_to_sql, backup_table_to_table, clean_table
import tushare
from pandas import DataFrame
from core.models import HorseBasic, HorseBasicBackup, TableName


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

    def handle(self, *args, **options):
        if options['get_stock_basics']:
            self.handle_get_stock_basices()

    def handle_get_stock_basices(self):
        """处理股票列表"""
        print self.handle_get_stock_basices.__doc__
        df = tushare.get_stock_basics()
        """:type : DataFrame"""
        backup_table_to_table(TableName.horse_basic, TableName.horse_basic_backup)
        clean_table(HorseBasic)
        write_dataframe_to_sql(df, TableName.horse_basic)
