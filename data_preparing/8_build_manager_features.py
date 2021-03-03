import json
import os
import numpy as np

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'
manager_files = os.listdir(project_path + '/data/managers')

with open(project_path + '/data/dictionary/manager_dict.json', 'r', encoding='UTF-8') as rp:
    manager_dict = json.load(rp)

manager_feature = {}
for file in manager_files:
    with open(project_path + '/data/managers/' + file, 'r', encoding='UTF-8') as fp:
        manager = json.load(fp)
    funds = list(manager.items())[-1][1]
    attributes = {'stock': list(), 'bond': list(), 'cash': list(), 'other': list(), 'size': list(), 'alpha': list(),
                  'beta': list(), 'sharp_ratio': list(), 'max_drop_down': list(), 'information_ratio': list(),
                  'risk': list(), 'instl_weight': list(), 'unit_nav': list(), 'nav_return': list(), 'car': list()}
    for f_id, _value in funds.items():
        attributes['stock'].append(_value['stock'])
        attributes['bond'].append(_value['bond'])
        attributes['cash'].append(_value['cash'])
        attributes['other'].append(_value['other'])
        attributes['size'].append(_value['size'])
        attributes['alpha'].append(_value['alpha'])
        attributes['beta'].append(_value['beta'])
        attributes['sharp_ratio'].append(_value['sharp_ratio'])
        attributes['max_drop_down'].append(_value['max_drop_down'])
        attributes['information_ratio'].append(_value['information_ratio'])
        attributes['risk'].append(_value['risk'])
        attributes['instl_weight'].append(_value['instl_weight'])
        attributes['unit_nav'].append(_value['unit_nav'])
        attributes['nav_return'].append(_value['nav_return'])
        attributes['car'].append(_value['car'])
    for _name, _list in attributes.items():
        if len(_list) == 1:
            attributes[_name] = _list[0]
        else:
            attributes[_name] = np.mean(_list)
    attributes['days'] = manager_dict[file[:-5]]['days']
    attributes['num_fund'] = len(funds)
    attributes['amcs'] = sorted(manager_dict[file[:-5]]['amcs'].items(), key=lambda d: int(d[1]))
    attributes['amcs'] = {_d: _v for _v, _d in attributes['amcs']}
    manager_feature[file[:-5]] = attributes
with open(project_path + '/data/dictionary/manager_features.json', 'w', encoding='UTF-8') as wp:
    json.dump(manager_feature, wp)
print('over')
