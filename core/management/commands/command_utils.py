#! encoding:utf-8

from datetime import date, datetime
from collections import Iterable

common_date_format = '%Y-%m-%d'
basic_table_date_format = '%Y%m%d'

date_format = "%Y_%m_%d_%H_%M_%S"

divider_h1 = "============================================================="
divider_h2 = "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
divider_h3 = "-------------------------------------------------------------"


def iterate_for_all(use_model, need_print=False):
    count = use_model.objects.count()

    i = 0
    cur_id = 1797702
    while i < count:
        if need_print:
            print i
            print cur_id

        try:
            obj = use_model.objects.get(pk=cur_id)
            i += 1
            yield obj
        except:
            pass
        cur_id -= 1


def max_index_and_value(values):
    """
    :param values:
    :type values:  Iterable
    :return:
    :rtype: tuple
    """
    return max(enumerate(values), key=lambda x: x[1])


def min_index_and_value(values):
    """
    :param values:
    :type values: Iterable
    :return:
    :rtype: tuple
    """
    return min(enumerate(values), key=lambda x: x[1])


def add_years(d, years):
    """
    :param d: 日期
    :type d: datetime
    :param years:
    :type years:
    :return:
    :rtype:
    """
    try:
        return d.replace(year=d.year + years)
    except ValueError:
        return d + (date(d.year + years, 1, 1) - date(d.year, 1, 1))
