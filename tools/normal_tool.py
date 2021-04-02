import numpy as np
from server import common


def get_max_min_feature(features, keys):
    max_min_dict = dict()
    for f_id, feature in features.items():
        for key in keys:
            if key not in max_min_dict:
                max_min_dict[key] = {'min': feature[key], 'max': feature[key]}
            if key not in feature:
                continue
            if feature[key] < max_min_dict[key]['min']:
                max_min_dict[key]['min'] = feature[key]
            if abs(feature[key]) > max_min_dict[key]['max']:
                max_min_dict[key]['max'] = abs(feature[key]) if abs(feature[key]) != 0 else 0.0001
    return max_min_dict


def get_normal_feature(features, max_min_dict):
    for f_id, feature in features.items():
        for key, min_max in max_min_dict.items():
            if key not in feature:
                feature[key] = {'norm': 0, 'value': 0}
                continue
            if min_max['min'] <= 0:
                if feature[key] == 0:
                    feature[key] = {'norm': feature[key], 'value': feature[key]}
                elif feature[key] < 0:
                    feature[key] = {'norm': feature[key] / min_max['max'] - 0.1, 'value': feature[key]}
                else:
                    feature[key] = {'norm': feature[key] / min_max['max'] + 0.1, 'value': feature[key]}
            else:
                if min_max['max'] - min_max['min'] == 0:
                    feature[key] = {'norm': 1.1, 'value': feature[key]}
                else:
                    feature[key] = {'norm': (feature[key] - min_max['min']) / (min_max['max'] - min_max['min']) + 0.1,
                                    'value': feature[key]}
    return features


def get_max_min_funds(funds, no_keys):
    max_min_dict = dict()
    for f_id, fund in funds.items():
        for _date, _values in fund.items():
            for _name, _value in _values.items():
                if _name in no_keys:
                    continue
                if type(_value) is not dict:
                    if _name not in max_min_dict:
                        max_min_dict[_name] = {'min': _value, 'max': _value}
                    if max_min_dict[_name]['max'] < abs(_value):
                        max_min_dict[_name]['max'] = abs(_value) if abs(_value) != 0 else 0.0001
                    if _value < max_min_dict[_name]['min']:
                        max_min_dict[_name]['min'] = _value
                else:
                    for _d, _v in _value.items():
                        if _name not in max_min_dict:
                            max_min_dict[_name] = {'min': _v, 'max': _v}
                        if max_min_dict[_name]['max'] < _v:
                            max_min_dict[_name]['max'] = _v if abs(_v) != 0 else 0.0001
                        if _v < max_min_dict[_name]['min']:
                            max_min_dict[_name]['min'] = _v
    return max_min_dict


