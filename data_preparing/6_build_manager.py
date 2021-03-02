import json
import os
import numpy as np

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'
fund_files = os.listdir(project_path + '/data/view_funds')


def check_time(_attr, start_date, end_date, str_date):
    _list = list()
    for _v in _attr:
        if int(_v[str_date]) < int(start_date):  # 之前的日期不算
            continue
        if int(end_date) < int(_v[str_date]):
            continue
        _list.append(_v)
    return _list


def build_fund_manager_dict(files):
    manager_dict = {}
    _len = len(files)
    for i, file in enumerate(files):
        with open(project_path + '/data/fund_features/' + file, 'r', encoding='UTF-8') as fp:
            fund = json.load(fp)
        for _date, _value in fund.items():
            for m_id, _title in _value['manager_ids'].items():
                if m_id not in manager_dict:
                    manager_dict[m_id] = {}
                if _date not in manager_dict[m_id]:
                    manager_dict[m_id][_date] = {}
                manager_dict[m_id][_date][file[:-5]] = _value
        print('\rbuild manager: {}/{} {:.2f}%'.format(i + 1, _len, (i + 1) * 100 / _len), end='')
    return manager_dict


print('start save manager')
fund_manager = build_fund_manager_dict(fund_files)
i = 1
_len = len(fund_manager)
for m_id, funds in fund_manager.items():
    with open(project_path + '/data/managers/' + m_id + '.json', 'w') as wp:
        json.dump(funds, wp)
    print('\rsaving manager:{}/{} {:.2f}%'.format(i, _len, i * 100 / _len), end='', flush=True)
    i += 1
print()
print('over')
