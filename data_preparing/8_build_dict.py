import json
import os

# ProjectPath = '/home/kuoluo/projects/FundAnalysis'
from collections import defaultdict

# project_path = 'E:/Projects/PythonProjects/FundAnalysis'
# fund_files = os.listdir(project_path + '/data/source')
# with open(project_path + '/data/stock_concept_sector.json', 'r', encoding='UTF-8') as rp:
#     stock_sector = json.load(rp)
#
#
# def build_dict(files):
#     manager_dict = defaultdict(int)
#     sector_dict = defaultdict(int)
#     _len = len(files)
#     for i, file in enumerate(files):
#         with open(project_path + '/data/source/' + file, 'r', encoding='UTF-8') as fp:
#             fund = json.load(fp)
#         for records in fund['manager_records']:
#             m_id = records['id']
#             manager_dict[m_id] += 1
#         for _record in fund['holding_records']:
#             for holding in _record['holdings_list']:
#                 if holding['order_book_id'][:6] not in stock_sector:
#                     _sector = '未知'
#                 else:
#                     _sector = stock_sector[holding['order_book_id'][:6]]
#                 sector_dict[_sector] += 1
#         print('\rbuild dict: {}/{} {:.2f}%'.format(i + 1, _len, (i + 1) * 100 / _len), end='')
#     return manager_dict, sector_dict
#
#
# print('start save dict')
# manager_dict, sector_dict = build_dict(fund_files)
# manager_list = sorted(manager_dict.items(), key=lambda v: v[1], reverse=True)
# manager_dict = {m_id: i for i, (m_id, _) in enumerate(manager_list)}
# sector_list = sorted(sector_dict.items(), key=lambda v: v[1], reverse=True)
# sector_dict = {m_id: i for i, (m_id, _) in enumerate(sector_list)}
# with open(project_path + '/data/mananger_dict.json', 'w') as wp:
#     json.dump(manager_dict, wp)
# with open(project_path + '/data/sector_dict.json', 'w') as wp:
#     json.dump(sector_dict, wp)
# print('over')
ProjectPath = '/home/kuoluo/projects/FundAnalysis'
# ProjectPath = 'E:/Projects/PythonProjects/FundAnalysis'
source_files = os.listdir(ProjectPath + '/data/source')
fund_files = os.listdir(ProjectPath + '/data/funds')
files = set(source_files) - set(fund_files)
for file in files:
    os.remove(ProjectPath + '/data/source/' + file)
