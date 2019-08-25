# coding: utf-8

from account import Account


class MacdGoldCrossAccount(Account):
    def __init__(self, pool, start=12, end=26, dea_length=9,
                 start_fond=10000000.0, target_horse='000001', target_is_index=True, base_line_horse='000001',
                 base_line_is_index=True,
                 start_date='20100105'):
        super(MacdGoldCrossAccount, self).__init__(pool, start_fond, target_horse, target_is_index, base_line_horse, base_line_is_index, start_date)
        self.start = start
        self.end = end
        self.dea_length = dea_length

        self.dea = list()
        self.axis['dea{}'.format(dea_length)] = self.dea

        self.diff = list()
        self.axis['diff{}_{}'.format(start, end)] = self.diff

        self.is_hold = False

    def heartbeats(self, date):
        super(MacdGoldCrossAccount, self).heartbeats(date)

        diff, dea, bar = self.pool.macd(date, self.target_horse, self.target_is_index, self.start, self.end, self.dea_length)
        cur_price = self.pool.price(date, self.target_horse, self.target_is_index)

        self.diff.append(diff)
        self.dea.append(dea)

        if self.is_hold:
            if dea > diff:
                if self.sell_all(self.target_horse, cur_price, date):
                    self.is_hold = False
        else:
            if diff > dea:
                if self.buy_account_percent(self.target_horse, cur_price, date, 1.0, self.target_is_index):
                    self.is_hold = True

    def param_string(self):
        return "macd_gold_cross_{}_{}_{}".format(self.start, self.end, self.dea_length)

    def algorithm_category(self):
        return "macd"

    def algorithm_desc(self):
        return "macd_gold_cross"

    @staticmethod
    def generator(pool):

        run_list = (
            # '000651', '600585', '600171', '002468', '600030',
            '000333', '601318', '600999', '600660', '600519',
            '002032',
            '300039', '002242',
            # '600612', '600104', '600754', '600886', '601588',
            # '600809', '600028', '601398', '601088', '000650'
            # '603260', '600600', '300296', '002563', '000848',
            # '601828', '600398', '002233', '002327', '600703',
            # '002422', '600597', '000513'
            # '600547', '600988', '002155', '002697', '002736',
            # '000776',
            # '601988', '600028', '600859', '601928', '603008',
            # '002640', '002769', '603199'
            # '601688', '601186', '601669', '601800', '601618',
            # '601390', '600820', '600170'
        )

        # run_list = ('000001', '399001', '000300', '399006', '399005', '000905')
        is_index = False

        for r in run_list:
            for start in range(6, 51, 3):
                for step1 in range(6, 36, 2):
                    for step2 in range(1, 16):
                        dea = start - step2
                        if dea >= 5:
                            yield MacdGoldCrossAccount(pool,
                                                       start=start,
                                                       end=start + step1,
                                                       dea_length=start - step2,
                                                       target_horse=r,
                                                       target_is_index=is_index,
                                                       base_line_horse=r,
                                                       base_line_is_index=is_index)
