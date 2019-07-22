# codeing: utf-8

from core.models import BackResultYear

import datetime
import json

date_format = "%Y_%m_%d_%H_%M_%S"


class BackResultYearDivider(object):
    def __init__(self, br):
        super(BackResultYearDivider, self).__init__()
        self.br = br
        self.cur_max_value = -1
        self.cur_max_down = 0
        self.max_down_start = None
        self.max_down_end = None
        self.saved_max_down_start = None
        self.cur_year_win_records = dict()
        self.last_year = 0
        self.cur_price = 0
        self.cur_date_origin = None
        self.win_records = None

    def __need_consider_target(self):
        return self.br.use_code != self.br.base_line_code

    def __save_back_result_year(self):
        year_result = BackResultYear()
        year_result.use_year = self.last_year
        year_result.from_result = self.br

        year_result.base_line_code = self.br.base_line_code
        year_result.base_line_result = self.cur_year_win_records['index'][-1] - self.cur_year_win_records['index'][0]

        year_result.use_code = self.br.use_code

        if self.__need_consider_target():
            year_result.use_code_result = self.cur_year_win_records['target'][-1] - self.cur_year_win_records['target'][0]
        else:
            year_result.use_code_result = self.cur_year_win_records['index'][-1] - self.cur_year_win_records['index'][0]

        year_result.final_win = self.cur_year_win_records['hold'][-1] - self.cur_year_win_records['hold'][0]
        year_result.win_records = json.dumps(self.cur_year_win_records)
        year_result.date_start = datetime.datetime.strptime(self.cur_year_win_records['date'][0], date_format)
        year_result.date_end = datetime.datetime.strptime(self.cur_year_win_records['date'][-1], date_format)
        year_result.run_time = self.br.run_time
        year_result.algorithm_category = self.br.algorithm_category
        year_result.algorithm_desc = self.br.algorithm_desc
        year_result.param_string = self.br.param_string
        year_result.max_down = self.cur_max_down
        year_result.max_down_start = self.max_down_start if self.max_down_start is not None else datetime.datetime.today()
        year_result.max_down_end = self.max_down_end if self.max_down_end is not None else datetime.datetime.today()
        year_result.save()

    def __calculate_md(self):
        if self.cur_price > self.cur_max_value:
            self.cur_max_value = self.cur_price
            self.saved_max_down_start = self.cur_date_origin

        my_max_down = (self.cur_max_value - self.cur_price) / self.cur_max_value
        if my_max_down > self.cur_max_down:
            self.cur_max_down = my_max_down
            self.max_down_start = self.saved_max_down_start
            self.max_down_end = self.cur_date_origin

    def divide(self):
        try_year_br = BackResultYear.objects.filter(from_result=self.br)

        if not (try_year_br is None or len(try_year_br) <= 0):
            print 'br with id {} already existed'.format(self.br.id)
            return

        self.win_records = json.loads(self.br.win_records)

        if not ('hold' in self.win_records and 'date' in self.win_records and 'index' in self.win_records):
            print 'win_records info lack problem'
            return

        length = len(self.win_records['date'])

        for i in range(0, length):
            self.cur_date_origin = datetime.datetime.strptime(self.win_records['date'][i], date_format)
            self.cur_price = self.win_records['hold'][i]

            if self.cur_date_origin.year != self.last_year:
                if self.last_year != 0:
                    self.__save_back_result_year()

                    #  reset all memory value
                    self.cur_year_win_records = dict()
                    self.cur_max_value = -1
                    self.cur_max_down = 0
                    self.max_down_start = None
                    self.max_down_end = None
                    self.saved_max_down_start = None

                self.last_year = self.cur_date_origin.year

            self.__calculate_md()

            for key in self.win_records:
                if key not in self.cur_year_win_records:
                    self.cur_year_win_records[key] = list()

                self.cur_year_win_records[key].append(self.win_records[key][i])

        if self.last_year != 0:
            self.__save_back_result_year()
