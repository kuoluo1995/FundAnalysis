import json
import os
import numpy as np

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'
manager_files = os.listdir(project_path + '/data/managers')

with open(project_path + '/data/dictionary/manager_dict.json', 'r', encoding='UTF-8') as rp:
    manager_dict = json.load(rp)

manager_feature = {}
_len = len(manager_files)
for i, file in enumerate(manager_files):
    with open(project_path + '/data/managers/' + file, 'r', encoding='UTF-8') as fp:
        manager = json.load(fp)
    for _da, funds in manager.items():
        if _da not in manager_feature:
            manager_feature[_da] = {}
        if file[:-5] not in manager_feature[_da]:
            manager_feature[_da][file[:-5]] = {}
        for f_id, _values in funds.items():
            for _name, _value in _values.items():
                if _name in ['detail_unit_navs', 'detail_hs300s', 'manager_ids', 'hs300']:
                    continue
                if _name not in manager_feature[_da][file[:-5]]:
                    manager_feature[_da][file[:-5]][_name] = list()
                manager_feature[_da][file[:-5]][_name].append(_value)
    for _da, manager in manager_feature.items():
        for m_id, _values in manager.items():
            for _name, _v in _values.items():
                manager_feature[_da][m_id][_name] = np.mean(_v)
    print('\rsaving manager {}/{} {:.2f}%'.format(i + 1, _len, (i + 1) * 100 / _len), end='')
with open(project_path + '/data/dictionary/manager_features.json', 'w', encoding='UTF-8') as wp:
    json.dump(manager_feature, wp)
print('over')
