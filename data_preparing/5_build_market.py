import json
import os
from collections import defaultdict

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'
fund_files = os.listdir(project_path + '/data/view_funds')


def get_index_return(index_json):
    x_date = [i for i in index_json.keys()]
    x_date.sort()
    income_close = dict()
    for _date in x_date:
        income_close[_date] = index_json[_date]['收盘价']
    return income_close


with open('/home/kuoluo/data/fund/index.json', 'r') as fp:
    index_data = json.load(fp)
hs300 = get_index_return(index_data['沪深300'])
hs300_list = list(hs300.items())


def get_market_fund_sector_by_report(files):
    sector_set = set()
    date_set = set()
    for file in files:
        with open(project_path + '/data/view_funds/' + file, 'r', encoding='UTF-8') as fp:
            view_fund = json.load(fp)
        for _date, _value in view_fund.items():
            date_set.add(_date)
            for _s, _v in _value['holding_values'].items():
                sector_set.add(_s)
    date_set = sorted(list(date_set), key=lambda v: v)
    sector_date = {_s: {_d: 0 for _d in date_set} for _s in sector_set}
    date_sector = {_d: {_s: 0 for _s in sector_set} for _d in date_set}
    size_date = {_d: 0 for _d in date_set}
    number_date = {_d: 0 for _d in date_set}
    income_date = {_d: {} for _d in date_set}
    for file in files:
        with open(project_path + '/data/view_funds/' + file, 'r', encoding='UTF-8') as fp:
            view_fund = json.load(fp)
        pre_value = None
        pre_nav = None
        for i, _date in enumerate(date_set):
            if _date not in view_fund and pre_value is None:
                continue
            if _date in view_fund:
                pre_value = view_fund[_date]
            if pre_nav is None:
                pre_nav = view_fund[_date]['unit_nav']
            for _s, _v in pre_value['holding_values'].items():
                sector_date[_s][_date] += _v
                date_sector[_date][_s] += _v
            number_date[_date] += 1
            size_date[_date] += pre_value['size']
            income_date[_date][file[:-5]] = {'income': pre_value['unit_nav'] / pre_nav - 1, 'size': pre_value['size']}
    for _date, _values in income_date.items():
        sum_size = 0
        for f_id, _navs in _values.items():
            sum_size += _navs['size']
        _income = 0
        for f_id, _navs in _values.items():
            _income += _navs['income'] * _navs['size'] / sum_size
        income_date[_date] = _income
    hs300_date = {}
    pre_hs300 = None
    _i = 0
    for i, _date in enumerate(date_set):
        temp = _i
        for __i, _v in enumerate(hs300):
            if __i < temp:
                continue
            if int(hs300_list[__i][0]) <= int(_date):
                temp = __i
            if int(hs300_list[__i][0]) > int(_date):
                break
        _i = temp
        if pre_hs300 is None:
            pre_hs300 = hs300[_date]
        hs300_date[_date] = hs300_list[_i][1] / pre_hs300 - 1
    return sector_date, number_date, size_date, hs300_date, income_date, date_sector


sector_date, number_date, size_date, hs300_date, income_date, date_sector = get_market_fund_sector_by_report(fund_files)
with open(project_path + '/data/market/market_sector_date.json', 'w') as wp:
    json.dump(sector_date, wp)
with open(project_path + '/data/market/market_date_sector.json', 'w') as wp:
    json.dump(date_sector, wp)
with open(project_path + '/data/market/market_fund_number.json', 'w') as wp:
    json.dump(number_date, wp)
with open(project_path + '/data/market/market_fund_size.json', 'w') as wp:
    json.dump(size_date, wp)
with open(project_path + '/data/market/market_hs300.json', 'w') as wp:
    json.dump(hs300_date, wp)
with open(project_path + '/data/market/market_fund_income.json', 'w') as wp:
    json.dump(income_date, wp)
print('over')
