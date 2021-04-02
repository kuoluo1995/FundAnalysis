import json

project_path = '/home/kuoluo/projects/FundAnalysis'

with open(project_path + '/data/dictionary/manager_dict.json', 'r', encoding='UTF-8') as rp:
    manager_dict = json.load(rp)

manager_index = {}
index_manager = {}
for m_id, value in manager_dict.items():
    manager_index[m_id] = value['index']
    index_manager[value['index']] = m_id
with open(project_path + '/data/manager_index.json', 'w') as wp:
    json.dump(manager_index, wp)
with open(project_path + '/data/index_manager.json', 'w') as wp:
    json.dump(index_manager, wp)
print()
