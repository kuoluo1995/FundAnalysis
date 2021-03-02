import json
import os

from collections import defaultdict

# project_path = 'E:/Projects/PythonProjects/FundAnalysis'
project_path = '/home/kuoluo/projects/FundAnalysis'
fund_files = os.listdir(project_path + '/data/view_funds')


def build_dict(files):
    manager_dict = {}
    sector_dict = defaultdict(int)
    key_dict = None
    fund_manager = {}
    manager_fund = {}
    _len = len(files)
    for i, file in enumerate(files):
        with open(project_path + '/data/view_funds/' + file, 'r', encoding='UTF-8') as fp:
            fund = json.load(fp)
        fund_manager[file[:-5]] = set()
        for _date, _value in fund.items():
            for m_id, _ in _value['manager_ids'].items():
                if m_id not in manager_dict:
                    manager_dict[m_id] = 0
                    manager_fund[m_id] = set()
                manager_dict[m_id] += 1
                fund_manager[file[:-5]].add(m_id)
                manager_fund[m_id].add(file[:-5])
            for _s, _ in _value['holding'].items():
                sector_dict[_s] += 1
            if key_dict is None and len(_value) == 22:
                key_dict = _value.keys()
        print('\rbuild dict: {}/{} {:.2f}%'.format(i + 1, _len, (i + 1) * 100 / _len), end='')
    for i, file in enumerate(files):
        with open(project_path + '/data/source/' + file, 'r', encoding='UTF-8') as fp:
            fund = json.load(fp)
        for _manager in fund['manager_records']:
            if _manager['id'] not in manager_dict:
                continue
            count = manager_dict[_manager['id']]
            if type(count) is not int:
                continue
            manager_dict[_manager['id']] = {'name': _manager['name'], 'count': count}
    for f_id, _list in fund_manager.items():
        fund_manager[f_id] = list(_list)
    for m_id, _list in manager_fund.items():
        manager_fund[m_id] = list(_list)
    return manager_dict, sector_dict, list(key_dict), fund_manager, manager_fund


print('start save dict')
manager_dict, sector_dict, key_dict, fund_manager, manager_fund = build_dict(fund_files)
manager_list = sorted(manager_dict.items(), key=lambda v: v[1]['count'], reverse=True)
manager_dict = {m_id: i for i, (m_id, _) in enumerate(manager_list)}
sector_list = sorted(sector_dict.items(), key=lambda v: v[1], reverse=True)
sector_dict = {m_id: i for i, (m_id, _) in enumerate(sector_list)}
with open(project_path + '/data/dictionary/manager_dict.json', 'w') as wp:
    json.dump(manager_dict, wp)
with open(project_path + '/data/dictionary/sector_dict.json', 'w') as wp:
    json.dump(sector_dict, wp)
with open(project_path + '/data/dictionary/weight_key_dict.json', 'w') as wp:
    json.dump(key_dict, wp)
with open(project_path + '/data/dictionary/fund_manager_dict.json', 'w') as wp:
    json.dump(fund_manager, wp)
with open(project_path + '/data/dictionary/manager_fund_dict.json', 'w') as wp:
    json.dump(manager_fund, wp)
print('over')
