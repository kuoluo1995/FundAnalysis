import json
from collections import defaultdict
from copy import copy

from server import common


def get_market_fund_size_by_month():
    market_dict = defaultdict(float)
    for f_id in common.fund_ids:
        record = common.get_source_fund_json(f_id)
        for asset_record in record['asset_allocation_records']:
            market_dict[asset_record['datetime'][:6]] += asset_record['net_asset']
    market_dict = sorted(market_dict.items(), key=lambda v: int(v[0]))
    market_dict = {_d: _v for _d, _v in market_dict}
    return market_dict


def get_market_fund_number_by_month():
    market_dict = defaultdict(int)
    for f_id in common.fund_ids:
        record = common.get_source_fund_json(f_id)
        market_dict[record['listed_date']] += 1
        if int(record['de_listed_date']) != 0:
            market_dict[record['de_listed_date']] -= 1
    market_dict = sorted(market_dict.items(), key=lambda v: int(v[0]))
    market_number = dict()
    pre_sum = 0
    for _date, _num in market_dict:
        market_number[_date[:6]] = pre_sum + _num
        pre_sum = market_number[_date[:6]]
    return market_number


def get_market_fund_income_by_month():
    market_dict = defaultdict(dict)
    for f_id in common.fund_ids:
        record = common.get_source_fund_json(f_id)
        first_acc_nav = None
        for _nav in record['nav']:
            if first_acc_nav is None:
                first_acc_nav = _nav['acc_net_value']
            market_dict[_nav['datetime'][:6]][record['fund_id']] = _nav['acc_net_value'] / first_acc_nav - 1
    market_dict = sorted(market_dict.items(), key=lambda v: int(v[0]))
    market_income = dict()
    for _d, _f_v in market_dict:
        sum = 0
        for _f, _v in _f_v.items():
            sum += _v
        market_income[_d] = sum / len(_f_v)
    return market_income


def get_market_fund_sector_by_month():
    market_dict = defaultdict(dict)
    market_set = set()
    for f_id in common.fund_ids:
        fund = common.get_source_fund_json(f_id)
        for records in fund['holding_records']:
            for holding in records['holdings_list']:
                if holding['order_book_id'][:6] in common.stock_sector:
                    _sector = common.stock_sector[holding['order_book_id'][:6]]
                else:
                    _sector = '未知'
                if _sector not in market_dict[records['datetime'][:6]]:
                    market_dict[records['datetime'][:6]][_sector] = 0
                market_dict[records['datetime'][:6]][_sector] += holding['market_value']
                market_set.add(_sector)
    market_dict = sorted(market_dict.items(), key=lambda v: int(v[0]))
    result = {}
    market_pre_dict = {}
    for _date, _market in market_dict:
        for _sector in market_set:
            if _sector not in market_pre_dict:
                market_pre_dict[_sector] = 0
            if _sector in _market:
                market_pre_dict[_sector] = _market[_sector]
        result[_date] = market_pre_dict.copy()
    return result


def get_market_sector_value():
    market_dict = {}
    for f_id in common.fund_ids:
        fund = common.get_source_fund_json(f_id)
        for _record in fund['holding_records']:
            for holding in _record['holdings_list']:
                if holding['order_book_id'][:6] in common.stock_sector:
                    _sector = common.stock_sector[holding['order_book_id'][:6]]
                else:
                    _sector = '未知'
                if _sector not in market_dict:
                    market_dict[_sector] = {}
                if _record['datetime'] not in market_dict[_sector]:
                    market_dict[_sector][_record['datetime']] = 0
                market_dict[_sector][_record['datetime']] += holding['market_value']
    for _sector, date_value in market_dict.items():
        date_value = sorted(date_value.items(), key=lambda d: int(d[0]), reverse=False)
        temp = dict()
        for _date, _value in date_value:
            temp[_date] = _value
        market_dict[_sector] = temp
    return market_dict


if __name__ == '__main__':
    # market_fund_size = get_market_fund_size_by_month()
    # market_fund_number = get_market_fund_number_by_month()
    # market_fund_income = get_market_fund_income_by_month()
    project_path = '/home/kuoluo/projects/FundAnalysis/data/temp'
    # project_path = 'E:/Projects/PythonProjects/FundAnalysis/data/temp'
    market_fund_sector = get_market_fund_sector_by_month()

    with open(project_path + '/market_sector.json', 'w') as wp:
        json.dump(market_fund_sector, wp)
    print('over')
