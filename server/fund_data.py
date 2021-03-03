import json
import sys
import numpy as np

sys.path.append('/home/kuoluo/projects/FundAnalysis/')

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
    max_return = None
    max_risk = None
    max_sharp_ratio = None
    max_information_ratio = None
    max_alpha = None
    max_beta = None
    max_size = min_size = None
    max_detail_return = None
    max_detail_car_return = None
    fund_dict = {}
    print('\r' + fund_ids[0], end='')
    attributes_dict = {}
    for f_id in fund_ids:
        fund = common.get_view_fund_json(f_id)
        pre_unit_nav = None
        pre_hs300 = None
        attributes_dict[f_id] = {}
        last_unit_nav = None
        last_hs300 = None
        for _date, _value in fund.items():
            if max_return is None or max_return < abs(_value['nav_return']):
                max_return = abs(_value['nav_return'])
            if max_risk is None or max_risk < _value['risk']:
                max_risk = _value['risk']
            if max_sharp_ratio is None or max_sharp_ratio < abs(_value['sharp_ratio']):
                max_sharp_ratio = abs(_value['sharp_ratio'])
            if max_information_ratio is None or max_information_ratio < abs(_value['information_ratio']):
                max_information_ratio = abs(_value['information_ratio'])
            if max_alpha is None or max_alpha < abs(_value['alpha']):
                max_alpha = abs(_value['alpha'])
            if max_beta is None or max_beta < abs(_value['beta']):
                max_beta = abs(_value['beta'])
            if max_size is None or max_size < _value['size']:
                max_size = _value['size']
            if min_size is None or min_size > _value['size']:
                min_size = _value['size']
            detail_nav_return = {}
            detail_car = {}
            for _d, _nav in _value['detail_unit_navs'].items():
                if int(start_date) <= int(_d) <= int(end_date):
                    if pre_unit_nav is None:
                        pre_unit_nav = _value['detail_unit_navs'][_d]
                        pre_hs300 = _value['detail_hs300s'][_d]
                    detail_nav_return[_d] = _value['detail_unit_navs'][_d] / pre_unit_nav - 1
                    detail_hs300_return = _value['detail_hs300s'][_d] / pre_hs300 - 1
                    detail_car[_d] = detail_nav_return[_d] - detail_hs300_return
                    if max_detail_return is None or max_detail_return < abs(detail_nav_return[_d]):
                        max_detail_return = abs(detail_nav_return[_d])
                    if max_detail_car_return is None or max_detail_car_return < abs(detail_car[_d]):
                        max_detail_car_return = abs(detail_car[_d])
                    last_unit_nav = _value['detail_unit_navs'][_d]
                    last_hs300 = _value['detail_hs300s'][_d]
            fund[_date]['detail_nav_return'] = detail_nav_return
            fund[_date]['detail_car'] = detail_car
            fund[_date].pop('hs300')
            fund[_date].pop('unit_nav')
            fund[_date].pop('acc_nav')
            fund[_date].pop('detail_acc_navs')
            fund[_date].pop('detail_hs300s')
            fund[_date].pop('holding_values')
        attributes_dict[f_id]['return'] = last_unit_nav / pre_unit_nav - 1
        attributes_dict[f_id]['car'] = last_unit_nav / pre_unit_nav - last_hs300 / pre_hs300
        fund_dict[f_id] = fund
    result = {}
    for f_id, fund in fund_dict.items():
        attributes_dict[f_id].update({'stock': list(), 'bond': list(), 'cash': list(), 'other': list(), 'size': list(),
                                      'alpha': list(), 'beta': list(), 'sharp_ratio': list(), 'max_drop_down': list(),
                                      'information_ratio': list(), 'risk': list(), 'instl_weight': list()})
        temp_fund = {}
        for _date, _value in fund.items():
            temp_fund[_date] = {**_value}
            attributes_dict[f_id]['stock'].append(temp_fund[_date]['stock'])
            attributes_dict[f_id]['bond'].append(temp_fund[_date]['bond'])
            attributes_dict[f_id]['cash'].append(temp_fund[_date]['cash'])
            attributes_dict[f_id]['other'].append(temp_fund[_date]['other'])
            if 'instl_weight' in temp_fund[_date]:
                attributes_dict[f_id]['instl_weight'].append(temp_fund[_date]['instl_weight'])
            temp_fund[_date]['nav_return'] = temp_fund[_date]['nav_return'] / max_return
            attributes_dict[f_id]['risk'].append(temp_fund[_date]['risk'] / max_risk)
            if temp_fund[_date]['risk'] == 0:
                temp_fund[_date]['risk'] = 0
            else:
                temp_fund[_date]['risk'] = temp_fund[_date]['risk'] / max_risk + 1
            temp_fund[_date]['sharp_ratio'] = temp_fund[_date]['sharp_ratio'] / max_sharp_ratio
            attributes_dict[f_id]['sharp_ratio'].append(temp_fund[_date]['sharp_ratio'])
            temp_fund[_date]['information_ratio'] = temp_fund[_date]['information_ratio'] / max_information_ratio
            attributes_dict[f_id]['information_ratio'].append(temp_fund[_date]['information_ratio'])
            temp_fund[_date]['alpha'] = temp_fund[_date]['alpha'] / max_alpha
            attributes_dict[f_id]['alpha'].append(temp_fund[_date]['alpha'])
            temp_fund[_date]['beta'] = temp_fund[_date]['beta'] / max_beta
            attributes_dict[f_id]['beta'].append(temp_fund[_date]['beta'])
            temp_fund[_date]['size'] = (temp_fund[_date]['size'] - min_size) / (max_size - min_size) + 0.2
            attributes_dict[f_id]['size'].append(temp_fund[_date]['size'] - 0.2)
            detail_nav_return = {}
            detail_car = {}
            for _d, _nav in _value['detail_unit_navs'].items():
                if int(start_date) <= int(_d) <= int(end_date):
                    detail_nav_return[_d] = _value['detail_unit_navs'][_d] / max_detail_return
                    detail_car[_d] = _value['detail_car'][_d] / max_detail_car_return
            temp_fund[_date]['detail_nav_return'] = detail_nav_return
            temp_fund[_date]['detail_car'] = detail_car
            attributes_dict[f_id]['max_drop_down'].append(temp_fund[_date]['max_drop_down'])
        result[f_id] = temp_fund
    for f_id, _attribute in attributes_dict.items():
        for _name, _v in _attribute.items():
            if _name == 'return' or _name == 'car':
                continue
            attributes_dict[f_id][_name] = np.mean(_v)
    return result, attributes_dict


