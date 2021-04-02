import os
import json
from collections import defaultdict
from datetime import datetime

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'

fund_files = os.listdir(project_path + '/data/view_funds')
with open(project_path + '/data/dictionary/manager_dict.json', 'r', encoding='UTF-8') as fp:
    manager_dict = json.load(fp)


def get_fund_feature(file):
    fund_dict = defaultdict(dict)
    with open(project_path + '/data/view_funds/' + file, 'r', encoding='UTF-8') as rp:
        view_fund = json.load(rp)
    pre_instl_weight = None
    for _date, _value in view_fund.items():
        if pre_instl_weight is None and 'instl_weight' in _value:
            pre_instl_weight = _value['instl_weight']
        if pre_instl_weight is not None and 'instl_weight' not in _value:
            view_fund[_date]['instl_weight'] = pre_instl_weight
        _value.pop('holding')
        _value.pop('holding_values')
        _value.pop('detail_acc_navs')
        _value.pop('acc_nav')
        _value.pop('detail_change_rate')
        view_fund[_date]['one_quarter_car'] = _value['one_quarter_return'] - _value['one_quarter_hs300_return']
        if 'one_year_return' in _value:
            view_fund[_date]['one_year_car'] = _value['one_year_return'] - _value['one_year_hs300_return']
        if 'three_year_return' in _value:
            view_fund[_date]['three_year_car'] = _value['three_year_return'] - _value['three_year_hs300_return']
        for m_id, _ in _value['manager_ids'].items():
            t = (datetime.strptime(_date, '%Y%m%d') - datetime.strptime(manager_dict[m_id]['start_date'],
                                                                        '%Y%m%d')).days
            _value['manager_ids'][m_id] = {'name': _, 'days': t}
        fund_dict[_date] = _value
    pre_instl_weight = None
    for _date, _value in reversed(list(fund_dict.items())):
        if pre_instl_weight is None or 'instl_weight' in _value:
            pre_instl_weight = _value['instl_weight']
        if pre_instl_weight is not None and 'instl_weight' not in _value:
            fund_dict[_date]['instl_weight'] = pre_instl_weight
    return fund_dict


print('saving fund')
_len = len(fund_files)
for _i, file in enumerate(fund_files):
    v = get_fund_feature(file)
    with open(project_path + '/data/fund_features/' + file, 'w', encoding='UTF-8') as wp:
        json.dump(v, wp)
    print('\rsaving fund {}/{} {:.2f}%'.format(_i + 1, _len, (_i + 1) * 100 / _len), end='')
print()
print('over')
