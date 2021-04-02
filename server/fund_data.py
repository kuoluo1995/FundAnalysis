import json
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append('/home/kuoluo/projects/FundAnalysis/')

from server import common, fund_manager
from models import ranksvm, pca
from tools import normal_tool


def get_fund_time_border(fund_ids):
    min_start_date = None
    max_end_date = None
    for f_id in fund_ids:
        fund = common.get_view_fund_json(f_id)
        dates = list(fund.keys())
        if min_start_date is None or int(dates[0]) < min_start_date:
            min_start_date = int(dates[0])
        if max_end_date is None or max_end_date < int(dates[-1]):
            max_end_date = int(dates[-1])
    return min_start_date, max_end_date


def get_fund_min_time_border(fund_ids):
    max_start_date = None
    min_end_date = None
    for f_id in fund_ids:
        fund = common.get_view_fund_json(f_id)
        dates = list(fund.keys())
        if max_start_date is None or int(dates[0]) > max_start_date:
            max_start_date = int(dates[0])
        if min_end_date is None or min_end_date > int(dates[-1]):
            min_end_date = int(dates[-1])
    return max_start_date, min_end_date


def get_fund_ranks(weights, start_date, end_date, sectors=None):
    fund_ids = common.fund_ids
    rank_funds = {}
    unrank_funds = {}
    manager2fund = {}
    for f_id in fund_ids:
        feature = common.get_feature_fund_json(f_id)
        dates = list(feature.keys())
        if int(start_date) < int(dates[0]) or int(dates[-1]) < int(end_date):
            unrank_funds[f_id] = feature
            continue
        else:
            if sectors is None:
                rank_funds[f_id] = feature
                continue
            else:
                fund = common.get_view_fund_json(f_id)
                sector_set = set(sectors.copy())
                for _date, _value in fund.items():
                    if len(sector_set) == 0:
                        break
                    if int(start_date) <= int(_date) <= int(end_date):
                        for _sector in _value['holding']:
                            if _sector in sector_set:
                                sector_set.remove(_sector)
                if len(sector_set) != 0:
                    unrank_funds[f_id] = feature
                else:
                    rank_funds[f_id] = feature
    for f_id, fund in rank_funds.items():
        key_dict = {_name: list() for _name, _ in weights.items()}
        for _date, _values in fund.items():
            if int(start_date) <= int(_date) <= int(end_date):
                for _name, _v in weights.items():
                    if _name not in _values:
                        continue
                    key_dict[_name].append(_values[_name])
                for m_id, _name in _values['manager_ids'].items():
                    if m_id not in manager2fund:
                        manager2fund[m_id] = set()
                    manager2fund[m_id].add(f_id)
        key_dict = {_name: np.mean(_list) if len(_list) != 0 else 0 for _name, _list in key_dict.items()}
        rank_funds[f_id] = key_dict
    max_min_border = normal_tool.get_max_min_feature(rank_funds, weights.keys())
    rank_funds = normal_tool.get_normal_feature(rank_funds, max_min_border)
    for f_id, feature in rank_funds.items():
        _sum = 0
        for _name, _v in weights.items():
            if _name not in feature:
                continue
            _sum += float(weights[_name]) * feature[_name]['norm']
        feature['score'] = _sum
    rank_funds = sorted(rank_funds.items(), key=lambda v: v[1]['score'], reverse=True)
    manager2fund = {m_id: list(_list) for m_id, _list in manager2fund.items()}
    return rank_funds, manager2fund


def get_view_fund(fund_ids, start_date, end_date):
    fund_dict = {}
    attributes_dict = {}
    date_set = set()
    for f_id in fund_ids:
        fund = common.get_view_fund_json(f_id)
        temp = {}
        for _date, _values in fund.items():
            if int(start_date) > int(_date) or int(end_date) < int(_date):
                continue
            date_set.add(_date)
            detail_nav_return = {}
            detail_car = {}
            detail_change = {}
            pre_unit_nav = None
            pre_hs300 = None
            for _d, _nav in _values['detail_unit_navs'].items():
                if pre_unit_nav is None:
                    pre_unit_nav = _values['detail_unit_navs'][_d]
                    pre_hs300 = _values['detail_hs300s'][_d]
                detail_nav_return[_d] = _values['detail_unit_navs'][_d] / pre_unit_nav - 1
                detail_hs300_return = _values['detail_hs300s'][_d] / pre_hs300 - 1
                detail_car[_d] = detail_nav_return[_d] - detail_hs300_return
                detail_change[_d] = _values['detail_change_rate'][_d]
            _values['detail_car'] = detail_car
            _values['detail_change_rate'] = detail_change
            # _values['detail_return'] = detail_nav_return
            if 'one_year_return' not in _values:
                _values['one_year_return'] = 0
            if 'one_year_hs300_return' not in _values:
                _values['one_year_hs300_return'] = 0
            if 'three_year_return' not in _values:
                _values['three_year_return'] = 0
            if 'three_year_hs300_return' not in _values:
                _values['three_year_hs300_return'] = 0
            _values.pop('hs300')
            _values.pop('unit_nav')
            _values.pop('acc_nav')
            _values.pop('detail_unit_navs')
            _values.pop('detail_acc_navs')
            _values.pop('detail_hs300s')
            # _values.pop('holding_values')
            if 'instl_weight' in _values:
                _values.pop('instl_weight')
            temp[_date] = _values
        if len(temp) > 0:
            fund_dict[f_id] = temp
    max_min_dict = normal_tool.get_max_min_funds(fund_dict,
                                                 {'holding', 'holding_values', 'stock', 'bond', 'cash', 'other',
                                                  'manager_ids', 'one_quarter_hs300_return', 'one_year_hs300_return',
                                                  'three_year_hs300_return'})
    features = normal_tool.get_normal_funds(fund_dict, max_min_dict)
    features = normal_tool.update_normal_type(features)
    attribute_temp = normal_tool.get_avg_funds_attribute(features, {'holding'})
    for f_id, attribute in attribute_temp.items():
        attributes_dict[f_id] = attribute
    dates = sorted(list(date_set), key=lambda v: int(v))
    result = {}
    for f_id, _values in features.items():
        result[f_id] = {}
        for _date in dates:
            if _date not in _values:
                result[f_id][_date] = {}
            else:
                result[f_id][_date] = _values[_date]
    return result, attributes_dict