def get_fund_t_sne(fund_ids):
    init_fund_data = {}
    max_return = None
    max_risk = None
    max_sharp_ratio = None
    max_information_ratio = None
    max_alpha = None
    max_beta = None
    max_size = min_size = None
    dates = set()
    funds = {}
    for f_id in fund_ids:
        fund = common.get_feature_fund_json(f_id)
        for _date, _value in fund.items():
            _value.pop('hs300')
            _value.pop('detail_unit_navs')
            dates.add(_date)
            fund[_date] = _value
            init_fund_data[f_id] = _value
            if max_return is None or max_return < abs(_value['nav_return']):
                max_return = abs(_value['nav_return'])
            if max_risk is None or max_risk < _value['risk']:
                max_risk = _value['risk']
            if max_sharp_ratio is None or max_sharp_ratio < abs(_value['sharp_ratio']):
                max_sharp_ratio = abs(_value['sharp_ratio'])
            if max_information_ratio is None or max_information_ratio < abs(_value['information_ratio']):
                max_information_ratio = abs(_value['information_ratio'])
            if max_alpha is None or max_alpha < abs(_value['alpha']):
                max_alpha = abs(_value['alpha'])
            if max_beta is None or max_beta < abs(_value['beta']):
                max_beta = abs(_value['beta'])
            if max_size is None or max_size < _value['size']:
                max_size = _value['size']
            if min_size is None or min_size > _value['size']:
                min_size = _value['size']
        funds[f_id] = fund
    x, clasz = tsne.get_fund_feature(init_fund_data, max_return, max_risk, max_sharp_ratio, max_information_ratio,
                                     max_alpha, max_beta, max_size, min_size)
    num_fund = len(fund_ids)
    y, dy, iy, gains = tsne.get_y(num_fund, 2)
    p = tsne.get_p(np.array(x))
    data_2d, dy, iy, gains = tsne.t_sne(p, num_fund, y, dy, iy, gains, 2)
    dates = sorted(list(dates), key=lambda v: int(v), reverse=True)
    result = {}
    pre_index_funds = set()
    pre_date = None
    for _da in dates:
        result[_da] = {}
        x, clasz, index_funds = tsne.update_features(x, clasz, funds, _da, max_return, max_risk, max_sharp_ratio,
                                                     max_information_ratio, max_alpha, max_beta, max_size, min_size)
        p = tsne.get_p(np.array(x))
        data_2d, dy, iy, gains = tsne.t_sne(p, num_fund, y, dy, iy, gains, 2, max_iter=100)
        for i, f_id in index_funds.items():
            result[_da][f_id] = {'loc': (data_2d[i][0], data_2d[i][1]), 'manager_id': clasz[i]}
        if pre_date is None:
            pre_date = _da
            pre_index_funds = set(index_funds.values())
            continue
        appear_funds = pre_index_funds - set(index_funds.values())
        disappear_funds = set(index_funds.values()) - pre_index_funds
        for f_id in appear_funds:
            result[pre_date][f_id]['new'] = True
        for f_id in disappear_funds:
            result[_da][f_id]['delete'] = True
        pre_date = _da
        pre_index_funds = set(index_funds.values())
    return result


