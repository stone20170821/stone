# coding:utf-8

from account import Account
from core.models import BackResult


class MAStartAccount(Account):
    """
    基于均线操作，上升超过ma_length日均线买入，下降低于ma_length均线卖出
    
    single run time: 600519 5.67s
    """

    def __init__(self, pool, ma_length=20, start_fond=10000000.0, target_horse='000001', target_is_index=True, base_line_horse='000001', base_line_is_index=True,
                 start_date='20100105'):
        super(MAStartAccount, self).__init__(pool, start_fond, target_horse, target_is_index, base_line_horse, base_line_is_index, start_date)

        self.ma_length = ma_length
        self.ma_vs = list()
        self.axis[str(ma_length)] = self.ma_vs

    def heartbeats(self, date):
        avg = self.pool.average_line(date, self.base_line_horse, index=self.base_line_is_index, ma_length=self.ma_length)
        cur_index = self.pool.price(date, self.base_line_horse, index=self.base_line_horse)
        cur_target = self.pool.price(date, self.target_horse, index=self.target_is_index)

        if cur_index > avg:
            self.buy_account_percent(self.target_horse, cur_target, date, 1, self.target_is_index)
        else:
            self.sell_all(self.target_horse, cur_target, date)

        self.ma_vs.append(avg / self.base_index_start_value)

    def param_string(self):
        return "ma_length: {}".format(self.ma_length)

    def algorithm_category(self):
        return "ma"

    def algorithm_desc(self):
        return "simple_ma"

    @staticmethod
    def generator(pool):
        """
        all index: (10, 400)
        600519: all index: (10, 400)
        :param pool: 
        :type pool: 
        :return: 
        :rtype: 
        """
        # for m in range(10, 400):
        #     yield MAStartAccount(pool, ma_length=m,
        #                          base_line_horse='000300', base_line_is_index=True,
        #                          target_horse='000300', target_is_index=True)
        #
        # for m in range(10, 400):
        #     yield MAStartAccount(pool, ma_length=m,
        #                          base_line_horse='399006', base_line_is_index=True,
        #                          target_horse='399006', target_is_index=True)

        for m in range(10, 400):
            for i in Account.CONSIDER_INDEX:
                yield MAStartAccount(pool, ma_length=m,
                                     base_line_horse=i, base_line_is_index=True,
                                     target_horse='600519', target_is_index=False)

                # for m in range(10, 400):
                #     yield MAStartAccount(pool, ma_length=m,
                #                          base_line_horse='000905', base_line_is_index=True,
                #                          target_horse='000905', target_is_index=True)


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
            # print '________________________'
            # print date

            if cur > ma_value:
                # print 'up'
                # print 'origin compare: ' + str(origin_compare)
                if not origin_compare:
                    count = self.buy_account_percent(self.target_horse, cur, date, self.divider, self.target_is_index)
                    # print 'buy count: ' + str(count)
                    if count > 0:
                        self.buy_ma_list[i] = count

                self.ma_compare_list[i] = True
            else:
                if cur < ma_value:
                    # print 'down'
                    if self.buy_ma_list[i] > 0:
                        # print 'try sell'
                        if self.sell(self.target_horse, cur, self.buy_ma_list[i], date):
                            # print 'sell success'
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
        # ds = range(5, 200, 5)
        # for d in ds:
        #     yield MARepoShareAccount([d, ])

        # 测试
        yield MARepoShareAccount([64, 244, ])

        # 双均线
        # s1 = range(5, 300, 5)
        # s2 = range(5, 300, 5)
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
    """
    enter_start > enter_end: enter
    leave_start < leave_end: leave
    :param ma_tuple: (enter_start, enter_end, leave_start, leave_end) 
    :type ma_tuple: tuple
    :param start_fond: 
    :type start_fond: 
    """

    def __init__(self, pool, ma_tuple, start_fond=10000000.0, target_horse='000001', target_is_index=True, base_line_horse='000001', base_line_is_index=True,
                 start_date='20100105'):
        super(MACrossAccount, self).__init__(pool, start_fond, target_horse, target_is_index, base_line_horse, base_line_is_index, start_date)

        self.ma_tuple = ma_tuple

        self.cur_ma_price = list()
        self.is_holding = False

        ma_set = set()

        for m in self.ma_tuple:
            if m not in ma_set:
                ma_set.add(m)
                self.axis[str(m)] = list()

    def heartbeats(self, date):
        super(MACrossAccount, self).heartbeats(date)

        avg_dict = dict()
        avg_price_list = list()

        for t in self.ma_tuple:
            if t not in avg_dict:
                avg_dict[t] = self.pool.average_line(date, self.base_line_horse, self.base_line_is_index, ma_length=t)
            avg_price_list.append(avg_dict[t])

        # enter_start = self.pool.average_line(date, self.base_line_horse, self.base_line_is_index, ma_length=self.ma_tuple[0])
        # enter_end = self.pool.average_line(date, self.base_line_horse, self.base_line_is_index, ma_length=self.ma_tuple[1])
        # leave_start = self.pool.average_line(date, self.base_line_horse, self.base_line_is_index, ma_length=self.ma_tuple[2])
        # leave_end = self.pool.average_line(date, self.base_line_horse, self.base_line_is_index, ma_length=self.ma_tuple[3])
        cur_price = self.pool.price(date, self.target_horse, self.target_is_index)

        if not self.is_holding:
            if avg_price_list[0] > avg_price_list[1]:
                if self.buy_account_percent(self.target_horse, cur_price, date, 1, self.target_is_index):
                    self.is_holding = True
        else:
            if avg_price_list[2] < avg_price_list[3]:
                if self.sell_all(self.target_horse, cur_price, date):
                    self.is_holding = False

        for k in avg_dict.keys():
            self.axis[str(k)].append(avg_dict[k] / self.base_index_start_value)

    def param_string(self):
        return "ma_cross_list__" + "_".join(str(x) for x in self.ma_tuple)

    def algorithm_category(self):
        return "ma"

    def algorithm_desc(self):
        return "ma_cross"

    @staticmethod
    def generator(pool):
        """
        
        :param pool: 
        :type pool: 
        :return: 
        :rtype: 
        """

        run_list = (
            # '000651', '600585', '600171', '002468', '600030',
            # '000333', '601318', '600999', '600660',
            # '002032',
            # '300039'
            # '600612', '600104', '600754', '600886', '601588',
            # '600809', '600028', '601398', '601088', '000650'
            # '603260', '600600', '300296', '002563', '000848', '002242'
            # '601828', '600398', '002233', '002327', '600703',
            # '002422', '600597', '000513'
            # '600547', '600988', '002155', '002697', '002736',
            # '000776',
            # '601988', '600028', '600859', '601928', '603008',
            # '002640', '002769', '603199'
            '601688', '601186', '601669', '601800', '601618',
            '601390', '600820', '600170'
        )

        # run_list = ('000001', '399001', '000300', '399006', '399005', '000905')
        is_index = False

        for target in run_list:
            params_pair = list()
            for start in range(10, 200, 20):
                for step in range(20, 190, 20):
                    if start + step <= 200:
                        params_pair.append((start, start + step))

            for param0 in params_pair:
                for param1 in params_pair:
                    print '{} {}'.format(param0, param1)
                    ac = MACrossAccount(pool, (param0[0], param0[1], param1[0], param1[1]),
                                        base_line_horse=target, base_line_is_index=is_index,
                                        target_horse=target, target_is_index=is_index)

                    fi = BackResult.objects.filter(param_string=ac.param_string(),
                                                   use_code=ac.code_to_string(ac.target_horse, ac.target_is_index),
                                                   base_line_code=ac.code_to_string(ac.base_line_horse, ac.base_line_is_index))

                    if len(fi) > 0:
                        print 'existed'
                        continue
                    else:
                        yield ac

                    # yield MACrossAccount(pool, (10, 30, 10, 30), target_horse='600519', target_is_index=False,
                    #                      base_line_horse='600519', base_line_is_index=False)
