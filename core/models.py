#! encoding:utf-8
from django.db import models


# Create your models here.

class TableName(object):
    # 基本信息
    horse_basic = 'horse_basic'
    horse_basic_backup = 'horse_basic_backup'

    # 大盘
    index_in_time = 'index_in_time'

    @staticmethod
    def k_data_default(code):
        return 'horse%s_k_data_default' % code


class ClassName(object):
    @staticmethod
    def k_data_default(code):
        return 'Horse%sKDataDefault' % code


class ModelDicts(object):
    k_data_default = dict()


class HorseBasicBase(models.Model):
    """
    基础表，HorseBasic和HorseBasicBackup同时继承这个
    Basic用来存放基本信息
    Backup用来备份，会存每一次download Basic的信息
    """
    code = models.CharField(max_length=10, verbose_name=u'代码')
    name = models.CharField(max_length=20, verbose_name=u'名称')
    industry = models.CharField(max_length=50, verbose_name=u'所属行业')
    area = models.CharField(max_length=50, default=u'未知', null=True, verbose_name=u'地区')
    pe = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'市盈率')
    outstanding = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'流通股本（亿）')
    totals = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'总股本（亿）')
    totalAssets = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'总资产（万）')
    liquidAssets = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'流动资产')
    fixedAssets = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'固定资产')
    reserved = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'公积金')
    reservedPerShare = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'每股公积金')
    esp = models.DecimalField(max_digits=7, decimal_places=4, verbose_name=u'每股收益')
    bvps = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'每股净资')
    pb = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'市净率')
    timeToMarket = models.BigIntegerField(verbose_name=u'上市日期')
    undp = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'未分利润')
    perundp = models.DecimalField(max_digits=7, decimal_places=4, verbose_name=u'每股未分')
    rev = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'收入同比（%）')
    profit = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'利润同比（%）')
    gpr = models.DecimalField(max_digits=7, decimal_places=4, verbose_name=u'毛利率（%）')
    npr = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u'净利润率（%）')
    holders = models.BigIntegerField(verbose_name=u'股东人数')

    def __str__(self):
        return self.code + u' ' + self.name

    class Meta:
        abstract = True


class HorseBasic(HorseBasicBase):
    """
    真正的基本信息表
    """

    class Meta:
        verbose_name = u'股票基本信息列表'
        db_table = TableName.horse_basic


class HorseBasicBackup(HorseBasicBase):
    """
    基本信息的每次修改都会备份到这里
    """

    class Meta:
        verbose_name = u'股票基本信息列表备份'
        db_table = TableName.horse_basic_backup


class IndexInTimeList(models.Model):
    """
    大盘指数的名称列表，实际上是实时的大盘列表数据，不过暂时只想用到名称，所以不做不同时段的维护
    """
    code = models.CharField(max_length=10, verbose_name=u'代码')
    name = models.CharField(max_length=20, verbose_name=u'名称')
    change = models.DecimalField(max_digits=7, decimal_places=4, verbose_name=u'涨跌幅')
    open = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u'开盘点位')
    preclose = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u'昨日收盘')
    close = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u'收盘点位')
    high = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u'最高点位')
    low = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u'最低点位')
    volume = models.BigIntegerField(verbose_name=u'成交量（手）')
    amount = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'成交金额（亿元）')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = u'大盘指数实时'
        db_table = TableName.index_in_time


class HorseKDataBase(models.Model):
    """
    get_k_data返回的基类
    """
    date = models.DateTimeField(verbose_name=u'日期和时间')
    open = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u'开盘价')
    close = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u'收盘价')
    high = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u'最高价')
    low = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u'最低价')
    volume = models.DecimalField(max_digits=16, decimal_places=4, verbose_name=u'成交量')
    code = models.CharField(max_length=10, verbose_name=u'代码')

    def __str__(self):
        return str(self.date)

    class Meta:
        abstract = True


def create_h_data_default_models():
    """
    创建k_data的default（qfq）的models
    """
    codes = HorseBasic.objects.values_list('code').all()
    for code_tuple in codes:
        code = str(code_tuple[0])
        class_name = ClassName.k_data_default(code)
        table_name = TableName.k_data_default(code)
        verbose_name = 'HorseKData' + str(code)
        class_type = type(
            class_name,
            (HorseKDataBase,),
            dict(
                __module__=HorseKDataBase.__module__,
                Meta=type(
                    'Meta',
                    (),
                    dict(
                        db_table=table_name,
                        verbose_name=verbose_name,
                    ),
                )
            ),
        )
        ModelDicts.k_data_default[code] = class_type

create_h_data_default_models()
