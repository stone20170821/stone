# coding:utf-8
import urllib2
import json
import time

# url = "http://emweb.securities.eastmoney.com/NewFinanceAnalysis/xjllbAjax?companyType=4&reportDateType=0&reportType=1&endDate=2018-01-01&code=SH600519"
# obj = json.loads(json.loads(urllib2.urlopen(url).read()))
# source_str = '2017/6/30'
# print len(obj)
# print time.strptime(source_str, '%Y/%m/%d')

from django.core.management import BaseCommand
from core.model_utils import get_all_codes_from_models
import traceback
from core.models import CfsDongfangcaijing


class Command(BaseCommand):
    # 不提供的时候参数的值，如果值为这个，应该不处理
    PARAM_EMPTY_KEY = 'empty'

    def add_arguments(self, parser):
        super(Command, self).add_arguments(parser)
        parser.add_argument('--simple', nargs='?', default=self.PARAM_EMPTY_KEY,
                            help='')

    def handle(self, *args, **options):
        if options['simple'] is None:
            self.handle_simple()

    def handle_simple(self):
        codes = get_all_codes_from_models()
        key_report_date = "REPORTDATE"
        key_cash_left_clean = "NETOPERATECASHFLOW"
        print codes
        for code in codes:
            print code
            if code.startswith('6'):
                code_str = 'SH' + code
            else:
                code_str = 'SZ' + code

            end_date = ['', ]
            while True:
                try:
                    url_template = "http://emweb.securities.eastmoney.com/NewFinanceAnalysis/xjllbAjax?companyType=4&reportDateType=0&reportType=1&endDate={}&code={}"
                    url = url_template.format(
                        end_date[0], code_str)
                    print url
                    report_list = json.loads(json.loads(urllib2.urlopen(url).read()))
                    if len(report_list) <= 0:
                        break
                    for report in report_list:
                        obj = CfsDongfangcaijing()
                        obj.code = code
                        end_date[0] = report[key_report_date].split(' ')[0]
                        print end_date[0]
                        obj.report_date = time.mktime(time.strptime(end_date[0], '%Y/%m/%d'))
                        obj.n_cashflow_act = float(report[key_cash_left_clean])
                        obj.save()
                except:
                    traceback.print_exc()
                    break
