# coding: utf-8

import datetime
import functools32
import json
import pandas as pd
import traceback
from core.model_utils import get_all_codes_from_models
from conn_utils import read_dataframe_from_sql
from core.models import TableName, BackResult
from back_result_divider import BackResultYearDivider
from order_analysis import OrderAnalysis
from horse_order import HorseOrder
from command_utils import date_format

# 计算price、avg、boll等值时的缓存数量
lru_cache_num = 5000


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

        self.macd_dict = dict()
        """:type: dict[str, dict[datetime.datetime, float]]"""

        if not self.lazy:
            need_index = ['000001', '399001']
            for code in need_index:
                self.src[self.parse_horse_name(code, True)] = read_code(code, True)

            codes = get_all_codes_from_models()
            for code in codes:
                self.src[code] = read_code(code)

    @functools32.lru_cache(lru_cache_num)
    def price(self, date, horse_name, index=False, column="close"):
        try:
            df = self.get_horse_frame(horse_name, index)
            return float(df.loc[date][column])
        except:
            # traceback.print_exc()
            print '{} date {} not exist'.format(horse_name, date)
            return None

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

    @functools32.lru_cache(lru_cache_num * 10)
    def average_line(self, date, horse_name, index=False, ma_length=20, column='close'):
        """
        天数不足ma_length，则取所有天数的平均值，例如，前4天的20日均线，值为4天平均值
        :param date: 
        :type date: 
        :param horse_name: 
        :type horse_name: 
        :param index: 
        :type index: 
        :param ma_length: 
        :type ma_length: 
        :param column: 
        :type column: 
        :return: 
        :rtype: 
        """
        df = self.get_horse_frame(horse_name, index)
        return df.ix[:date, [column]].iloc[-ma_length:].mean()[column]

    def boll(self, date, horse_name, index=False, ma_length=20, column='close', p=2):
        df = self.get_horse_frame(horse_name, index)
        window = df.ix[:date, [column]].iloc[-ma_length:]
        sta = window.std()[column]
        avg = self.average_line(date, horse_name, index, ma_length, column)
        return avg, avg + p * sta, avg - p * sta

    # def macd(self, date, horse_name, index=False, start=12, middle=9, end=26, column='close'):
    #     df = self.get_horse_frame(horse_name, index)
    #     window = df.ix[:date, [column]].iloc[-ma_length:]

    def macd(self, date, horse_name, index=False, x=12, y=26, column='close'):
        df = self.get_horse_frame(horse_name, index)
        horse_macd_key = self.parse_horse_name(horse_name, index)

        if horse_macd_key not in self.macd_dict:
            self.macd_dict[horse_macd_key] = dict()

            # last_ema_12 =

    @staticmethod
    def parse_horse_name(horse_name, index):
        return horse_name if not index else horse_name + 'i'



