#! encoding:utf-8

from django.utils.translation import ugettext_lazy as _

from core.admin_list_filters.base_list_filters import BaseRangeListFilter


class PeListFilter(BaseRangeListFilter):
    title = _(u'市盈率')
    parameter_name = 'pe'
    const_values = (20, 30, 50, 80, 100, 150, 200)


class PbListFilter(BaseRangeListFilter):
    title = _(u'市净率')
    parameter_name = 'pb'
    const_values = (20,30, 50, 80, 100, 150, 200)


