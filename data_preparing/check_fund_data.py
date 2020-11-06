import os
import json
import numpy as np
import pandas as pd
from pathlib import Path

DATAPath = '/home/kuoluo/data/fund_data'
all_fund = []
for _file in os.listdir(DATAPath):
    with open(DATAPath + '/' + _file, 'r') as fp:
        json_data = json.load(fp)
        if len(json_data) > 1 or len(json_data) == 0:
            print('test')
        all_fund.append(json_data[0])
# with open(OUTPath, 'w') as wp:
#     json.dump(all_fund, wp)

# 检查一级列表的数据
# fund_base_args = {}
# for fund in all_fund:
#     for key, value in fund.items():
#         if isinstance(value, dict) or isinstance(value, list):
#             continue
#         if key not in fund_base_args:
#             fund_base_args[key] = set()
#         fund_base_args[key].add(value)
# print('test')

# 检查二级列表的数据
records_args = {'manager_records': {}, 'asset_allocation_records': {}, 'indicators_records': {}}
error_records = {'days': {}, 'return': {}, 'stock': {}, 'bond': {}, 'cash': {}, 'other': {}, 'average_size': {}}
for fund in all_fund:
    for _manager_records in fund['manager_records']:
        for key, value in _manager_records.items():
            if key not in records_args:
                records_args['manager_records'][key] = set()
            records_args['manager_records'][key].add(value)
            # 错误
            if key == 'days' and value == 0:
                if fund['fund_id'] not in error_records['days']:
                    error_records['days'][fund['fund_id']] = []
                error_records['days'][fund['fund_id']].append(_manager_records['manager_id'])
            if key == 'return' and pd.isnull(value):
                if fund['fund_id'] not in error_records['return']:
                    error_records['return'][fund['fund_id']] = []
                error_records['return'][fund['fund_id']].append(_manager_records['manager_id'])
    for _asset_allocation_records in fund['asset_allocation_records']:
        for key, value in _asset_allocation_records.items():
            if key not in records_args:
                records_args['asset_allocation_records'][key] = set()
            records_args['asset_allocation_records'][key].add(value)
            # 错误
            if key == 'stock' and value > 1.0:
                if fund['fund_id'] not in error_records['stock']:
                    error_records['stock'][fund['fund_id']] = []
                error_records['stock'][fund['fund_id']].append(_asset_allocation_records['datetime'])
            if key == 'bond' and value > 1.0:
                if fund['fund_id'] not in error_records['bond']:
                    error_records['bond'][fund['fund_id']] = []
                error_records['bond'][fund['fund_id']].append(_asset_allocation_records['datetime'])
            if key == 'cash' and value > 1.0:
                if fund['fund_id'] not in error_records['cash']:
                    error_records['cash'][fund['fund_id']] = []
                error_records['cash'][fund['fund_id']].append(_asset_allocation_records['datetime'])
            if key == 'other' and (0 > value or value > 1.0):
                if fund['fund_id'] not in error_records['other']:
                    error_records['other'][fund['fund_id']] = []
                error_records['other'][fund['fund_id']].append(_asset_allocation_records['datetime'])
    for _indicators_records_records in fund['indicators_records']:
        for key, value in _indicators_records_records.items():
            if key not in records_args:
                records_args['indicators_records'][key] = set()
            records_args['indicators_records'][key].add(value)
            # 错误
            if key == 'average_size' and pd.isnull(value):
                if fund['fund_id'] not in error_records['average_size']:
                    error_records['average_size'][fund['fund_id']] = []
                error_records['average_size'][fund['fund_id']].append(_indicators_records_records['datetime'])

# print('test')  # max([_return for _return in manager_records_args['return'] if not pd.isnull(_return)])

# 检查三级列表的数据
error_holding = {'weight': {}, 'market_value': {}}
holding_records_args = {'datetime': set(), 'holding_list': {}}
for fund in all_fund:
    for _holding_records in fund['holding_records']:
        holding_records_args['datetime'].add(_holding_records['datetime'])
        for _holding in _holding_records['holdings_list']:
            for key, value in _holding.items():
                if key not in holding_records_args['holding_list']:
                    holding_records_args['holding_list'][key] = set()
                holding_records_args['holding_list'][key].add(value)
                # 错误
                if key == 'weight' and pd.isnull(value):
                    if fund['fund_id'] not in error_holding['weight']:
                        error_holding['weight'][fund['fund_id']] = {}
                    if _holding_records['datetime'] not in error_holding['weight'][fund['fund_id']]:
                        error_holding['weight'][fund['fund_id']][_holding_records['datetime']] = []
                    error_holding['weight'][fund['fund_id']][_holding_records['datetime']].append(_holding['order_book_id'])
                if key == 'market_value' and pd.isnull(value):
                    if fund['fund_id'] not in error_holding['market_value']:
                        error_holding['market_value'][fund['fund_id']] = {}
                    if _holding_records['datetime'] not in error_holding['market_value'][fund['fund_id']]:
                        error_holding['market_value'][fund['fund_id']][_holding_records['datetime']] = []
                    error_holding['market_value'][fund['fund_id']][_holding_records['datetime']].append(_holding['order_book_id'])

# 错误数据按照 基金id, 基金经理id和datetime 归类
error_fund = {}
for key, value in error_records.items():
    for _fund_id, _list in value.items():
        if _fund_id not in error_fund:
            error_fund[_fund_id] = {}
        if key == 'days' or key == 'return':
            if 'manager_id' not in error_fund[_fund_id]:
                error_fund[_fund_id] = {'manager_id': {}}
            for _id in _list:
                if _id not in error_fund[_fund_id]['manager_id']:
                    error_fund[_fund_id]['manager_id'] = {_id: []}
                error_fund[_fund_id]['manager_id'][_id].append(key)
        if key == 'stock' or key == 'bond' or key == 'cash' or key == 'other' or key == 'average_size':
            if 'datetime' not in error_fund[_fund_id]:
                error_fund[_fund_id] = {'datetime': {}}
            for _id in _list:
                if _id not in error_fund[_fund_id]['datetime']:
                    error_fund[_fund_id]['datetime'] = {_id: {}}
                error_fund[_fund_id]['datetime'][_id][key] = '有问题'
for key, value in error_holding.items():
    for _fund_id, _list in value.items():
        if _fund_id not in error_fund:
            error_fund[_fund_id] = {'datetime': {}}
        for _datetime, _ids in _list.items():
            if _datetime not in error_fund[_fund_id]['datetime']:
                error_fund[_fund_id]['datetime'] = {_datetime: {'order_book_id': {}}}
            for _id in _ids:
                if _id not in error_fund[_fund_id]['datetime'][_datetime]['order_book_id']:
                    error_fund[_fund_id]['datetime'][_datetime]['order_book_id'] = {_id: []}
                error_fund[_fund_id]['datetime'][_datetime]['order_book_id'][_id].append(key)
print('save error funds')  # max([_return for _return in holding_records_args['holding_list']['weight'] if not pd.isnull(_return)])
with open('data/error_funds.json', 'w') as wp:
    json.dump(error_fund, wp)
