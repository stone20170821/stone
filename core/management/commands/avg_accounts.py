# coding:utf-8

from account import Account


class MAStartAccount(Account):
    """
    基于均线操作，上升超过ma_length日均线买入，下降低于ma_length均线卖出
    """

    def __init__(self, ma_length=20, start_fond=10000000.0):
        super(MAStartAccount, self).__init__(start_fond)

        self.ma_length = ma_length
        self.target_axis = list()
        self.axis['hold'] = self.target_axis
        self.ma_vs = list()
        self.axis[str(ma_length)] = self.ma_vs
        self.start_value = None

    def heartbeats(self, date, pool):
        target_horse = '000001'
        is_index = True

        avg = pool.average_line(date, target_horse, index=is_index, ma_length=self.ma_length)
        cur = pool.price(date, target_horse, index=is_index)

        if self.start_value is None:
            self.start_value = cur

        if cur > avg:
            self.buy_account_percent(target_horse, cur, date, 1, is_index)
        else:
            self.sell_all(target_horse, cur, date)

        self.target_axis.append(self.total_hold_value() / self.start_fond)
        self.ma_vs.append(avg / self.start_value)

    def param_string(self):
        return "ma_length: {}".format(self.ma_length)

    def algorithm_category(self):
        return "ma"

    def algorithm_desc(self):
        return "simple_ma"


class MARepoShareAccount(Account):
    """
    基于均线，不同均线对应不同仓位
    """

    def __init__(self, ma_list, start_fond=10000000.0):
        super(MARepoShareAccount, self).__init__(start_fond)
        self.ma_list = ma_list

        self.target_axis = list()
        self.axis['hold'] = self.target_axis

        self.target_horse = '000001'
        self.target_is_index = True

        self.ma_list_length = len(self.ma_list)

        # 原本是否大于均线的值
        self.ma_compare_list = [False for x in ma_list]
        # 每个均线对应的买入量
        self.buy_ma_list = [0 for x in ma_list]

        # 均线基准
        for x in self.ma_list:
            self.axis[str(x)] = list()

        # 每次买入的百分比
        self.divider = 1.0 / float(self.ma_list_length)

        self.start_value = None

    def heartbeats(self, date, pool):
        super(MARepoShareAccount, self).heartbeats(date, pool)

        ma_value_list = [pool.average_line(date, self.target_horse, index=self.target_is_index, ma_length=x)
                         for x in self.ma_list]

        cur = pool.price(date, self.target_horse, index=self.target_is_index)

        # print date
        # print cur

        if self.start_value is None:
            self.start_value = cur

        for i in range(0, self.ma_list_length):
            ma_value = ma_value_list[i]
            origin_compare = self.ma_compare_list[i]

            if cur > ma_value:
                if not origin_compare:
                    count = self.buy_account_percent(self.target_horse, cur, date, self.divider, self.target_is_index)
                    if count > 0:
                        self.buy_ma_list[i] = count

                self.ma_compare_list[i] = True
            else:
                if cur < ma_value:
                    if self.buy_ma_list[i] > 0:

                        if self.sell(self.target_horse, cur, self.buy_ma_list[i], date):
                            self.buy_ma_list[i] = 0
                self.ma_compare_list[i] = False

        self.target_axis.append(self.total_hold_value() / self.start_fond)
        for i in range(0, self.ma_list_length):
            m = self.ma_list[i]
            v = ma_value_list[i]
            self.axis[str(m)].append(v / self.start_value)

    def param_string(self):
        return "ma_list:" + " ".join(str(x) for x in self.ma_list)

    def algorithm_category(self):
        return "ma"

    def algorithm_desc(self):
        return "ma_list"

    @staticmethod
    def generator():
        # ss = [20, ]
        # es = [30, ]
        # ns = [60, ]
        # for s in ss:
        #     for e in es:
        #         for n in ns:
        #             # yield MARepoShareAccount([s, e, n])
        #             yield MARepoShareAccount([s, ])
        # yield MARepoShareAccount([20, 30, 60])

        # 单均线
        ds = range(5, 200, 5)
        for d in ds:
            yield MARepoShareAccount([d, ])

        # 双均线
            # s1 = range(5, 50, 5)
            # s2 = range(10, 100, 10)
            #
            # for a in s1:
            #     for b in s2:
            #         yield MARepoShareAccount([a, b, ])


