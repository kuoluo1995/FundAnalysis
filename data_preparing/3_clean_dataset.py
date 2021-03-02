import json
import os

import numpy as np

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'
data_path = '/home/kuoluo/data/fund'
# data_path = 'E:/Dataset/fund/'
fund_files = os.listdir(data_path + '/perpared_fund')
with open(project_path + '/data/stock_concept_sector.json', 'r', encoding='UTF-8') as rp:
    stock_sector = json.load(rp)

_len = len(fund_files)
# 检查一级列表的数据
for i, _file in enumerate(fund_files):
    with open(data_path + '/perpared_fund/' + _file, 'r', encoding='UTF-8') as fp:
        fund = json.load(fp)
    bad_fund = False
    f_id = fund['fund_id']
    temp_list = list()
    for _record in fund['manager_records']:
        if _record['name'] is None or (_record['name']).strip() == '':
            bad_fund = True
        if int(_record['end_date']) - int(_record['start_date']) <= 0:
            continue
        _record.pop('return')
        # if _record['title'] != '基金经理':
        #     continue
        temp_list.append(_record)
    if len(temp_list) == 0 or bad_fund:
        continue
    fund['manager_records'] = temp_list
    temp_list = list()
    for _record in fund['nav']:
        temp_list.append(_record)
    if len(temp_list) == 0:
        continue
    fund['nav'] = temp_list
    for _record in fund['holder_structure']:
        if _record['instl_weight'] is None or _record['retail_weight'] is None:
            bad_fund = True
    if len(fund['holder_structure']) == 0 or bad_fund:
        continue
    for _record in fund['holding_records']:
        for _v in _record['holdings_list']:
            # if np.isnan(_v['weight']):
            #     bad_fund = True
            # if np.isnan(_v['shares']):
            #     bad_fund = True
            if np.isnan(_v['market_value']):
                bad_fund = True
            if _v['order_book_id'][:6] not in stock_sector:
                _sector = '未知'
            else:
                _sector = stock_sector[_v['order_book_id'][:6]]
            _v['sector'] = _sector
    if len(fund['holding_records']) == 0 or bad_fund:
        continue
    if not bad_fund:
        with open(project_path + '/data/source/' + fund['fund_id'] + '.json', 'w', encoding='UTF-8') as wp:
            json.dump(fund, wp)
        print('\rsaving source fund: {}/{} {:.2f}%'.format(i + 1, _len, (i + 1) * 100 / _len), end='')
print()
print('over')
