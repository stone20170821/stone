#! encoding:utf-8

from datetime import date, datetime


common_date_format = '%Y-%m-%d'
basic_table_date_format = '%Y%m%d'


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