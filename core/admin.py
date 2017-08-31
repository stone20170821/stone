from django.contrib import admin

from .models import HorseBasic, HorseBasicBackup
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