def get_fund_loc(exist_mid, new_m_ids, start_date, end_date):
    manager2fund = {}
    result = {}
    for _date, managers in common.manager_fund_dict.items():
        if int(start_date) <= int(_date) <= int(end_date):
            for m_id, funds in managers.items():
                if m_id in exist_mid or m_id in new_m_ids:
                    if _date not in manager2fund:
                        manager2fund[_date] = {}
                        result[_date] = {}
                    manager2fund[_date][m_id] = funds
                    for f_id in funds:
                        _loc = common.fund_loc_dict[_date][f_id]
                        if m_id in new_m_ids:
                            _loc['other'] = True
                        else:
                            _loc['other'] = False
                        result[_date][f_id] = _loc
    return result, manager2fund


def get_fund_last_dict(fund_ids):
    fund_list = []
    for i, f_id in enumerate(fund_ids):
        temp = {'key': i + 1, 'id': f_id}
        fund = common.get_feature_fund_json(f_id)
        values = list(fund.items())[-1][1]
        values.pop('detail_unit_navs')
        values.pop('detail_hs300s')
        values.pop('manager_ids')
        values.pop('hs300')
        values.pop('one_quarter_hs300_return')
        if 'one_year_hs300_return' in values:
            values.pop('one_year_hs300_return')
        if 'three_year_hs300_return' in values:
            values.pop('three_year_hs300_return')
        for key, _value in values.items():
            if type(values[key]) is float:
                temp[key] = round(values[key], 4)
            else:
                temp[key] = values[key]
        fund_list.append(temp)
    return fund_list


def update_fund_weights(weight, pair_result, start_date, end_date):
    feature_dict = {}
    for _pair in pair_result:
        f_ids = set()
        for f_id in _pair.keys():
            if f_id not in feature_dict:
                feature = common.get_feature_fund_json(f_id)
                cols = {}
                for _name, _v in weight.items():
                    for _date, _ in feature.items():
                        if int(start_date) < int(_date) < int(end_date):
                            if _name not in cols:
                                cols[_name] = 0
                            if _name in _:
                                cols[_name] += float(_v) * feature[_date][_name]
                            else:
                                cols[_name] += 0
                feature_dict[f_id] = cols
            f_ids.add(f_id)
    x, y, rows = ranksvm.build_train_data(feature_dict, weight, pair_result)
    rsvm = ranksvm.train_by_pair_data(x, y)
    scores = ranksvm.predict(rsvm, rows)
    weight = ranksvm.updata_weight(weight, rows, scores)
    return weight


if __name__ == '__main__':
    # project_path = 'E:/Projects/PythonProjects/FundAnalysis'
    project_path = '/home/kuoluo/projects/FundAnalysis'
    weights = {'one_quarter_return': 1.0, 'one_year_return': 1.0, 'three_year_return': 1.0, 'max_drop_down': 0.0,
               'risk': 1.0, 'sharp_ratio': 0.0, 'information_ratio': 0.0, 'alpha': 0.0, 'beta': 0.0, 'size': 1.0,
               'instl_weight': 0.0}
    pairs = [{'001740': 0, '001790': 1}, {'001790': 0, '000717': 1, '003834': 0},
             {'000717': 0, '003834': 1}, {'003834': 0, '005911': 1}, {'003745': 0, '002939': 1}]
    f_ids = set()
    for _pair in pairs:
        f_ids.update(_pair.keys())
    start_date, end_date = get_fund_min_time_border(f_ids)
    # sectors = ['计算机', '医药生物']
    sectors = None
    # ranks, manager2fund = get_fund_ranks(weights, start_date, end_date, sectors)
    print('over')
    # detail, last = get_view_fund(f_ids, start_date, end_date)
    # detail, last = get_view_fund([list(f_ids)[0]], start_date, end_date)
    exist_mid, new_m_ids = fund_manager.get_manager_ranks(f_ids, weights, start_date, end_date, 10)
    all_m_ids = new_m_ids + exist_mid
    managers = fund_manager.get_manager_feature(all_m_ids, start_date, end_date)
    for m_id in new_m_ids:
        managers[m_id]['other'] = True
    funds, manager_funds = get_fund_loc(exist_mid, new_m_ids, start_date, end_date)
    weights = update_fund_weights(weights, pairs, start_date, end_date)
    print('over')
