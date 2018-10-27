import urllib2
import json


url = "http://emweb.securities.eastmoney.com/NewFinanceAnalysis/zcfzbAjax?companyType=4&reportDateType=0&reportType=1&endDate=1995-6-30+0:00:00&code=SZ000002"
print json.dumps(json.loads(json.loads(urllib2.urlopen(url).read())), indent=4)