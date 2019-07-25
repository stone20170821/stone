#! encoding:utf-8
from django.db import models


# Create your models here.

class TableName(object):
    # 基本信息
    horse_basic = 'horse_basic'
    horse_basic_backup = 'horse_basic_backup'

    # 大盘
    index_in_time = 'index_in_time'

    # 回测结果
    back_result = 'back_result'

    @staticmethod
    def k_data_default(code):
        return 'horse%s_k_data_default' % code

    @staticmethod
    def k_data_default_index(code):
        return 'index%s_k_data_default' % code


class ClassName(object):
    @staticmethod
    def k_data_default_index(code):
        return 'Index%sKDataDefault' % code

    @staticmethod
    def k_data_default(code):
        return 'Horse%sKDataDefault' % code


class ModelDicts(object):
    """
    "classname": modelObject
    """
    k_data_default = dict()
    k_data_default_index = dict()


class BackResult(models.Model):
    base_line_result = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'基准线收益')
    base_line_code = models.CharField(max_length=10, verbose_name=u'基准线代码')
    use_code = models.CharField(max_length=10, verbose_name=u'回测使用')
    use_code_result = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'使用代码原本收益')
    final_win = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'收益')
    back_codes = models.TextField(verbose_name=u'回测样本使用HORSE')  # deprecated, 改用json形式，存在win_records中，回测用到的样本，配合收益情况记录，可以直接生成图
    win_records = models.TextField(verbose_name=u'收益情况记录')
    date_start = models.DateTimeField(verbose_name=u'起始时间')
    date_end = models.DateTimeField(verbose_name=u'终止时间')
    run_time = models.DateTimeField(verbose_name=u'执行时间')
    algorithm_category = models.CharField(max_length=100, verbose_name=u'算法分类')
    algorithm_desc = models.CharField(max_length=100, verbose_name=u'算法描述')
    param_string = models.CharField(max_length=888, verbose_name=u'算法参数')
    max_down = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u'最大回撤')
    max_down_start = models.DateTimeField(verbose_name=u'最大回撤起始')
    max_down_end = models.DateTimeField(verbose_name=u'最大回撤结束')
    orders = models.TextField(verbose_name=u'订单记录')
    buy_sell_success_rate = models.DecimalField(max_digits=5, decimal_places=4, verbose_name=u'信号成功率')
    total_hold_day_count = models.IntegerField(verbose_name=u'持有天数')
    avg_hold_day_count = models.DecimalField(max_digits=9, decimal_places=4, verbose_name=u'平均持有天数')
    buy_count = models.IntegerField(verbose_name=u'买入次数')
    sell_count = models.IntegerField(verbose_name=u'卖出次数')
    up_list = models.TextField(verbose_name=u'买卖单次收益')

    def __unicode__(self):
        return self.param_string

    class Meta:
        # verbose_name = u'回测结果'
        db_table = TableName.back_result


class BackResultYear(models.Model):
    base_line_result = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'基准线收益')
    base_line_code = models.CharField(max_length=10, verbose_name=u'基准线代码')
    use_code = models.CharField(max_length=10, verbose_name=u'回测使用')
    use_code_result = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'使用代码原本收益')
    final_win = models.DecimalField(max_digits=14, decimal_places=4, verbose_name=u'收益')
    back_codes = models.TextField(verbose_name=u'回测样本使用HORSE')  # deprecated, 改用json形式，存在win_records中，回测用到的样本，配合收益情况记录，可以直接生成图
    win_records = models.TextField(verbose_name=u'收益情况记录')
    date_start = models.DateTimeField(verbose_name=u'起始时间')
    date_end = models.DateTimeField(verbose_name=u'终止时间')
    run_time = models.DateTimeField(verbose_name=u'执行时间')
    algorithm_category = models.CharField(max_length=100, verbose_name=u'算法分类')
    algorithm_desc = models.CharField(max_length=100, verbose_name=u'算法描述')
    param_string = models.CharField(max_length=888, verbose_name=u'算法参数')
    max_down = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=u'最大回撤')
    max_down_start = models.DateTimeField(verbose_name=u'最大回撤起始')
    max_down_end = models.DateTimeField(verbose_name=u'最大回撤结束')
    orders = models.TextField(verbose_name=u'订单记录')
    buy_sell_success_rate = models.DecimalField(max_digits=5, decimal_places=4, verbose_name=u'信号成功率')
    total_hold_day_count = models.IntegerField(verbose_name=u'持有天数')
    avg_hold_day_count = models.DecimalField(max_digits=9, decimal_places=4, verbose_name=u'平均持有天数')
    buy_count = models.IntegerField(verbose_name=u'买入次数')
    sell_count = models.IntegerField(verbose_name=u'卖出次数')
    up_list = models.TextField(verbose_name=u'买卖单次收益')

    from_result = models.ForeignKey(BackResult)
    use_year = models.IntegerField(verbose_name=u'年份')


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

    def __unicode__(self):
        return self.code + ' ' + self.name

    class Meta:
        abstract = True


class CfsDongfangcaijing(models.Model):
    code = models.CharField(max_length=10, verbose_name=u'代码')
    n_cashflow_act = models.DecimalField(max_digits=18, decimal_places=4, verbose_name=u'经营活动产生的现金流量净额')
    report_date = models.BigIntegerField(verbose_name=u'报告日期')


class HorseBasicSnow(models.Model):
    code = models.CharField(max_length=10, verbose_name=u'代码')
    symbol = models.CharField(max_length=12, verbose_name=u'代码')
    high52w = models.DecimalField(max_digits=5, decimal_places=4, verbose_name=u'52周最高')


class HorseBasic(HorseBasicBase):
    """
    真正的基本信息表
    """

    class Meta:
        # verbose_name = u'股票基本信息列表'
        db_table = TableName.horse_basic


class HorseBasicBackup(HorseBasicBase):
    """
    基本信息的每次修改都会备份到这里
    """

    class Meta:
        # verbose_name = u'股票基本信息列表备份'
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

    def __unicode__(self):
        return self.name

    class Meta:
        # verbose_name = u'大盘指数实时'
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

    def __unicode__(self):
        return str(self.date)

    class Meta:
        abstract = True


def create_k_data_default_models(is_index=False):
    """
    创建k_data的default（qfq）的models
    """
    codes = HorseBasic.objects.values_list('code').all()
    if is_index:
        codes = IndexInTimeList.objects.values_list('code').all()
    for code_tuple in codes:
        code = str(code_tuple[0])
        class_name = ClassName.k_data_default(code)
        table_name = TableName.k_data_default(code)
        verbose_name = 'HorseKData' + str(code)

        if is_index:
            class_name = ClassName.k_data_default_index(code)
            table_name = TableName.k_data_default_index(code)
            verbose_name = 'IndexKData' + str(code)

        class_type = type(
            class_name,
            (HorseKDataBase,),
            dict(
                is_index=is_index,
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
        if not is_index:
            ModelDicts.k_data_default[class_name] = class_type
        else:
            ModelDicts.k_data_default_index[class_name] = class_type


create_k_data_default_models()
create_k_data_default_models(True)
