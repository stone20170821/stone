#! encoding:utf-8
from django.core.management import BaseCommand
from argparse import ArgumentParser
from conn_utils import *
import tushare
from pandas import DataFrame
from core.models import *
from datetime import datetime, timedelta
from django.db.models import Max
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

        parser.add_argument('--update_h_data', action='store_true', default=False,
                            dest='update_h_data', help='update get_h_data and save')

    def handle(self, *args, **options):
        if options['get_stock_basics']:
            self.handle_get_stock_basices()

        if options['get_index']:
            self.handle_get_index()

        if options['update_h_data']:
            self.handle_update_h_data()

    def handle_update_h_data(self):
        """
        调用get_h_data更新数据，会根据最后的日期进行，默认执行所有的股票
        """
        print self.handle_update_h_data.__doc__
        # table_codes = HorseBasic.objects.all()
        # for table_code in table_codes:
        #     class_name = ClassName.get_h_default_name_from_code(table_code)
        #     stock_class = horse_h_data_default_class_dict[class_name]
        #     """:type:HorseHDataBase"""
        #     stock_class.objects.
        # code = '600193'
        # df = tushare.get_h_data(code)
        # write_dataframe_to_sql(df, TableName.get_h_default_name_from_code(code), index=True)

        # stock_class = horse_h_data_default_class_dict[ClassName.get_h_default_name_from_code('600171')]
        # last_update_date = stock_class.objects.aggregate(Max('date'))['date__max']
        # print 'Last data date: ' + str(last_update_date)

        codes = HorseBasic.objects.values_list('code').all()
        for code_tuple in codes:
            code = code_tuple[0]
            # 获取上市日期
            time_to_market = datetime.strptime(str(HorseBasic.objects.get(code=code).timeToMarket), basic_table_date_format)
            # 获取当前code的最后一天数据的日期
            stock_class = horse_h_data_default_class_dict[ClassName.get_h_default_name_from_code(code)]
            """:type:HorseHDataBase"""
            last_date = stock_class.objects.aggregate(Max('date'))['date__max']
            start = last_date + timedelta(days=1) if last_date else time_to_market
            end = datetime.now()

            print '%s: Last updated date: %s. So update from %s to %s.' % (str(code), str(last_date), start, end)
            # 按年获取，一次全部获取，会失败，失败之后貌似有缓存，其他本应该能用的不好使了，要等一段时间才能再用
            y = start.year
            cur_start = start
            cur_end = datetime(y, 12, 31)
            now = datetime.now()

            print 'start'

            def write_from_start_to_end(start_str, end_str):
                print 'from %s to %s' % (start_str, end_str)
                # 获取数据
                df = tushare.get_h_data(code, start=start_str, end=end_str)
                # 写入
                write_dataframe_to_sql(df, TableName.get_h_default_name_from_code(code), index=True)

            print 'in the middle'

            while cur_end < now:
                print cur_start
                print cur_end
                start_str = cur_start.strftime(common_date_format)
                end_str = cur_end.strftime(common_date_format)

                write_from_start_to_end(start_str, end_str)

                # 更新start和end
                y += 1
                cur_start = datetime(y, 1, 1)
                cur_end = datetime(y, 12, 31)

            print 'end'

            write_from_start_to_end(cur_start.strftime(common_date_format), end.strftime(common_date_format))


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
