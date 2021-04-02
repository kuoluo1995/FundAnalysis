import json
import os
import sys
from pypinyin import lazy_pinyin
from datetime import datetime
from collections import defaultdict

sys.path.append('/home/kuoluo/projects/FundAnalysis/')
from tools import color_tool

# project_path = 'E:/Projects/PythonProjects/FundAnalysis'
project_path = '/home/kuoluo/projects/FundAnalysis'
fund_files = os.listdir(project_path + '/data/view_funds')
# with open(project_path + '/data/dictionary/weight_key.json', 'r', encoding='UTF-8') as fp:
#     weight_key = json.load(fp)
# weight_keys = {}
# for _key in weight_key:
#     weight_keys[_key] = {'cn_name': '', 'en_name': ''}
# with open(project_path + '/data/dictionary/weight_key.json', 'w', encoding='UTF-8') as wp:
#     json.dump(weight_keys, wp)

def build_dict(files):
    manager_dict = {}
    fund_dict = {}
    sector_dict = defaultdict(int)
    fund_manager = {}
    manager_fund = {}
    _len = len(files)
    for i, file in enumerate(files):
        with open(project_path + '/data/view_funds/' + file, 'r', encoding='UTF-8') as fp:
            view_fund = json.load(fp)
        fund_manager[file[:-5]] = set()
        for _date, _value in view_fund.items():
            if 'manager_ids' not in _value:
                print()
            for m_id, _ in _value['manager_ids'].items():
                if m_id not in manager_dict:
                    manager_dict[m_id] = 0
                    manager_fund[m_id] = set()
                manager_dict[m_id] += 1
                fund_manager[file[:-5]].add(m_id)
                manager_fund[m_id].add(file[:-5])
            for _s, _ in _value['holding'].items():
                sector_dict[_s] += 1
        print('\rbuild dict: {}/{} {:.2f}%'.format(i + 1, _len, (i + 1) * 100 / _len), end='')
    for i, file in enumerate(files):
        with open(project_path + '/data/source/' + file, 'r', encoding='UTF-8') as fp:
            fund = json.load(fp)
        if int(fund['de_listed_date']) == 0:
            fund['de_listed_date'] = '20191231'
        d = (datetime.strptime(fund['de_listed_date'], '%Y%m%d') - datetime.strptime(fund['listed_date'],
                                                                                     '%Y%m%d')).days
        fund_dict[file[:-5]] = {'amc': fund['amc'], 'symbol': fund['symbol'], 'fund_type': fund['fund_type'],
                                'listed_date': fund['listed_date'], 'de_listed_date': fund['de_listed_date'],
                                'days': d, 'exchange': fund['exchange']}
        for _manager in fund['manager_records']:
            if _manager['id'] not in manager_dict:
                continue
            count = manager_dict[_manager['id']]
            if type(count) is int:
                pinyin = lazy_pinyin(_manager['name'])
                pinyin[0] = pinyin[0].capitalize()
                if len(pinyin) > 1:
                    pinyin[1] = pinyin[1].capitalize()
                manager_dict[_manager['id']] = {'cn_name': _manager['name'], 'count': count, 'start_date': 20200000,
                                                'end_date': 0, 'amcs': dict(), 'en_name': ''.join(pinyin)}
            if int(manager_dict[_manager['id']]['start_date']) > int(_manager['start_date']):
                manager_dict[_manager['id']]['start_date'] = _manager['start_date']
            if int(manager_dict[_manager['id']]['end_date']) < int(_manager['end_date']):
                manager_dict[_manager['id']]['end_date'] = _manager['end_date']
            if fund['amc'] not in manager_dict[_manager['id']]['amcs']:
                manager_dict[_manager['id']]['amcs'][fund['amc']] = 0
            if int(manager_dict[_manager['id']]['amcs'][fund['amc']]) < int(_manager['end_date']):
                manager_dict[_manager['id']]['amcs'][fund['amc']] = _manager['end_date']
    for m_id, _values in manager_dict.items():
        d = (datetime.strptime(_values['end_date'], '%Y%m%d') - datetime.strptime(_values['start_date'],
                                                                                  '%Y%m%d')).days
        manager_dict[m_id]['days'] = d
    for f_id, _list in fund_manager.items():
        fund_manager[f_id] = list(_list)
    for m_id, _list in manager_fund.items():
        manager_fund[m_id] = list(_list)
    manager_list = sorted(manager_dict.items(), key=lambda v: v[1]['count'], reverse=True)
    manager_dict = {m_id: {'index': i, **_} for i, (m_id, _) in enumerate(manager_list)}
    sector_list = sorted(sector_dict.items(), key=lambda v: v[1], reverse=True)
    sector_colors = color_tool.get_hex_colors_by_num(len(sector_list))
    sector_dict = {m_id: {'color': sector_colors[i], 'en_name': ''} for i, (m_id, _) in enumerate(sector_list)}
    return fund_dict, manager_dict, sector_dict, fund_manager, manager_fund


print('start save dict')
fund_dict, manager_dict, sector_dict, fund_manager, manager_fund = build_dict(fund_files)
with open(project_path + '/data/dictionary/fund_dict.json', 'w') as wp:
    json.dump(fund_dict, wp)
with open(project_path + '/data/dictionary/manager_dict.json', 'w') as wp:
    json.dump(manager_dict, wp)
with open(project_path + '/data/dictionary/sector_dict.json', 'w') as wp:
    json.dump(sector_dict, wp)
with open(project_path + '/data/dictionary/fund_manager_dict.json', 'w') as wp:
    json.dump(fund_manager, wp)
with open(project_path + '/data/dictionary/manager_fund_dict.json', 'w') as wp:
    json.dump(manager_fund, wp)
print()
print('over')