def get_fund_ranks(weights):
    fund_ids = common.fund_ids
    funds = {}
    for f_id in fund_ids:
        fund = common.global_fund_features[f_id]
        _sum = 0
        for _name, _v in weights.items():
            _sum += weights[_name] * fund[_name]
        funds[f_id] = _sum
    funds = sorted(funds.items(), key=lambda v: v[1], reverse=True)
    return [i for i, _ in funds]


def get_fund_last_dict(fund_ids, keys):
    fund_list = []
    for f_id in fund_ids:
        temp = {'id': f_id}
        fund = common.get_feature_fund_json(f_id)
        values = list(fund.items())[-1][1]
        for key in keys:
            if 'car' == key:
                temp[key] = values['nav_return'] - values['hs300_return']
            else:
                temp[key] = values[key]
        fund_list.append(temp)
    return fund_list


if __name__ == '__main__':
    result = {}
    pre_f_id = '007590'
    for f_id in common.fund_ids:
        min_start_date, max_end_date = get_fund_time_border([f_id, pre_f_id])
        _ = get_view_fund([f_id, pre_f_id], min_start_date, max_end_date)
        result.update(_)
        pre_f_id = f_id
    project_path = '/home/kuoluo/projects/FundAnalysis'
    for f_id, _value in result.items():
        with open(project_path + '/data/temp/funds/' + f_id + '.json', 'w', encoding='UTF-8') as wp:
            json.dump(_value, wp)
    print('over')
    # weights = {'stock': 1.0, 'bond': 1.0, 'cash': 1.0, 'other': 1.0, 'size': 1.0, 'alpha': 1.0, 'beta': 1.0,
    #            'sharp_ratio': 1.0, 'max_drop_down': 1.0, 'information_ratio': 1.0, 'nav_return': 1.0, 'risk': 1.0,
    #            'instl_weight': 1.0, 'car': 1.0}
    # fund_ids = get_fund_ranks(weights)
    # get_fund_last_dict(fund_ids, list(weights.keys()))
    # m_ids = []
    # for f_id in common.fund_ids[:10]:
    #     m_ids += common.fund_manager_dict[f_id]
    # f_ids = []
    # for m_id in m_ids:
    #     f_ids += common.manager_fund_dict[m_id]
    # f_ids = list(set(f_ids))
    # funds = get_fund_t_sne(f_ids)
    # project_path = 'E:/Projects/PythonProjects/FundAnalysis'
    # with open(project_path + '/data/temp/funds_tsne.json', 'w', encoding='UTF-8') as wp:
    #     json.dump(funds, wp)
    # print('over')
