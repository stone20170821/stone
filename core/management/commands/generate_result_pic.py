# coding:utf-8

from django.core.management import BaseCommand
from core.models import BackResult

import matplotlib.pyplot as plt
import json
import datetime

date_format = "%Y_%m_%d_%H_%M_%S"

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w']


class Command(BaseCommand):
    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)

        parser.add_argument('-i', '--id', type=int, required=True)

    def handle(self, *args, **options):
        res_id = options['id']

        back_res = BackResult.objects.get(pk=res_id)

        records = json.loads(back_res.win_records)

        date_axis = [datetime.datetime.strptime(d, date_format) for d in records['date']]
        keys = list()
        for key in records.keys():
            if key != 'date':
                keys.append(key)

        # 画图
        plt.figure(num=1, figsize=(36, 18))

        i = 0
        for key in keys:
            if key != 'date':
                target = records[key]
                plt.plot(date_axis, target, 'r', color=colors[i])
                i += 1

        plt.title(back_res.algorithm_desc)

        plt.legend(keys)
        plt.show()
