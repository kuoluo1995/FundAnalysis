import json
import os
import numpy as np
from collections import defaultdict

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'
fund_files = os.listdir(project_path + '/data/source')


def get_fund(file):
    fund_dict = defaultdict(dict)
    with open(project_path + '/data/source/' + file, 'r', encoding='UTF-8') as rp:
        fund = json.load(rp)
    risk = []
    for _record in fund['nav']:
        fund_dict[_record['datetime']]['nav'] = _record['unit_net_value']
        if len(risk) >= 90:
            risk.pop(0)
        risk.append(_record['acc_net_value'])
        fund_dict[_record['datetime']]['risk'] = np.std(risk, ddof=0)
    for _record in fund['asset_allocation_records']:
        fund_dict[_record['datetime']]['stock'] = _record['stock']
        fund_dict[_record['datetime']]['bond'] = _record['bond']
        fund_dict[_record['datetime']]['cash'] = _record['cash']
        fund_dict[_record['datetime']]['other'] = _record['other']
        fund_dict[_record['datetime']]['size'] = _record['net_asset']
    for _record in fund['holder_structure']:
        fund_dict[_record['date']]['instl_weight'] = _record['instl_weight'] / 100
        fund_dict[_record['date']]['retail_weight'] = _record['retail_weight'] / 100
    for _record in fund['indicators_records']:
        fund_dict[_record['datetime']]['alpha'] = _record['total_alpha']
        fund_dict[_record['datetime']]['beta'] = _record['total_beta']
        fund_dict[_record['datetime']]['sharp_ratio'] = _record['sharp_ratio']
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

    fund_dict = sorted(fund_dict.items(), key=lambda v: int(v[0]))
    result = {}
    detail_nav = {}
    detail_risk = {}
    for i, (d, _v) in enumerate(fund_dict):
        if 'nav' not in _v:
            continue
        detail_nav[d] = _v['nav']
        detail_risk[d] = _v['risk']
        if 'size' in _v:
            result[d] = {**_v}
            if d == '20180930':
                for j in range(1, i):
                    if 'alpha' in fund_dict[i - j][1]:
                        result[d]['alpha'] = fund_dict[i - j][1]['alpha']
                        result[d]['beta'] = fund_dict[i - j][1]['beta']
                        result[d]['sharp_ratio'] = fund_dict[i - j][1]['sharp_ratio']
                        result[d]['information_ratio'] = fund_dict[i - j][1]['information_ratio']
                        break
            result[d]['navs'] = detail_nav
            result[d]['risks'] = detail_risk
            detail_nav = {}
            detail_risk = {}
    for _record in fund['manager_records']:
        for d, _value in result.items():
            if int(_record['start_date']) <= int(d) <= int(_record['end_date']):
                if 'manager_id' not in result[d]:
                    result[d]['manager_id'] = list()
                result[d]['manager_id'].append(_record['id'])
    return result


print('saving fund')
_len = len(fund_files)
for i, file in enumerate(fund_files):
    v = get_fund(file)
    bad_fund = False
    for d, _v in v.items():
        if 'manager_id' not in _v:
            bad_fund = True
            break
    if bad_fund:
        continue
    with open(project_path + '/data/funds/' + file, 'w') as wp:
        json.dump(v, wp)
    print('\rsaving fund {}/{} {:.2f}%'.format(i + 1, _len, (i + 1) * 100 / _len), end='')
print()
print('over')