def get_normal_funds(funds, max_min_dict):
    for f_id, fund in funds.items():
        for _date, _values in fund.items():
            for key, min_max in max_min_dict.items():
                if type(_values[key]) is not dict:
                    if key in _values:
                        if min_max['min'] <= 0:
                            if _values[key] == 0:
                                _values[key] = {'norm': _values[key], 'value': _values[key]}
                            elif _values[key] < 0:
                                _values[key] = {'norm': _values[key] / min_max['max'] - 0.1, 'value': _values[key]}
                            else:
                                _values[key] = {'norm': _values[key] / min_max['max'] + 0.1, 'value': _values[key]}
                        else:
                            if min_max['max'] - min_max['min'] == 0:
                                _values[key] = {'norm': 1.1, 'value': _values[key]}
                            else:
                                _values[key] = {
                                    'norm': (_values[key] - min_max['min']) / (min_max['max'] - min_max['min']) + 0.1,
                                    'value': _values[key]}
                    if 'one_quarter_return' == key:
                        _values['one_quarter_hs300_return'] = {
                            'norm': _values['one_quarter_hs300_return'] / min_max['max'],
                            'value': _values['one_quarter_hs300_return']}
                        if _values['one_quarter_hs300_return']['norm'] > 0:
                            _values['one_quarter_hs300_return']['norm'] += 0.1
                        elif _values['one_quarter_hs300_return']['norm'] < 0:
                            _values['one_quarter_hs300_return']['norm'] -= 0.1
                    if 'one_year_return' == key:
                        if min_max['max'] != 0:
                            _values['one_year_hs300_return'] = {
                                'norm': _values['one_year_hs300_return'] / min_max['max'],
                                'value': _values['one_year_hs300_return']}
                        else:
                            _values['one_year_hs300_return'] = {'norm': 0, 'value': _values['one_year_hs300_return']}
                        if _values['one_year_hs300_return']['norm'] > 0:
                            _values['one_year_hs300_return']['norm'] += 0.1
                        elif _values['one_year_hs300_return']['norm'] < 0:
                            _values['one_year_hs300_return']['norm'] -= 0.1
                    if 'three_year_return' == key:
                        if min_max['max'] != 0:
                            _values['three_year_hs300_return'] = {
                                'norm': _values['three_year_hs300_return'] / min_max['max'],
                                'value': _values['three_year_hs300_return']}
                        else:
                            _values['three_year_hs300_return'] = {'norm': 0,
                                                                  'value': _values['three_year_hs300_return']}
                        if _values['three_year_hs300_return']['norm'] > 0:
                            _values['three_year_hs300_return']['norm'] += 0.1
                        elif _values['three_year_hs300_return']['norm'] < 0:
                            _values['three_year_hs300_return']['norm'] -= 0.1
                elif key not in ['one_quarter_hs300_return', 'one_year_hs300_return', 'three_year_hs300_return']:
                    for _d, _v in _values[key].items():
                        if _v == 0:
                            _values[key][_d] = {'norm': _v, 'value': _v}
                        elif _v < 0:
                            _values[key][_d] = {'norm': _v / abs(min_max['min']), 'value': _v}
                        else:
                            _values[key][_d] = {'norm': _v / min_max['max'], 'value': _v}
                        if key == 'detail_car':
                            temp = _values[key][_d]['norm'] * 22
                            if _values[key][_d]['norm'] >= 0:
                                if temp > 24:
                                    temp = 24
                                _values[key][_d]['color'] = common.yellow2red[int(temp) + 25]
                            else:
                                if temp < -25:
                                    temp = -25
                                _values[key][_d]['color'] = common.yellow2green[int(temp) + 25]
                            _values[key][_d]['color'] = str(_values[key][_d]['color'])
                        if _v > 0:
                            _values[key][_d]['norm'] += 0.2
                        elif _v < 0:
                            _values[key][_d]['norm'] -= 0.2
    return funds


def get_avg_funds_attribute(funds, no_keys):
    key_dict = {}
    for f_id, fund in funds.items():
        key_dict[f_id] = {}
        for _date, _values in fund.items():
            for key, _v in _values.items():
                if key in no_keys:
                    continue
                if key == 'holding_values':
                    if key not in key_dict[f_id]:
                        key_dict[f_id][key] = {}
                    for _name, _sector in _v.items():
                        if _name not in key_dict[f_id][key]:
                            key_dict[f_id][key][_name] = list()
                        key_dict[f_id][key][_name].append(_sector)
                if key == 'manager_ids':
                    for m_id in _v:
                        if 'manager_ids' not in key_dict[f_id]:
                            key_dict[f_id]['manager_ids'] = set()
                        key_dict[f_id]['manager_ids'].add(m_id)
                if 'norm' in _v:
                    if key not in key_dict[f_id]:
                        key_dict[f_id][key] = {'norm': list(), 'value': list()}
                    key_dict[f_id][key]['norm'].append(_v['norm'])
                    key_dict[f_id][key]['value'].append(_v['value'])
            _values.pop('manager_ids')
    for f_id, key_values in key_dict.items():
        for key, values in key_values.items():
            if key == 'holding_values':
                _sum = 0
                for _name, _sectors in values.items():
                    key_dict[f_id][key][_name] = np.mean(_sectors)
                    _sum += key_dict[f_id][key][_name]
                for _name, _sectors in values.items():
                    key_dict[f_id][key][_name] /= _sum
                continue
            if key == 'manager_ids':
                key_dict[f_id][key] = list(values)
                continue
            key_dict[f_id][key]['norm'] = np.mean(values['norm'])
            key_dict[f_id][key]['value'] = np.mean(values['value'])
    return key_dict


def update_normal_type(funds):
    for f_id, fund in funds.items():
        for _date, _values in fund.items():
            for _key, _value in _values.items():
                if type(_value) == float:
                    _values[_key] = {'norm': _value, 'value': _value}
    return funds
