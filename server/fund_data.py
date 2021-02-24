import json
import sys
from collections import defaultdict

import numpy as np
from tools import show_tool
import matplotlib.pyplot as plt

sys.path.append('/home/kuoluo/projects/FundAnalysis/')
from server import common
from models import tsne


def get_fund_last_income(fund_ids, interval=5000):
    fund_dict = {}
    for f_id in fund_ids:
        fund = common.get_source_fund_json(f_id)
        first_nav = fund['nav'][0]['acc_net_value']
        last_nav = fund['nav'][-1]['acc_net_value']
        fund_dict[f_id] = last_nav / first_nav - 1
    result = show_tool.sort_interval(fund_dict, interval)
    return result


def get_fund_last_size(fund_ids, interval=5000):
    fund_dict = {}
    for f_id in fund_ids:
        fund = common.get_source_fund_json(f_id)
        fund_dict[f_id] = fund['asset_allocation_records'][-1]['net_asset']
    result = show_tool.sort_interval(fund_dict, interval)
    return result


def get_fund_last_holder(fund_ids, interval=5000):
    fund_dict = {}
    for f_id in fund_ids:
        fund = common.get_source_fund_json(f_id)
        if len(fund['holder_structure']) == 0 or fund['holder_structure'][-1]['instl_weight'] is None:
            continue
        fund_dict[f_id] = fund['holder_structure'][-1]['instl_weight']
    result = show_tool.sort_interval(fund_dict, interval)
    return result


def get_fund_last_sharp_ratio(fund_ids, interval=5000):
    fund_dict = {}
    for f_id in fund_ids:
        fund = common.get_source_fund_json(f_id)
        fund_dict[f_id] = fund['indicators_records'][-1]['sharp_ratio']
    result = show_tool.sort_interval(fund_dict, interval)
    return result


def get_fund_last_max_drop(fund_ids, interval=5000):
    fund_dict = {}
    for f_id in fund_ids:
        fund = common.get_source_fund_json(f_id)
        fund_dict[f_id] = fund['indicators_records'][-1]['max_drop_down']
    result = show_tool.sort_interval(fund_dict, interval)
    return result


def get_fund_dict(fund_ids, key):
    fund_dict = {}
    for f_id in fund_ids:
        fund_dict[f_id] = {}
        fund = common.get_source_fund_json(f_id)
        for nav_dict in fund['nav']:
            fund_dict[f_id][nav_dict['datetime']] = nav_dict[key]
    return fund_dict


def get_fund_time_nav(fund_ids, start_date=None, end_date=None, nav_type='unit_net_value'):
    fund_dict = {}
    for f_id in fund_ids:
        fund_dict[f_id] = {}
        first_nav = None
        fund = common.get_source_fund_json(f_id)
        for nav_dict in fund['nav']:
            if (start_date is None and end_date is None) or \
                    (start_date is None and int(nav_dict['datetime']) <= int(end_date)) or \
                    (end_date is None and int(start_date) <= int(nav_dict['datetime'])) or \
                    int(start_date) <= int(nav_dict['datetime']) <= int(end_date):
                if first_nav is None:
                    first_nav = nav_dict[nav_type]
                fund_dict[f_id][nav_dict['datetime']] = nav_dict[nav_type]
    return fund_dict


def get_fund_time_border(fund_ids):
    min_start_date = None
    max_end_date = None
    for f_id in fund_ids:
        fund = common.get_source_fund_json(f_id)
        if min_start_date is None or int(fund['nav'][0]['datetime']) < min_start_date:
            min_start_date = int(fund['nav'][0]['datetime'])
        if max_end_date is None or max_end_date < int(fund['nav'][-1]['datetime']):
            max_end_date = int(fund['nav'][-1]['datetime'])
    return min_start_date, max_end_date


def get_fund_date_sector(fund_ids):
    fund_dict = {}
    for f_id in fund_ids:
        fund_dict[f_id] = {}
        fund = common.get_source_fund_json(f_id)
        for holding_record in fund['holding_records']:
            fund_dict[f_id][holding_record['datetime']] = {}
            for hold in holding_record['holdings_list']:
                if hold['order_book_id'][:6] in common.stock_sector:
                    _sector = common.stock_sector[hold['order_book_id'][:6]]
                else:
                    _sector = '未知'
                if _sector not in fund_dict[f_id][holding_record['datetime']]:
                    fund_dict[f_id][holding_record['datetime']][_sector] = 0
                fund_dict[f_id][holding_record['datetime']][_sector] = hold['market_value']
    return fund_dict


def get_fund_date_income(fund_ids, start_date=None, end_date=None):
    fund_dict = {}
    for f_id in fund_ids:
        fund_dict[f_id] = {}
        first_nav = None
        fund = common.get_source_fund_json(f_id)
        for nav_dict in fund['nav']:
            if (start_date is None and end_date is None) or \
                    (start_date is None and int(nav_dict['datetime']) <= int(end_date)) or \
                    (end_date is None and int(start_date) <= int(nav_dict['datetime'])) or \
                    int(start_date) <= int(nav_dict['datetime']) <= int(end_date):
                if first_nav is None:
                    first_nav = nav_dict['unit_net_value']
                fund_dict[f_id][nav_dict['datetime']] = round((nav_dict['unit_net_value'] / first_nav - 1) * 100, 2)
    return fund_dict


