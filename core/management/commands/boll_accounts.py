# coding:utf-8

from account import Account, InfoPool


class SimpleBollAccount(Account):
    def __init__(self, pool, ma_length=20, p=2.0, start_fond=10000000.0, target_horse='000001', target_is_index=True, base_line_horse='000001', base_line_is_index=True,
                 start_date='20100105'):
        super(SimpleBollAccount, self).__init__(pool, start_fond, target_horse, target_is_index, base_line_horse, base_line_is_index, start_date)

        self.ma_length = ma_length
        self.p = p

        self.ma_vs = list()
        self.axis[str(ma_length)] = self.ma_vs

        self.up = list()
        self.down = list()
        self.axis['up'] = self.up
        self.axis['down'] = self.down

        self.is_holding = False

    def heartbeats(self, date):
        """
        :param date: 
        :type date: 
        :return: 
        :rtype: 
        """
        super(SimpleBollAccount, self).heartbeats(date)

        cur = self.current_target_or_index_price()
        cur_index = self.pool.price(date, self.base_line_horse, self.base_line_is_index)
        avg, up, down = self.pool.boll(date, self.base_line_horse, self.base_line_is_index, self.ma_length, p=self.p)

        if self.is_holding:
            if cur_index < down:
                self.sell_all(self.target_horse, cur, date)
                self.is_holding = False
        else:
            if cur_index > up:
                self.buy_account_percent(self.target_horse, cur, date, 1, self.target_is_index)
                self.is_holding = True

        self.ma_vs.append(avg / self.base_index_start_value)
        self.up.append(up / self.base_index_start_value)
        self.down.append(down / self.base_index_start_value)

    def param_string(self):
        return "simple_boll: {} p {}".format(self.ma_length, self.p).replace(' ', '_').replace(':', '_')

    def algorithm_category(self):
        return "boll"

    def algorithm_desc(self):
        return "simple_boll"

    @staticmethod
    def generator(pool):
        """
        target base param
        600519：600519: (10, 90): (1.5, 3.6) done
        000651: 000651 : (10, 90): (1.5, 3.6) ready
        600585: 600585 : (10, 90): (1.5, 3.6) ready
        600171: 600171 : (10, 90): (1.5, 3.6) ready
        002468: 002468 : (10, 90): (1.5, 3.6) ready
        600030: 600030 : (10, 90): (1.5, 3.6) ready
        000333: 000333 : (10, 90): (1.5, 3.6) ready
        601318: 601318 : (10, 90): (1.5, 3.6) ready
        600999: 600999 : (10, 90): (1.5, 3.6) ready
        600660: 600660 : (10, 90): (1.5, 3.6) ready
        002032: 002032 : (10, 90): (1.5, 3.6) ready
        
        300039: 300039 : (10, 90): (1.5, 3.6) ready
        600754: 600754 : (10, 90): (1.5, 3.6) ready
        600886: 600886 : (10, 90): (1.5, 3.6) ready
        :param pool: 
        :type pool: 
        :return: 
        :rtype: 
        
        """
        # for ma in range(10, 90):
        #     for p in range(15, 36):
        #         # for i in Account.CONSIDER_INDEX:
        #             yield SimpleBollAccount(pool, ma, p / 10.0,
        #                                     base_line_horse='600585', base_line_is_index=False,
        #                                     target_horse='600585', target_is_index=False)
        #
        # for ma in range(10, 90):
        #     for p in range(15, 36):
        #         # for i in Account.CONSIDER_INDEX:
        #         yield SimpleBollAccount(pool, ma, p / 10.0,
        #                                 base_line_horse='600171', base_line_is_index=False,
        #                                 target_horse='600171', target_is_index=False)

        # for ma in range(10, 90):
        #     for p in range(15, 36):
        #         yield SimpleBollAccount(pool, ma, p / 10.0,
        #                                 base_line_horse='002468', base_line_is_index=False,
        #                                 target_horse='002468', target_is_index=False,
        #                                 start_date='20100908')
        #
        # for ma in range(10, 90):
        #     for p in range(15, 36):
        #         yield SimpleBollAccount(pool, ma, p / 10.0,
        #                                 base_line_horse='000333', base_line_is_index=False,
        #                                 target_horse='000333', target_is_index=False,
        #                                 start_date='20130917')
        #
        # for ma in range(10, 90):
        #     for p in range(15, 36):
        #         yield SimpleBollAccount(pool, ma, p / 10.0,
        #                                 base_line_horse='600030', base_line_is_index=False,
        #                                 target_horse='600030', target_is_index=False)

        # run_list = (
        #     '000651', '600585', '600171', '002468', '600030',
        #     '000333', '601318', '600999', '600660', '002032'
        # )

        # run_list = (
        #     '000651', '600585', '600171', '002468', '600030',
        #     '000333', '601318', '600999', '600660', '002032'
        # )

        # ready
        # for t in run_list:
        #     for ma in range(10, 90):
        #         for p in range(15, 36):
        #             yield SimpleBollAccount(pool, ma, p / 10.0,
        #                                     base_line_horse=t, base_line_is_index=False,
        #                                     target_horse=t, target_is_index=False,
        #                                     # start_date='20100107'
        #                                     )

        # yield SimpleBollAccount(pool, 20, 2.5, base_line_horse='600519', base_line_is_index=False,
        #                         target_horse='600519', target_is_index=False)

        yield SimpleBollAccount(pool, 20, 2.5,
                                base_line_horse='000333', base_line_is_index=False,
                                target_horse='000333', target_is_index=False,
                                # start_date='20100107'
                                )
