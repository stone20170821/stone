# coding: utf-8

from django.core.management import BaseCommand
from core.models import BackResult
from command_utils import iterate_for_all


class Command(BaseCommand):
    def handle(self, *args, **options):
        res_dict = dict()

        objs = iterate_for_all(BackResult, True)
        for obj in objs:
            if obj.base_line_code == obj.use_code and obj.final_win > obj.base_line_result:
                if obj.param_string not in res_dict:
                    res_dict[obj.param_string] = 0

                res_dict[obj.param_string] += 1

        sr = sorted(res_dict.items(), key=lambda x: x[1], reverse=True)
        for s in sr:
            print s

            # objs = iterate_for_all(BackResult, True)
            # for obj in objs:
            #     if obj.base_line_code != obj.use_code:
            #         obj.delete()
