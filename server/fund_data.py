import json
import sys
from collections import defaultdict
import numpy as np

sys.path.append('/home/kuoluo/projects/FundAnalysis/')

from tools import show_tool
from server import common
from models import tsne


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


def get_view_fund(fund_ids, start_date, end_date):
    max_size = None
    max_alpha = min_alpha = None
    max_beta = min_beta = None
    max_sharp_ratio = min_sharp_ratio = None
    max_information_ratio = min_information_ratio = None
    max_risk = min_risk = None
    fund_dict = {}
    print('\r' + fund_ids[0], end='')
    for f_id in fund_ids:
        fund = common.get_view_fund_json(f_id)
        for _date, _value in fund.items():
            if max_size is None or max_size < _value['size']:
                max_size = _value['size']
            if max_alpha is None or max_alpha < _value['alpha']:
                max_alpha = _value['alpha']
            if max_beta is None or max_beta < _value['beta']:
                max_beta = _value['beta']
            if max_sharp_ratio is None or max_sharp_ratio < _value['sharp_ratio']:
                max_sharp_ratio = _value['sharp_ratio']
            if max_information_ratio is None or max_information_ratio < _value['information_ratio']:
                max_information_ratio = _value['information_ratio']
            if max_risk is None or max_risk < _value['risk']:
                max_risk = _value['risk']
            if min_alpha is None or min_alpha > _value['alpha']:
                min_alpha = _value['alpha']
            if min_beta is None or min_beta > _value['beta']:
                min_beta = _value['beta']
            if min_sharp_ratio is None or min_sharp_ratio > _value['sharp_ratio']:
                min_sharp_ratio = _value['sharp_ratio']
            if min_information_ratio is None or min_information_ratio > _value['information_ratio']:
                min_information_ratio = _value['information_ratio']
            if min_risk is None or min_risk > _value['risk']:
                min_risk = _value['risk']
        fund_dict[f_id] = fund
    result = {}
    for f_id, fund in fund_dict.items():
        pre_unit_nav = None
        pre_hs300 = None
        temp_fund = {}
        max_unit_nav = None
        min_unit_nav = None
        max_return = None
        min_return = None
        for _date, _value in fund.items():
            temp_fund[_date] = {**_value}
            temp_fund[_date]['size'] = temp_fund[_date]['size'] / max_size
            temp_fund[_date]['alpha'] = (temp_fund[_date]['alpha'] - min_alpha) / (max_alpha - min_alpha)
            temp_fund[_date]['beta'] = (temp_fund[_date]['beta'] - min_beta) / (max_beta - min_beta)
            temp_fund[_date]['sharp_ratio'] = (temp_fund[_date]['sharp_ratio'] - min_sharp_ratio) / (
                    max_sharp_ratio - min_sharp_ratio)
            temp_fund[_date]['information_ratio'] = (temp_fund[_date]['information_ratio'] - min_information_ratio) / (
                    max_information_ratio - min_information_ratio)
            temp_fund[_date]['risk'] = (temp_fund[_date]['risk'] - min_risk) / (max_size - min_risk)
            detail_nav_return = {}
            detail_hs300_return = {}
            detail_car = {}
            for _d, _nav in _value['detail_unit_navs'].items():
                if int(start_date) <= int(_d) <= int(end_date):
                    if pre_unit_nav is None:
                        pre_unit_nav = _value['detail_unit_navs'][_d]
                        pre_hs300 = _value['detail_hs300s'][_d]
                    detail_nav_return[_d] = _value['detail_unit_navs'][_d] / pre_unit_nav - 1
                    detail_hs300_return[_d] = _value['detail_hs300s'][_d] / pre_hs300 - 1
                    detail_car[_d] = detail_nav_return[_d] - detail_hs300_return[_d]
                    if min_return is None or min_return > detail_car[_d]:
                        min_return = detail_car[_d]
                    if max_return is None or max_return < detail_car[_d]:
                        max_return = detail_car[_d]
                    if min_unit_nav is None or min_unit_nav > detail_nav_return[_d]:
                        min_unit_nav = detail_nav_return[_d]
                    if max_unit_nav is None or max_unit_nav < detail_nav_return[_d]:
                        max_unit_nav = detail_nav_return[_d]
            temp_fund[_date].pop('hs300')
            temp_fund[_date].pop('unit_nav')
            temp_fund[_date].pop('acc_nav')
            temp_fund[_date].pop('detail_acc_navs')
            temp_fund[_date].pop('detail_hs300s')
            temp_fund[_date].pop('holding_values')
            temp_fund[_date]['detail_hs300_return'] = detail_hs300_return
            temp_fund[_date]['detail_nav_return'] = detail_nav_return
            temp_fund[_date]['detail_car'] = detail_car
        for _date, _value in temp_fund.items():
            for _d, _ in _value['detail_car'].items():
                _value['detail_car'][_d] = (_value['detail_car'][_d] - min_return) / (max_return - min_return)
                _value['detail_nav_return'][_d] = (_value['detail_nav_return'][_d] - min_unit_nav) / (
                        max_unit_nav - min_unit_nav)
        result[f_id] = temp_fund
    return result


