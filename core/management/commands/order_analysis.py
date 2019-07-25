# coding:utf-8


from horse_order import HorseOrder


class OrderAnalysis(object):
    """
    buy/sell成功率
    hold day count 
    avg hold day count
    total buy count
    total sell count
    这里的日计算包含休息日、节假日等（直接用order中的day相减获得）
    
    现有问题：
    1.暂时只支持全仓buy/sell
    2.当前统计方式会导致单年看意义不大，因为前一年的买和后一年卖这种情况不会被统计到
    """

    def __init__(self, orders):
        """
        :param orders: 
        :type orders: list[HorseOrder]
        """
        super(OrderAnalysis, self).__init__()
        self.orders = orders

        self.buy_sell_success_rate = 0
        self.total_hold_day_count = 0
        self.avg_hold_day_count = 0
        self.buy_count = 0
        self.sell_count = 0
        self.up_list = list()

    def calculate(self):
        last_buy_order = None
        day_count_list = list()
        self.buy_count = 0
        self.sell_count = 0
        self.total_hold_day_count = 0

        success_buy_sell_count = 0

        for order in self.orders:
            if order.opt == HorseOrder.BUY:
                last_buy_order = order
                self.buy_count += 1
            elif order.opt == HorseOrder.SELL:
                if last_buy_order is not None:
                    hold_days = (order.date - last_buy_order.date).days
                    day_count_list.append(hold_days)
                    self.total_hold_day_count += hold_days

                    up = (order.price - last_buy_order.price) / last_buy_order.price
                    if up > 0:
                        success_buy_sell_count += 1
                    self.up_list.append(up)
                self.sell_count += 1

        up_length = len(self.up_list)
        self.buy_sell_success_rate = float(success_buy_sell_count) / float(up_length) if up_length != 0 else 0
        self.avg_hold_day_count = float(self.total_hold_day_count) / float(up_length) if up_length != 0 else 0
