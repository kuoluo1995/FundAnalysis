import json
import os
import numpy as np
from collections import defaultdict

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'
fund_files = os.listdir(project_path + '/data/source')

with open('/home/kuoluo/data/fund/index.json', 'r') as fp:
    index_data = json.load(fp)


def get_index_return(index_json):
    x_date = [i for i in index_json.keys()]
    x_date.sort()
    income_close = dict()
    for _date in x_date:
        income_close[_date] = index_json[_date]['收盘价']
    return income_close


hs300 = get_index_return(index_data['沪深300'])
hs300_list = list(hs300.items())


def get_fund(file):
    fund_dict = defaultdict(dict)
    with open(project_path + '/data/source/' + file, 'r', encoding='UTF-8') as rp:
        fund = json.load(rp)
    _i = 0
    for _record in fund['nav']:
        temp = _i
        for __i, _v in enumerate(hs300):
            if __i < temp:
                continue
            if int(hs300_list[__i][0]) <= int(_record['datetime']):
                temp = __i
            if int(hs300_list[__i][0]) > int(_record['datetime']):
                break
        _i = temp
        fund_dict[_record['datetime']]['hs300'] = hs300_list[_i][1]
        fund_dict[_record['datetime']]['unit_nav'] = _record['unit_net_value']
        fund_dict[_record['datetime']]['acc_nav'] = _record['acc_net_value']
    for _record in fund['asset_allocation_records']:
        fund_dict[_record['datetime']]['stock'] = _record['stock']
        fund_dict[_record['datetime']]['bond'] = _record['bond']
        fund_dict[_record['datetime']]['cash'] = _record['cash']
        fund_dict[_record['datetime']]['other'] = _record['other']
        fund_dict[_record['datetime']]['size'] = _record['net_asset']
    for _record in fund['holder_structure']:
        fund_dict[_record['date']]['instl_weight'] = _record['instl_weight'] / 100
    for _record in fund['indicators_records']:
        fund_dict[_record['datetime']]['alpha'] = _record['total_alpha']
        fund_dict[_record['datetime']]['beta'] = _record['total_beta']
        fund_dict[_record['datetime']]['sharp_ratio'] = _record['sharp_ratio']
        fund_dict[_record['datetime']]['max_drop_down'] = _record['max_drop_down']
        fund_dict[_record['datetime']]['information_ratio'] = _record['information_ratio']
    for _record in fund['holding_records']:
        _sector_dict = defaultdict(float)
        _sum = 0
        for holding in _record['holdings_list']:
            _sector_dict[holding['sector']] += holding['market_value']
            _sum += holding['market_value']
        _sector_dict = sorted(_sector_dict.items(), key=lambda v: v[1], reverse=True)
        temp = {}
        for _sector, _v in _sector_dict:
            temp[_sector] = _v / _sum
        fund_dict[_record['datetime']]['holding'] = temp
        fund_dict[_record['datetime']]['holding_values'] = {_sector: _v for _sector, _v in _sector_dict}
    fund_dict = sorted(fund_dict.items(), key=lambda v: int(v[0]))
    result = {}
    detail_unit_nav = {}
    detail_acc_nav = {}
    detail_hs300 = {}
    for _i, (_date, _v) in enumerate(fund_dict):
        for _z in range(0, _i):
            if 'unit_nav' not in fund_dict[_i - _z][1]:
                continue
            _v['unit_nav'] = fund_dict[_i - _z][1]['unit_nav']
            _v['acc_nav'] = fund_dict[_i - _z][1]['acc_nav']
            _v['hs300'] = fund_dict[_i - _z][1]['hs300']
            break
        if 'unit_nav' not in _v:
            continue
        detail_unit_nav[_date] = _v['unit_nav']
        detail_acc_nav[_date] = _v['acc_nav']
        detail_hs300[_date] = _v['hs300']
        if 'size' in _v:
            result[_date] = {**_v}
            if 'alpha' not in _v:
                for j in range(1, _i):
                    if 'alpha' in fund_dict[_i - j][1]:
                        result[_date]['alpha'] = fund_dict[_i - j][1]['alpha']
                        result[_date]['beta'] = fund_dict[_i - j][1]['beta']
                        result[_date]['sharp_ratio'] = fund_dict[_i - j][1]['sharp_ratio']
                        result[_date]['information_ratio'] = fund_dict[_i - j][1]['information_ratio']
                        result[_date]['max_drop_down'] = fund_dict[_i - j][1]['max_drop_down']
                        break
            if 'holding' not in _v:
                _found = False
                for _z in range(-30, 30):
                    if _i - _z < 0 or _i - _z >= len(fund_dict):
                        continue
                    if 'holding' not in fund_dict[_i - _z][1]:
                        continue
                    _found = True
                    result[_date]['holding'] = fund_dict[_i - _z][1]['holding']
                    result[_date]['holding_values'] = fund_dict[_i - _z][1]['holding_values']
                    break
            result[_date]['detail_unit_navs'] = detail_unit_nav
            result[_date]['detail_acc_navs'] = detail_acc_nav
            result[_date]['detail_hs300s'] = detail_hs300
            detail_unit_nav = {}
            detail_acc_nav = {}
            detail_hs300 = {}
    for _record in fund['manager_records']:
        for _date, _ in result.items():
            if int(_record['start_date']) <= int(_date) <= int(_record['end_date']):
                if 'manager_ids' not in result[_date]:
                    result[_date]['manager_ids'] = {}
                result[_date]['manager_ids'][_record['id']] = _record['title']

    new_result = {}
    pre_value = None
    last_date = None
    for _date, _value in result.items():
        if int(_date) < 20100930:
            continue
        if (_value['stock'] + _value['bond'] + _value['cash'] + _value['other']) == 0.0:
            return None
        if _date[4:] not in ['0331', '0630', '0930', '1231']:
            pre_value = _value
            continue
        if pre_value is not None:
            temp = {}
            for _d, _v in pre_value['detail_unit_navs'].items():
                temp[_d] = _v
            for _d, _v in _value['detail_unit_navs'].items():
                temp[_d] = _v
            _value['detail_unit_navs'] = temp
            temp = {}
            for _d, _v in pre_value['detail_acc_navs'].items():
                temp[_d] = _v
            for _d, _v in _value['detail_acc_navs'].items():
                temp[_d] = _v
            _value['detail_acc_navs'] = temp
            temp = {}
            for _d, _v in pre_value['detail_hs300s'].items():
                temp[_d] = _v
            for _d, _v in _value['detail_hs300s'].items():
                temp[_d] = _v
            _value['detail_hs300s'] = temp
            pre_value = None
        new_result[_date] = _value
        last_date = _date
    if len(new_result) == 1 and last_date[4:] not in ['0331', '0630', '0930', '1231']:
        return None
    for i, (_date, _value) in enumerate(new_result.items()):
        if 'manager_ids' not in _value:
            return None
        if 'holding' not in _value:
            return None
        if 'information_ratio' not in _value or _value['information_ratio'] < -20:
            return None
        if 'alpha' not in _value or _value['alpha'] > 3.3:
            return None
        if 'beta' not in _value or _value['beta'] < -10 or _value['beta'] > 2:
            return None
        if (_date[4:] in ['0331', '0930'] and len(_value) != 19) or (
                _date[4:] in ['0630', '1231'] and len(_value) != 20):
            return None
    new_result_list = list(new_result.items())
    for i, (_date, _value) in enumerate(new_result.items()):
        _value['risk'] = np.std(list(_value['detail_unit_navs'].values()), ddof=0)
        if _value['risk'] > 2:
            return None
        pre_nav = None
        temp = {}
        for _d, _v in _value['detail_unit_navs'].items():
            if pre_nav is None:
                temp[_d] = 0
            else:
                temp[_d] = (_v - pre_nav) / pre_nav
            pre_nav = _v
        _value['detail_change_rate'] = temp
        detail_unit_navs_list = list(_value['detail_unit_navs'].items())
        _value['one_quarter_return'] = detail_unit_navs_list[-1][1] / detail_unit_navs_list[0][1] - 1
        # if _value['one_quarter_return'] > 1.2:
        #     return None
        detail_hs300s_list = list(_value['detail_hs300s'].items())
        _value['one_quarter_hs300_return'] = detail_hs300s_list[-1][1] / detail_hs300s_list[0][1] - 1
        if i < 3:
            continue
        pre_detail_unit_navs_list = list(new_result_list[i - 3][1]['detail_unit_navs'].items())
        pre_detail_hs300s_list = list(new_result_list[i - 3][1]['detail_hs300s'].items())
        _value['one_year_return'] = detail_unit_navs_list[-1][1] / pre_detail_unit_navs_list[0][1] - 1
        _value['one_year_hs300_return'] = detail_hs300s_list[-1][1] / pre_detail_hs300s_list[0][1] - 1
        if i < 11:
            continue
        pre_detail_unit_navs_list = list(new_result_list[i - 11][1]['detail_unit_navs'].items())
        pre_detail_hs300s_list = list(new_result_list[i - 11][1]['detail_hs300s'].items())
        _value['three_year_return'] = detail_unit_navs_list[-1][1] / pre_detail_unit_navs_list[0][1] - 1
        _value['three_year_hs300_return'] = detail_hs300s_list[-1][1] / pre_detail_hs300s_list[0][1] - 1
    return new_result


print('saving fund')
_len = len(fund_files)
for _i, file in enumerate(fund_files):
    if '159946.json' == file:
        continue
    v = get_fund(file)
    if v is None:
        continue
    with open(project_path + '/data/view_funds/' + file, 'w', encoding='UTF-8') as wp:
        json.dump(v, wp)
    print('\rsaving fund {}/{} {:.2f}%'.format(_i + 1, _len, (_i + 1) * 100 / _len), end='')
print()
print('over')
