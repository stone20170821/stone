#! encoding:utf-8

from datetime import date, datetime
from collections import Iterable

common_date_format = '%Y-%m-%d'
basic_table_date_format = '%Y%m%d'

divider_h1 = "============================================================="
divider_h2 = "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
divider_h3 = "-------------------------------------------------------------"


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
