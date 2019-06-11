# coding : utf-8

from conn_utils import read_dataframe_from_sql
from core.models import ModelDicts, TableName

from django.core.management import BaseCommand

from account import InfoPool

import datetime
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        now = time.time()
        pool = InfoPool()

        tmp_date = datetime.datetime.strptime('2019-03-04 16:00:00', '%Y-%m-%d %H:%M:%S')

        pool.average_line('20180304', '600171')

        print time.time() - now
