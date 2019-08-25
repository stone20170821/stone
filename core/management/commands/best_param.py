# coding:utf-8

from core.models import BackResult
from django.core.management import BaseCommand
from django.db.models import Avg, Count


def put_sort_index(objs, tuple_index, sort_dict):
    length = len(objs)
    for i in range(0, length):
        obj = objs[i]
        param_string = obj['param_string']
        if param_string not in sort_dict:
            sort_dict[param_string] = [10000, 10000, 10000]
        sort_dict[param_string][tuple_index] = i


def print_objs(objs):
    for obj in objs:
        print obj
    print '\n\n\n'


def sort_lambda(dict_item_tuple):
    return dict_item_tuple[1][0] * 0.4 + dict_item_tuple[1][1] * 0.4 + dict_item_tuple[1][2] * 0.2


class Command(BaseCommand):
    def handle(self, *args, **options):
        # objs = BackResult.objects.filter(buy_count__gt=5)
        base_query = BackResult.objects.filter(buy_count__gt=5) \
            .values('param_string') \
            .annotate(num_id=Count('id'),
                      avg_final_win=Avg('final_win'),
                      avg_max_down=Avg('max_down'),
                      avg_success_rate=Avg('buy_sell_success_rate'),
                      avg_buy_count=Avg('buy_count')) \
            .filter(num_id__gt=5)

        sort_dict = dict()

        objs = base_query.order_by('-avg_final_win')
        print_objs(objs)
        put_sort_index(objs, 0, sort_dict)

        objs = base_query.order_by('-avg_success_rate')
        print_objs(objs)
        put_sort_index(objs, 1, sort_dict)

        objs = base_query.order_by('-avg_final_win')
        print_objs(objs)
        put_sort_index(objs, 2, sort_dict)

        res_list = sorted(sort_dict.items(), key=sort_lambda)

        for res in res_list:
            print res
