# coding: utf-8

import datetime
import json
from command_utils import date_format


class HorseOrder(object):
    BUY = "buy"
    SELL = "sell"

    __TAX_PERCENT = 0.003

    def __init__(self, opt, price, volume, date, target, target_is_index):
        super(HorseOrder, self).__init__()
        self.opt = opt
        self.price = price
        self.volume = volume
        self.date = date
        """:type:datetime.datetime"""
        self.target = target
        self.target_is_index = target_is_index

    def __str__(self):
        return json.dumps(self.to_dict())

    @staticmethod
    def from_json_string(json_string):
        json_dict = json.loads(json_string)
        return HorseOrder.from_dict(json_dict)

    @staticmethod
    def from_dict(json_dict):
        return HorseOrder(
            opt=json_dict['opt'],
            price=float(json_dict['price']),
            volume=long(json_dict['volume']),
            date=datetime.datetime.strptime(json_dict['date'], date_format),
            target=json_dict['target'],
            target_is_index=bool(json_dict['target_is_index']),
        )

    def to_dict(self):
        return {
            'opt': self.opt,
            'price': str(self.price),
            'volume': str(self.volume),
            'date': self.date.strftime(date_format),
            'target': self.target,
            'target_is_index': str(self.target_is_index)
        }

    def to_json_string(self):
        return json.dumps(self.to_dict())

    def tax(self):
        """
        税直接收取千分之三
        """
        return self.price * self.volume * self.__TAX_PERCENT

    @staticmethod
    def pure_tax(opt, price, volume):
        return price * volume * HorseOrder.__TAX_PERCENT

    def receive(self):
        return self.price * self.volume - self.tax() if self.opt == self.SELL else 0

    def cost(self):
        return self.price * self.volume + self.tax() if self.opt == self.BUY else 0

