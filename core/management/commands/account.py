# coding: utf-8

import datetime
import functools32
import pandas as pd
from core.model_utils import get_all_codes_from_models
from conn_utils import read_dataframe_from_sql
from core.models import TableName


@functools32.lru_cache
def get_horse_frame():
    pass


def read_code(code, index=False):
    print 'read {} index = {}'.format(code, index)

    table_name = TableName.k_data_default(code) if not index else TableName.k_data_default_index(code)
    return read_dataframe_from_sql(table_name, index_col='date').ix[:, ['close', 'open']]
    # return read_dataframe_from_sql(table_name, index_col='date') \
    #     .drop('id', axis=1) \
    #     .drop('high', axis=1) \
    #     .drop('low', axis=1) \
    #     .drop('code', axis=1)s


class InfoPool(object):
    """
    LRU cache的方式提供horse的信息
    提供各种可能用到的信息，比如ma，macd，boll等
    基于日期提供
    """

    def __init__(self, lazy=True):
        super(InfoPool, self).__init__()
        self.lazy = lazy

        self.src = dict()
        """:type: dict[str, pd.DataFrame]"""

        if not self.lazy:
            need_index = ['000001', '399001']
            for code in need_index:
                self.src[self.parse_horse_name(code, True)] = read_code(code, True)

            codes = get_all_codes_from_models()
            for code in codes:
                self.src[code] = read_code(code)

    def price(self, date, horse_name, index=False, column="close"):
        df = self.get_horse_frame(horse_name, index)
        return df.loc[date][column]

    def get_horse_frame(self, code, index=False):
        """
        :param code: 
        :type code: 
        :param index: 
        :type index: 
        :return: 
        :rtype: pd.DataFrame 
        """
        name = self.parse_horse_name(code, index)
        if name not in self.src:
            self.src[name] = read_code(code, index)
        return self.src[name]

    def ma(self, date, horse_name, index=False, ma_length=20, column='close'):
        df = self.get_horse_frame(horse_name, index)
        print df.ix[:date, [column]].iloc[-ma_length:].mean()

    @staticmethod
    def parse_horse_name(horse_name, index):
        return horse_name if not index else horse_name + 'i'


class HorseOrder(object):
    BUY = "buy"
    SELL = "sell"

    __TAX_PERCENT = 0.003

    def __init__(self, opt, price, volume, date):
        super(HorseOrder, self).__init__()
        self.opt = opt
        self.price = price
        self.volume = volume
        self.date = date

    def __str__(self):
        return "opt: {}\tprice: {}\tvolume: {}\tdate: {}".format(
            self.opt, self.price, self.volume, self.date
        )

    def tax(self):
        """
        税直接收取千分之三
        """
        return self.price * self.volume * self.__TAX_PERCENT

    @staticmethod
    def pure_tax(opt, price, volume):
        return price * volume * HorseOrder.__TAX_PERCENT

    def receive(self):
        return self.price * self.volume - self.tax() if self.opt == self.BUY else 0

    def cost(self):
        return self.price & self.volume + self.tax() if self.opt == self.SELL else 0


