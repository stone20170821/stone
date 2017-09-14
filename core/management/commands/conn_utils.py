#! encoding:utf-8

from django.conf import settings
from sqlalchemy import create_engine
from pandas import DataFrame, read_sql, read_sql_table
from django.db import models

user = settings.DATABASES['default']['USER']
password = settings.DATABASES['default']['PASSWORD']
database_name = settings.DATABASES['default']['NAME']

database_url = 'postgresql://{user}:{password}@localhost:5432/{database_name}'.format(
    user=user,
    password=password,
    database_name=database_name
)
engine = create_engine(database_url, echo=False)


def write_dataframe_to_sql(df, table_name, if_exists='append', index=True):
    """
    :param index: index是否作为单独的一列保存
    :param if_exists:
    :param df:
    :type df: DataFrame
    :param table_name:
    :return:
    """
    df.to_sql(table_name, engine, if_exists=if_exists, index=index)


def read_dataframe_from_sql(table_name, index_col=None):
    """
    :param index_col:
    :type index_col: str
    :param table_name:
    :type table_name: str
    :return:
    :rtype: DataFrame
    """
    return read_sql_table(table_name, engine, index_col=index_col)


def backup_table_to_table(source, target):
    """
    :param source: table name
    :type source: str
    :param target: target table name
    :type target: str
    """
    df = read_sql(source, engine)
    write_dataframe_to_sql(df, target, index=False)


def clean_table(remove_model):
    """
    :param remove_model:
    :type remove_model: models.Model
    """
    remove_model.objects.all().delete()
