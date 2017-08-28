#! encoding:utf-8
from django.db import models


# Create your models here.

class TableName(object):
    horse_basic = 'horse_basic'
    horse_basic_backup = 'horse_basic_backup'


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