class HoldHorse(object):
    """
    负责单只horse的买卖
    todo：T+1 不准确，只是单纯的比较时间差的天数，没考虑这些天是否是交易日
    """

    SELL_GAP = 1  # T+1

    def __init__(self, name, index=False):
        super(HoldHorse, self).__init__()
        # 原始数据(无法通过计算得到)
        self.name = name
        self.index = index
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

    def current_hold_win_percent(self, price, date):
        """
        :param price: 
        :type price: 
        :param date: 
        :type date: 
        :return: 
        :rtype: float
        """
        self.update_price(price)
        self.update_date(date)

        return price / self.cost_price - 1

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

        order = HorseOrder(HorseOrder.BUY, price, volume, date, self.name, self.index)
        self.orders.append(order)
        return order

    def enough_to_sell(self, date, volume):
        self.update_date(date)
        return self.avail_volume >= volume

    def sell(self, price, volume, date):
        if self.enough_to_sell(date, volume):
            self.cur_price = price
            self.cur_date = date
            self.win_money += price * volume

            # 更新avail
            self.update_date(date)
            self.avail_volume -= volume

            # 总数
            self.total_volume -= volume

            order = HorseOrder(HorseOrder.SELL, price, volume, date, self.name, self.index)
            self.orders.append(order)
            return order
        else:
            return None

    def sell_all(self, price, date):
        self.update_date(date)
        if self.avail_volume >= 0:
            return self.sell(price, self.avail_volume, date)
        return None

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
    CONSIDER_INDEX = ('000001', '399001', '000300', '399005', '000905')

    def __init__(self, pool,
                 start_fond=10000000.0,
                 target_horse='000001', target_is_index=True,
                 base_line_horse='000001', base_line_is_index=True,
                 start_date='20100105'):
        super(Account, self).__init__()
        self.pool = pool
        """:type: InfoPool"""
        self.start_fond = start_fond
        self.cur_fond = start_fond
        self.cur_holds = dict()
        """:type: dict[str, HoldHorse]"""
        self.orders = list()
        """:type: list[HorseOrder]"""
        self.axis = dict()
        """:type: dict[str, list]"""

        self.base_line_horse = base_line_horse
        self.base_line_is_index = base_line_is_index

        self.hold_axis = list()
        self.axis['hold'] = self.hold_axis

        self.index_axis = list()
        self.axis['index'] = self.index_axis

        self.target_horse = target_horse
        self.target_is_index = target_is_index

        self.start_date = start_date

        # 获取target和index的值，如果target就是index，只存index
        self.base_index_frame = self.pool.get_horse_frame(self.base_line_horse, self.base_line_is_index)

        # 找到base_line的2010年后的第一个日期
        real_start_date = start_date
        it_d = start_date
        for i in range(0, 50000):
            it_dd = (datetime.datetime.strptime(it_d, '%Y%m%d') + datetime.timedelta(days=i)).strftime('%Y%m%d')
            if it_dd in self.base_index_frame.index:
                real_start_date = it_dd
                break

        self.start_date = real_start_date

        self.base_index_start_value = self.pool.price(self.start_date, self.base_line_horse, self.base_line_is_index)
        self.cur_base_index_price = self.base_index_start_value

        if self.need_consider_target():
            self.target_frame = self.pool.get_horse_frame(self.target_horse, self.target_is_index)
            self.target_start_value = self.pool.price(self.start_date, self.target_horse, self.target_is_index)
            self.cur_target_price = self.target_start_value

            self.target_axis = list()
            self.axis['target'] = self.target_axis

        self.date_axis_origin = self.base_index_frame.ix[self.start_date:, ['close']].index
        self.date_str_axis = list()
        self.axis['date'] = self.date_str_axis
        # self.axis['date'] = [d.strftime(date_format) for d in self.date_axis_origin]

        # 计算md专用
        self.cur_max_down = 0
        self.cur_max_value = -1
        self.max_down_start = None
        self.max_down_end = None
        self.saved_max_down_start = None

    def __str__(self):
        return "cur_fond:\t{}\ncur_holds:\n---\n{}\n---\norders:\n---\n{}\n---\n".format(
            self.cur_fond, '\n'.join(map(lambda x: x + '\n' + self.cur_holds[x].__str__(), self.cur_holds)), '\n'.join(map(lambda x: x.__str__(), self.orders))
        )

    def before_heartbeats(self, date):
        # 更新hold的价值
        for name in self.cur_holds:
            hold = self.cur_holds[name]
            hold.update_date(date)
            p = self.pool.price(date, hold.name, hold.index)
            # 持有中任意不存在，忽略这个date
            if p is None:
                return False
            hold.update_price(p)

        # 获取index和target的值
        self.cur_base_index_price = self.pool.price(date, self.base_line_horse, self.base_line_is_index)
        if self.need_consider_target():
            self.cur_target_price = self.pool.price(date, self.target_horse, self.target_is_index)

            if self.cur_target_price is None:
                return False

        return True

    def current_target_or_index_price(self):
        if self.need_consider_target():
            return self.cur_target_price
        else:
            return self.cur_base_index_price

    def heartbeats(self, date):
        """
        :param pool: 
        :type pool: InfoPool
        :param date: 
        :type date: 
        :return: 
        :rtype: 
        """
        pass

    def after_heartbeats(self, date):
        """
        :param date: 
        :type date: datetime.datetime 
        """
        # 值放入axis
        # 日期也会在此时放入，因为有可能target在指定date并没有price，这些date会被丢弃，这个逻辑在before中过滤
        self.index_axis.append(self.cur_base_index_price / self.base_index_start_value)
        self.date_str_axis.append(date.strftime(date_format))
        if self.need_consider_target():
            self.target_axis.append(self.cur_target_price / self.target_start_value)

        self.hold_axis.append(self.total_hold_value() / self.start_fond)

        # 年份变化时，分年保存结果

        # 计算md
        p = self.hold_axis[-1]
        if p > self.cur_max_value:
            self.cur_max_value = p
            self.saved_max_down_start = date

        my_max_down = (self.cur_max_value - p) / self.cur_max_value
        if my_max_down > self.cur_max_down:
            self.cur_max_down = my_max_down
            self.max_down_start = self.saved_max_down_start
            self.max_down_end = date

    @staticmethod
    def code_to_string(code, is_index):
        res = code
        if is_index:
            return res + '_0'
        else:
            return res + '_1'

    def done_this_round(self):
        index_win = self.index_axis[-1] - 1
        final_win = self.final_win_percent()

        # 保存整体结果
        back_result = BackResult()
        back_result.base_line_result = index_win
        back_result.base_line_code = self.code_to_string(self.base_line_horse, self.base_line_is_index)

        if self.need_consider_target():
            back_result.use_code = self.code_to_string(self.target_horse, self.target_is_index)
            back_result.use_code_result = self.target_axis[-1] - 1
        else:
            back_result.use_code = self.code_to_string(self.base_line_horse, self.base_line_is_index)
            back_result.use_code_result = index_win

        back_result.final_win = final_win
        back_result.win_records = json.dumps(self.axis)
        back_result.date_start = self.date_axis_origin[0]
        back_result.date_end = self.date_axis_origin[-1]
        back_result.run_time = datetime.datetime.now()
        back_result.algorithm_category = self.algorithm_category()
        back_result.algorithm_desc = self.algorithm_desc()
        back_result.param_string = self.param_string()
        back_result.max_down = self.cur_max_down
        back_result.max_down_start = self.max_down_start if self.max_down_start else datetime.datetime.today()
        back_result.max_down_end = self.max_down_end if self.max_down_end else datetime.datetime.today()
        back_result.orders = "**".join([order.to_json_string() for order in self.orders])

        order_ana = OrderAnalysis(self.orders)
        order_ana.calculate()
        back_result.buy_sell_success_rate = order_ana.buy_sell_success_rate
        back_result.total_hold_day_count = order_ana.total_hold_day_count
        back_result.avg_hold_day_count = order_ana.avg_hold_day_count
        back_result.buy_count = order_ana.buy_count
        back_result.sell_count = order_ana.sell_count
        back_result.up_list = ','.join([str(up) for up in order_ana.up_list])

        back_result.save()

        BackResultYearDivider(back_result, self.orders).divide()

    def enough_to_buy(self, price, volume):
        # print 'enough_to_buy: {} {} {} {}'.format(self.cur_fond, price, volume, HorseOrder.pure_tax(HorseOrder.BUY, price, volume))
        return self.cur_fond >= price * volume + HorseOrder.pure_tax(HorseOrder.BUY, price, volume)

    def repo_percent(self):
        """
        仓位
        :return: 
        :rtype: float 
        """
        return 1 - self.cur_fond / self.total_hold_value()

    def final_win_percent(self):
        """
        最终盈利
        :return: 
        :rtype: 
        """
        return self.total_hold_value() / self.start_fond - 1

    def total_hold_value(self):
        total = self.cur_fond
        for name in self.cur_holds:
            hold = self.cur_holds[name]
            total += hold.total_hold_value()

        return total

    def buy(self, horse_name, price, volume, date, index=False):
        if self.enough_to_buy(price, volume):
            if horse_name not in self.cur_holds:
                self.cur_holds[horse_name] = HoldHorse(horse_name, index)

            order = self.cur_holds[horse_name].buy(price, volume, date)
            self.cur_fond -= order.cost()
            self.orders.append(order)
            return True
        return False

    def buy_account_percent(self, horse_name, price, date, percent, index=False):
        """
        :param index: 
        :type index: 
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

        while buy_num > 0 and not self.enough_to_buy(price, buy_num):
            buy_num -= self.BUY_UNIT

        if buy_num > 0 and self.enough_to_buy(price, buy_num):
            if self.buy(horse_name, price, buy_num, date, index):
                return buy_num

        return -1

    def enough_to_sell(self, horse_name, volume, date):
        return horse_name in self.cur_holds and self.cur_holds[horse_name].enough_to_sell(date, volume)

    def sell(self, horse_name, price, volume, date):
        if self.enough_to_sell(horse_name, volume, date):
            order = self.cur_holds[horse_name].sell(price, volume, date)
            self.cur_fond += order.receive()
            self.orders.append(order)
            # print 'after sell fond is: ' + str(self.cur_fond)
            return True
        return False

    def sell_all(self, horse_name, price, date):
        if horse_name in self.cur_holds:
            order = self.cur_holds[horse_name].sell_all(price, date)
            self.cur_fond += order.receive()
            self.orders.append(order)
            return True
        return False

    def need_consider_target(self):
        return not (self.base_line_horse == self.target_horse and self.base_line_is_index == self.target_is_index)

    def param_string(self):
        """
        避免换行
        :return: 
        :rtype: 
        """
        return ""

    def algorithm_category(self):
        """
        避免换行
        :return: 
        :rtype: 
        """
        return ""

    def algorithm_desc(self):
        """
        避免换行
        :return: 
        :rtype: 
        """
        return ""