def get_fund_t_sne(fund_ids):
    init_fund_data = {}
    max_size = None
    min_nav_len = 100
    dates = set()
    funds = {}
    for f_id in fund_ids:
        fund = common.get_feature_fund_json(f_id)
        for _date, _value in fund.items():
            dates.add(_date)
            if min_nav_len > len(_value['detail_unit_navs']):
                min_nav_len = len(_value['detail_unit_navs'])
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
    dates = sorted(list(dates), key=lambda v: int(v), reverse=True)
    result = {}
    for _da in dates:
        result[_da] = {}
        x, clasz, index_funds = tsne.update_features(x, clasz, funds, _da, max_size, min_nav_len)
        p = tsne.get_p(np.array(x))
        data_2d, dy, iy, gains = tsne.t_sne(p, num_fund, y, dy, iy, gains, 2, max_iter=100)
        for i, f_id in index_funds.items():
            result[_da][f_id] = {'loc': (data_2d[i][0], data_2d[i][1]), 'manager_id': clasz[i]}
    return result


def get_fund_last_dict(fund_ids, keys):
    fund_dict = {}
    for f_id in fund_ids:
        fund_dict[f_id] = {}
        fund = common.get_view_fund_json(f_id)
        values = list(fund.items())[-1][1]
        for key in keys:
            if 'detail' in key:
                fund_dict[f_id][key] = values[key][-1]
            else:
                fund_dict[f_id][key] = values[key]
    return fund_dict


def get_fund_ranks(weights, num_top=20):
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
    funds = sorted(funds.items(), key=lambda v: v[1], reverse=True)
    return funds[:num_top]


if __name__ == '__main__':
    result = {}
    pre_f_id = '007590'
    for f_id in common.fund_ids:
        min_start_date, max_end_date = get_fund_time_border([f_id, pre_f_id])
        _ = get_view_fund([f_id, pre_f_id], min_start_date, max_end_date)
        result.update(_)
        pre_f_id = f_id
    # project_path = '/home/kuoluo/projects/FundAnalysis'
    # for f_id, _value in result.items():
    #     with open(project_path + '/data/temp/funds/' + f_id + '.json', 'w', encoding='UTF-8') as wp:
    #         json.dump(_value, wp)
    # print('over')
    # get_fund_ranks({'stock': 1.0, 'bond': 1.0, 'cash': 1.0, 'other': 1.0, 'size': 1.0, 'alpha': 1.0, 'beta': 1.0,
    #                 'sharp_ratio': 1.0, 'information_ratio': 1.0, 'navs': 1.0, 'risks': 1.0})
    m_ids = []
    for f_id in common.fund_ids[:10]:
        m_ids += common.fund_manager_dict[f_id]
    f_ids = []
    for m_id in m_ids:
        f_ids += common.manager_fund_dict[m_id]
    f_ids = list(set(f_ids))
    funds = get_fund_t_sne(f_ids)
    project_path = 'E:/Projects/PythonProjects/FundAnalysis'
    with open(project_path + '/data/temp/funds_tsne.json', 'w', encoding='UTF-8') as wp:
        json.dump(funds, wp)
    print('over')
