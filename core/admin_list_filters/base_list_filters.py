#! encoding:utf-8

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class BaseRangeListFilter(admin.SimpleListFilter):
    """
    basic基础处理10 < x < 30这样的Filter，使用这个基类需要做的是：
    定义一个自己的const_values，title，parameter_name
    """
    const_values = ()
    parameter_name = ''

    def lookups(self, request, model_admin):
        res_list = list()
        res_list.append((0, _('<' + str(self.const_values[0]))))
        for i in range(0, len(self.const_values) - 1):
            res_list.append((i + 1, _(str(self.const_values[i]) + '~' + str(self.const_values[i + 1]))))
        res_list.append((len(self.const_values) + 1, _('>' + str(self.const_values[-1]))))
        return tuple(res_list)

    def queryset(self, request, queryset):
        more = self.parameter_name + '__gte'
        less = self.parameter_name + '__lte'
        if self.value():
            cur_value = int(self.value())
            if cur_value == 0:
                return queryset.filter(**{less: self.const_values[0]})
            elif cur_value == len(self.const_values) + 1:
                return queryset.filter(**{more: self.const_values[-1]})
            else:
                return queryset.filter(**{more: self.const_values[cur_value - 1], less: self.const_values[cur_value]})
