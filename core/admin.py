#! encoding:utf-8
from django.contrib import admin

from .models import *
from .admin_list_filters.horse_basics_list_filters import PeListFilter, PbListFilter


# Register your models here.

@admin.register(HorseBasic)
class HorseBasicAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'industry', 'pe', 'outstanding', 'totals', 'totalAssets', 'liquidAssets',
                    'fixedAssets', 'esp', 'bvps', 'pb', 'timeToMarket', 'rev', 'profit', 'gpr', 'npr',)
    search_fields = ('code', 'name',)
    list_filter = (PeListFilter, PbListFilter)
    list_per_page = 15


@admin.register(HorseBasicBackup)
class HorseBasicBackupAdmin(HorseBasicAdmin):
    pass


@admin.register(IndexInTimeList)
class IndexInTimeListAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'close', 'change')
    search_fields = ('code', 'name',)


@admin.register(BackResult)
class BackResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'param_string', 'base_line_result', 'final_win',
                    'max_down', 'max_down_start', 'max_down_end', 'algorithm_desc',
                    # 'date_start', 'date_end',
                    'base_line_code', 'use_code', 'run_time',
                    'buy_sell_success_rate', 'total_hold_day_count',
                    'avg_hold_day_count', 'buy_count', 'sell_count')
    list_filter = ('algorithm_desc', 'use_code', 'base_line_code')
    search_fields = ('param_string', 'id',)


@admin.register(BackResultYear)
class BackResultYearAdmin(admin.ModelAdmin):
    list_display = ('id', 'use_year', 'param_string', 'base_line_result', 'final_win',
                    'max_down', 'max_down_start', 'max_down_end', 'algorithm_desc',
                    # 'date_start', 'date_end',
                    'base_line_code', 'use_code')
    list_filter = ('algorithm_desc', 'use_code', 'base_line_code')
    search_fields = ('from_result__id',)


class HorseKDataBaseAdmin(admin.ModelAdmin):
    list_display = ('date', 'open', 'high', 'close', 'low', 'volume')
    search_fields = \
        ('date', 'close',)
    list_per_page = 20

# for key in ModelDicts.k_data_default.keys():
#     k_data_type = type(
#         ClassName.k_data_default(key) + 'Admin',
#         (HorseKDataBaseAdmin,),
#         dict(),
#     )
#     admin.site.register(ModelDicts.k_data_default[key], k_data_type)


# 想看哪一个就注册哪一个
def register_class_in_model_dict(code, index=False):
    class_name = ClassName.k_data_default_index(code) if index else ClassName.k_data_default(code)
    k_data_type = type(
        class_name + 'Admin',
        (HorseKDataBaseAdmin,),
        dict(),
    )
    admin.site.register(ModelDicts.k_data_default[class_name], k_data_type)

register_class_in_model_dict('600171', False)
