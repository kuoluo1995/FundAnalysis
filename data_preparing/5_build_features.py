import os
import json
from collections import defaultdict

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'

fund_files = os.listdir(project_path + '/data/view_funds')


def get_fund_feature(file):
    fund_dict = defaultdict(dict)
    with open(project_path + '/data/view_funds/' + file, 'r', encoding='UTF-8') as rp:
        view_fund = json.load(rp)
    pre_date = None
    for _date, _value in view_fund.items():
        if _date[4:] not in ['0331', '0630', '0930', '1231']:
            pre_date = _value
            print(file)
            continue
        if pre_date is not None:
            temp = dict()
            for _d, _v in pre_date['detail_unit_navs'].items():
                temp[_d] = _v
            for _d, _v in _value['detail_unit_navs'].items():
                temp[_d] = _v
            _value['detail_unit_navs'] = temp
        if 'instl_weight' in _value:
            _value.pop('instl_weight')
            _value.pop('retail_weight')
        _value.pop('holding')
        _value.pop('holding_values')
        _value.pop('detail_acc_navs')
        _value.pop('detail_hs300s')
        fund_dict[_date] = _value
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