def get_fund_t_sne(fund_ids):
    init_fund_data = {}
    max_size = None
    min_nav_len = 100
    dates = set()
    funds = {}
    for f_id in fund_ids:
        fund = common.get_view_fund_json(f_id)
        for _date, _value in fund.items():
            dates.add(_date)
            if min_nav_len > len(_value['risks']):
                min_nav_len = len(_value['risks'])
            _value.pop('holding')
            if 'instl_weight' in _value:
                _value.pop('instl_weight')
                _value.pop('retail_weight')
            fund[_date] = _value
            init_fund_data[f_id] = _value
            if 'size' in _value and (max_size is None or max_size < _value['size']):
                max_size = _value['size']
        funds[f_id] = fund
    x, clasz = tsne.get_fund_feature(init_fund_data, max_size, min_nav_len)
    num_fund = len(fund_ids)
    y, dy, iy, gains = tsne.get_y(num_fund, 2)
    p = tsne.get_p(np.array(x))
    data_2d, dy, iy, gains = tsne.t_sne(p, num_fund, y, dy, iy, gains, 2)
    dates = sorted(list(dates), key=lambda v: int(v))
    result = {}
    for _da in dates:
        result[_da] = {}
        x, clasz, index_funds = tsne.update_features(x, clasz, funds, _da, max_size, min_nav_len)
        p = tsne.get_p(np.array(x))
        data_2d, dy, iy, gains = tsne.t_sne(p, num_fund, y, dy, iy, gains, 2, max_iter=100)
        for i, f_id in index_funds.items():
            result[_da][f_id] = {'loc': (data_2d[i][0], data_2d[i][1]), 'manager_id': clasz[i]}
    return result


def get_fund_ranks(weights, tops=20):
    fund_ids = common.fund_ids
    funds = {}
    for f_id in fund_ids:
        fund = list(common.get_view_fund_json(f_id).items())[-1][1]
        _sum = 0
        for _name, _value in fund.items():
            if 'instl_weight' == _name or 'retail_weight' == _name or 'holding' == _name or 'manager_id' == _name or 'nav' == _name or 'risk' == _name:
                continue
            if 'navs' == _name or 'risks' == _name:
                list_sum = 0
                for _d, _v in _value[_name]:
                    list_sum += _v
                _sum += weights[_name] * list_sum
            else:
                _sum += weights[_name] * _value
            funds[f_id] = _sum
    funds = sorted(funds.items(), key=lambda v: v, reverse=True)
    return funds[:tops]


if __name__ == '__main__':
    # min_start_date, max_end_date = get_fund_time_border(['163402'])
    # fund_date_income = get_fund_dict(['163402'], 'unit_net_value')
    # print('start')
    # min_start_date, max_end_date = get_fund_time_border(['510310'])
    # fund_date_income = get_fund_date_income(['510310'], min_start_date, max_end_date)
    #
    # min_start_date, max_end_date = get_fund_time_border(fund_ids)
    # fund_date_sector = get_fund_date_sector(fund_ids)
    # fund_date_income = get_fund_date_income(fund_ids, min_start_date, max_end_date)
    # project_path = '/home/kuoluo/projects/FundAnalysis'
    # get_fund_ranks({'stock': 1.0, 'bond': 1.0, 'cash': 1.0, 'other': 1.0, 'size': 1.0, 'alpha': 1.0, 'beta': 1.0,
    #                 'sharp_ratio': 1.0, 'information_ratio': 1.0, 'navs': 1.0, 'risks': 1.0})
    funds = get_fund_t_sne(common.fund_ids[:10])
    project_path = 'E:/Projects/PythonProjects/FundAnalysis'
    with open(project_path + '/data/temp/funds_tsne.json', 'w', encoding='UTF-8') as wp:
        json.dump(funds, wp)
    print('over')

    _income = get_fund_last_income(common.fund_ids)
    with open(project_path + '/data/temp/income.json', 'w') as wp:
        json.dump(_income, wp)
    _size = get_fund_last_size(common.fund_ids)
    with open(project_path + '/data/temp/size.json', 'w') as wp:
        json.dump(_size, wp)
    _holder = get_fund_last_holder(common.fund_ids)
    with open(project_path + '/data/temp/holder.json', 'w') as wp:
        json.dump(_holder, wp)
    _risk = get_fund_last_sharp_ratio(common.fund_ids)
    with open(project_path + '/data/temp/risk.json', 'w') as wp:
        json.dump(_risk, wp)
    _max_drop = get_fund_last_max_drop(common.fund_ids)
    with open(project_path + '/data/temp/max_drop.json', 'w') as wp:
        json.dump(_max_drop, wp)
    print('over')
