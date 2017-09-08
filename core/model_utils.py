#! encoding: utf-8
from models import *


def get_all_codes_from_basic():
    """
    从Basic表中返回所有的code
    :return:
    :rtype: list
    """
    code_tuples = HorseBasic.objects.values_list('code').order_by('code')
    return [str(code_tuple[0]) for code_tuple in code_tuples]