class HoldHorse(object):
    """
    负责单只horse的买卖
    todo：T+1 不准确，只是单纯的比较时间差的天数，没考虑这些天是否是交易日
    """

    SELL_GAP = 1  # T+1

    def __init__(self, name):
        super(HoldHorse, self).__init__()
        # 原始数据(无法通过计算得到)
        self.name = name
        self.cur_date = None
        self.cur_price = -1.0
        self.unavail = dict()  # datetime: (price, volume)
        """:type: dict[datetime.datetime, tuple[float]]"""
        self.avail_volume = 0
        self.orders = list()
        """:type: list[Order]"""
        # 成本价格，永远等于当前持有horse的总价值/当前持有horse的总数量，不能用来计算收益(由于一部分已经卖出变现而不准确)
        self.cost_price = 0.0
        self.total_volume = 0
        # 在当前horse上变现的总钱数，每次buy会减少，每次sell会增加，第一次buy的金额就是 -price * volume
        self.win_money = 0.0

    def __str__(self):
        return "name:\t{}\ncur_date:\t{}\ncur_price:\t{}\nunavail:\t{}\navail_volume:\t{}" \
               "\norders:\n---\n{}\n---\ncost_price:\t{}\ntotal_volume:\t{}\nwin_money:\t{}\n".format(
            self.name, self.cur_date, self.cur_price, self.unavail, self.avail_volume, '\n'.join(map(lambda x: x.__str__(), self.orders)),
            self.cost_price, self.total_volume, self.win_money
        )

    def buy(self, price, volume, date):
        self.cur_date = date
        self.cur_price = price
        self.win_money -= price * volume

        # 成本价、总数
        self.cost_price = (self.cost_price * self.total_volume + price * volume) / (self.total_volume + volume)
        self.total_volume += volume

        # 当前购买进入unavail，然后计算最新的avail
        if date in self.unavail:
            avg_price = (self.unavail[date][0] * self.unavail[date][1] + price * volume) / (self.unavail[date][1] + volume)
            self.unavail[date] = (avg_price, self.unavail[date][1] + volume)
        else:
            self.unavail[date] = (price, volume)
        self._calculate_avail_and_cost_price()

        order = HorseOrder(HorseOrder.BUY, price, volume, date)
        self.orders.append(order)
        return order

    def enough_to_sell(self, date, volume):
        self.update_date(date)
        return self.avail_volume >= volume

    def sell(self, price, volume, date):
        self.cur_price = price
        self.cur_date = date
        self.win_money += price * volume

        # 更新avail
        self.update_date(date)
        self.avail_volume -= volume

        # 总数
        self.total_volume -= volume

        order = HorseOrder(HorseOrder.SELL, price, volume, date)
        self.orders.append(order)
        return order

    def total_hold_value(self):
        return self.cur_price * self.total_volume

    def update_price(self, price):
        self.cur_price = price

    def update_date(self, date):
        self.cur_date = date
        self._calculate_avail_and_cost_price()

    def _calculate_avail_and_cost_price(self):
        remove_date = list()
        for date in self.unavail.keys():
            p, v = self.unavail[date]

            if self.cur_date - date >= datetime.timedelta(days=self.SELL_GAP):
                remove_date.append(date)
                self.avail_volume += v

        for date in remove_date:
            del self.unavail[date]


class Account(object):
    """
    要进行的操作：
    基于仓位的买和卖，总值计算，收益计算
    """

    BUY_UNIT = 100  # 一手最少数量

    def __init__(self, start_fond=10000000.0):
        super(Account, self).__init__()
        self.start_fond = start_fond
        self.cur_fond = start_fond
        self.cur_holds = dict()
        """:type: dict[str, HoldHorse]"""
        self.orders = list()
        """:type: list[Order]"""

    def heartbeats(self, date, pool):
        """
        :param pool: 
        :type pool: 
        :param date: 
        :type date: 
        :return: 
        :rtype: 
        """
        pass

    def enough_to_buy(self, price, volume):
        return self.cur_fond >= price * volume + HorseOrder.pure_tax(HorseOrder.BUY, price, volume)

    def total_hold_value(self):
        total = self.cur_fond
        for name in self.cur_holds:
            total += self.cur_holds[name].total_hold_value()

        return total

    def buy(self, horse_name, price, volume, date):
        if horse_name not in self.cur_holds:
            self.cur_holds[horse_name] = HoldHorse(horse_name)

        order = self.cur_holds[horse_name].buy(price, volume, date)
        self.cur_fond -= order.cost()
        self.orders.append(order)

    def buy_account_percent(self, horse_name, price, date, percent):
        """
        :param horse_name: 
        :type horse_name: 
        :param price: 
        :type price: 
        :param date: 
        :type date: datetime.datetime
        :param percent: 百分比，以float的方式提供，比如0.2，代表20%
        :type percent: float
        :return: 
        :rtype: 
        """
        use_money = self.total_hold_value() * percent

        if self.cur_fond <= use_money:
            use_money = self.cur_fond

        buy_num = int(use_money / price)
        buy_num = buy_num - buy_num % self.BUY_UNIT

        if buy_num >= 0 and self.enough_to_buy(price, buy_num):
            self.buy(horse_name, price, buy_num, date)
            return True
        else:
            return False

    def enough_to_sell(self, horse_name, volume, date):
        return horse_name in self.cur_holds and self.cur_holds[horse_name].enough_to_sell(date, volume)

    def sell(self, horse_name, price, volume, date):
        order = self.cur_holds[horse_name].sell(price, volume, date)
        self.cur_fond += order.receive()
        self.orders.append(order)
