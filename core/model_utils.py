#! encoding: utf-8
from models import *


def get_all_codes_from_models(index=False):
    """
    从Basic表中返回所有的code
    :return:
    :rtype: list
    """
    code_model = HorseBasic
    if index:
        code_model = IndexInTimeList
    code_tuples = code_model.objects.values_list('code').order_by('code')
    return [str(code_tuple[0]) for code_tuple in code_tuples]


def get_model(code, index=False):
    if index:
        return ModelDicts.k_data_default_index[ClassName.k_data_default_index(code)]
    else:
        return ModelDicts.k_data_default[ClassName.k_data_default(code)]
