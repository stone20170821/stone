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


class HorseHDataBaseAdmin(admin.ModelAdmin):
    list_display = ('date', 'open', 'high', 'close', 'low', 'volume', 'amount')
    search_fields = ('date', 'close',)
    list_per_page = 20


for key in horse_h_data_default_class_dict.keys():
    h_data_type = type(
        key + 'Admin',
        (HorseHDataBaseAdmin,),
        dict(),
    )
    admin.site.register(horse_h_data_default_class_dict[key], h_data_type)