class MASaveProfitAccount(Account):
    """
    基于均线操作，有盈利后，最小盈利0，n（阈值），2n，m（最大上升）/2
    """

    def __init__(self, ma_s=20, ma_e=20, n=0.1, start_fond=10000000.0):
        super(MASaveProfitAccount, self).__init__(start_fond)

        self.target_axis = list()
        self.axis['hold'] = self.target_axis

        self.target_horse = '000001'
        self.target_is_index = True

        self.pre_large_than_s = False
        self.pre_large_than_e = False
        self.large_than_s = False
        self.large_than_e = False

        self.ma_s = ma_s
        self.ma_e = ma_e

        self.n = n
        self.max_win_percent = 0.0

    def heartbeats(self, date, pool):
        super(MASaveProfitAccount, self).heartbeats(date, pool)

        avg_s = pool.average_line(date, self.target_horse, index=self.target_is_index, ma_length=self.ma_s)
        avg_e = pool.average_line(date, self.target_horse, index=self.target_is_index, ma_length=self.ma_e)
        cur = pool.price(date, self.target_horse, index=self.target_is_index)

        self.pre_large_than_s = self.large_than_s
        self.pre_large_than_e = self.large_than_e

        self.large_than_s = cur > avg_s
        self.large_than_e = cur > avg_e

        if self.repo_percent() > 0.8:
            if (self.pre_large_than_s and not self.large_than_s) or \
                    (self.pre_large_than_e and not self.large_than_e) \
                    or (not self.large_than_s and not self.large_than_e):
                # 卖点：止损
                self.sell_all(self.target_horse, cur, date)
            elif self.large_than_s and self.large_than_e:
                # 卖点：锁定盈利
                win_percent = self.cur_holds[self.target_horse].current_hold_win_percent(cur, date)

                if self.max_win_percent > self.n * 2:
                    if win_percent < self.max_win_percent / 2:
                        self.sell_all(self.target_horse, cur, date)

                elif self.max_win_percent > self.n:
                    if win_percent < self.n:
                        self.sell_all(self.target_horse, cur, date)

                if win_percent > self.max_win_percent:
                    self.max_win_percent = win_percent

        else:
            if not self.pre_large_than_s and self.large_than_s:
                # 买点

                self.buy_account_percent(self.target_horse, cur, date, 1, True)
                self.max_win_percent = 0.0

        self.target_axis.append(self.total_hold_value() / self.start_fond)

    @staticmethod
    def output_dir_name():
        return "ma_save_profit"

    def fig_filename(self):
        return "ma_save_profit_{}_{}_{}".format(self.ma_s, self.ma_e, int(self.n * 100))

    def param_string(self):
        return "ma_s: {}\tma_e:{}\tn:{}".format(self.ma_s, self.ma_e, self.n)

    @staticmethod
    def generator():
        ss = range(5, 100, 5)
        es = range(5, 100, 5)
        ns = range(2, 20, 2)
        for s in ss:
            for e in es:
                for n in ns:
                    yield MASaveProfitAccount(s, e, float(n) / 100)


class MACrossAccount(Account):
    def __init__(self, ma_list, start_fond=10000000.0):
        super(MACrossAccount, self).__init__(start_fond)
        self.ma_list = ma_list

    def heartbeats(self, date, pool):
        super(MACrossAccount, self).heartbeats(date, pool)

    def param_string(self):
        return "ma_cross_list: " + " ".join(str(x) for x in self.ma_list)

    def algorithm_category(self):
        return "ma"

    def algorithm_desc(self):
        return "ma_cross"
