# coding:utf-8

from django.core.management import BaseCommand

from account import InfoPool

from avg_accounts import MASaveProfitAccount

import matplotlib.pyplot as plt

import os

colors = ['g', 'r', 'c', 'm', 'y', 'k', 'w']

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')

# output_order = False

base_index_code = '000001'
base_index_is_index = True
start_date = '20100105'
# start_date = '20180107'


class Command(BaseCommand):
    def handle(self, *args, **options):
        p = InfoPool()

        # if not os.path.exists(output_path):
        #     os.mkdir(output_path)

        # out_dir = os.path.join(output_path, MASaveProfitAccount.output_dir_name())

        # if not os.path.exists(out_dir):
        #     os.mkdir(out_dir)

        # 生成执行日志
        # log_path = os.path.join(out_dir, '000.log')
        # with open(log_path, 'w+') as f:

        index_win = 0
        target_win_groups = list()

        for a in MASaveProfitAccount.generator():
            base_index = p.get_horse_frame(base_index_code, base_index_is_index)
            base_index_start_value = p.price(start_date, base_index_code, base_index_is_index)
            base_axis = list()
            date_axis = list()

            ds = base_index.ix[start_date:, ['close']].index
            for d in ds:
                date_axis.append(d)
                base_axis.append(p.price(d, base_index_code, True) / base_index_start_value)
                a.heartbeats(d, p)

            index_win = base_axis[-1] - 1
            final_win_percent = a.final_win_percent()
            print 'index win : {}'.format(index_win)
            print 'final win : {}'.format(final_win_percent)

            target_win_groups.append((final_win_percent, a.param_string()))

            # if output_order:
            #     for o in a.orders:
            #         f.write(str(o) + '\n')

            # 画图
            # plt.figure(num=1, figsize=(36, 18))
            # plt.plot(date_axis, base_axis, 'r', color='b')
            # i = 0
            # for key in a.axis:
            #     target = a.axis[key]
            #     plt.plot(date_axis, target, 'r', color=colors[i])
            #     i += 1
            # le = ['index', ]
            # le.extend(a.axis.keys())
            # plt.legend(le)
            # plt.title("index win: {}\nfinal win: {}".format(base_axis[-1] - 1, a.final_win_percent()))
            # plt.savefig(os.path.join(out_dir, a.fig_filename()))
            # plt.close()

        # 根据收益排序
        # target_win_groups.sort(key=lambda x: x[0], reverse=True)

        # f.write('index win: {}\n'.format(index_win))
        # for target in target_win_groups:
        #     f.write(str(target) + '\n')
