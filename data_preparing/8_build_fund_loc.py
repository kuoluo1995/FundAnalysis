import json
import os
import sys

import numpy as np

sys.path.append('/home/kuoluo/projects/FundAnalysis/')
from tools import normal_tool
from models import pca, tsne

project_path = '/home/kuoluo/projects/FundAnalysis'
fund_files = os.listdir(project_path + '/data/fund_features')
fund_dict = {}
dates = set()
_len = len(fund_files)
for i, _file in enumerate(fund_files):
    with open(project_path + '/data/fund_features/' + _file, 'r', encoding='UTF-8') as rp:
        fund = json.load(rp)
    temp = {}
    for _date, _value in fund.items():
        dates.add(_date)
        _value.pop('hs300')
        _value.pop('unit_nav')
        _value.pop('detail_unit_navs')
        _value.pop('detail_hs300s')
        _value.pop('one_quarter_car')
        if 'one_year_return' in _value:
            _value.pop('one_year_car')
        else:
            _value['one_year_return'] = 0
            _value['one_year_hs300_return'] = 0
        if 'three_year_return' in _value:
            _value.pop('three_year_car')
        else:
            _value['three_year_return'] = 0
            _value['three_year_hs300_return'] = 0
        temp[_date] = _value
    print('\rread fund {}/{} {:.2f}%'.format(i + 1, _len, (i + 1) * 100 / _len), end='')
    if len(temp) > 0:
        fund_dict[_file[:-5]] = temp
max_min_dict = normal_tool.get_max_min_funds(fund_dict, {'manager_ids'})
fund_dict = normal_tool.get_normal_funds(fund_dict, max_min_dict)
init_fund_data = []
init_class = []
dates = sorted(list(dates), key=lambda v: int(v))

for _date in dates:
    for f_id, _values in fund_dict.items():
        if _date not in _values:
            continue
        x = []
        y = []
        for _key, _v in _values[_date].items():
            if _key != 'manager_ids':
                x.append(_v['norm'])
            else:
                for m_id, _ in _v.items():
                    y.append(m_id)
        init_fund_data.append(x)
        init_class.append(y)
data_2d = tsne.train(np.array(init_fund_data))
result = {}
manager_fund = {}
_len = len(dates)
_k = 0
for _i, _da in enumerate(dates):
    result[_da] = {}
    manager_fund[_da] = {}
    for f_id, _values in fund_dict.items():
        if _da not in _values:
            continue
        result[_da][f_id] = {'loc': (float(data_2d[_k][0]), float(data_2d[_k][1])), 'manager_ids': init_class[_k]}
        for m_id in init_class[_k]:
            if m_id not in manager_fund[_da]:
                manager_fund[_da][m_id] = list()
            manager_fund[_da][m_id].append(f_id)
        _k += 1
    print('\rkpca fund {}/{} {:.2f}%'.format(_i + 1, _len, (_i + 1) * 100 / _len), end='')
manager_fund = {_da: {m_id: list(_list) for m_id, _list in _values.items()} for _da, _values in manager_fund.items()}
with open(project_path + '/data/dictionary/fund_loc.json', 'w', encoding='UTF-8') as wp:
    json.dump(result, wp)
with open(project_path + '/data/dictionary/manager2fund.json', 'w', encoding='UTF-8') as wp:
    json.dump(manager_fund, wp)
print('over')
