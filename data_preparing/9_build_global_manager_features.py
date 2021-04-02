import json
from tools import normail_tool

project_path = '/home/kuoluo/projects/FundAnalysis'
manager_dict = {}
with open(project_path + '/data/dictionary/manager_features.json', 'r', encoding='UTF-8') as rp:
    features = json.load(rp)
for m_id, feature in features.items():
    manager_dict[m_id] = feature
    feature.pop('amcs')
min_max_dict = normail_tool.get_max_min_feature(manager_dict,
                                                {'stock', 'bond', 'cash', 'other', 'size', 'alpha', 'beta',
                                                 'sharp_ratio', 'max_drop_down', 'information_ratio', 'risk',
                                                 'instl_weight', 'one_quarter_return', 'one_year_return',
                                                 'three_year_return', 'one_quarter_car', 'one_year_car',
                                                 'three_year_car', 'days', 'num_fund'})
manager_dict = normail_tool.get_normail_feature(manager_dict, min_max_dict)
with open(project_path + '/data/dictionary/global_manager_features.json', 'w', encoding='UTF-8') as wp:
    json.dump(manager_dict, wp)
print('over')
