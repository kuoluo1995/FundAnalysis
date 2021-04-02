import os
import json
from tools import color_tool

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'

fund_ids = [file[:-5] for file in os.listdir(project_path + '/data/view_funds')]
manager_ids = [file[:-5] for file in os.listdir(project_path + '/data/managers')]

# green2red_dict = color_tool.get_green2red_dict_by_num(100)
yellow2green = color_tool.get_green_dict_by_num(50)
yellow2red = color_tool.get_red_dict_by_num(50)

with open(project_path + '/data/dictionary/manager_dict.json', 'r', encoding='UTF-8') as rp:
    manager_dict = json.load(rp)

with open(project_path + '/data/dictionary/sector_dict.json', 'r', encoding='UTF-8') as rp:
    sector_dict = json.load(rp)

with open(project_path + '/data/dictionary/fund_loc.json', 'r', encoding='UTF-8') as rp:
    fund_loc_dict = json.load(rp)

with open(project_path + '/data/dictionary/manager2fund.json', 'r', encoding='UTF-8') as rp:
    manager_fund_dict = json.load(rp)

with open(project_path + '/data/dictionary/manager_features.json', 'r', encoding='UTF-8') as rp:
    manager_features = json.load(rp)


def get_source_fund_json(fund_id):
    with open(project_path + '/data/source/' + fund_id + '.json', 'r', encoding='UTF-8') as fp:
        fund_data = json.load(fp)
    return fund_data


def get_manager_json(manager_id):
    with open(project_path + '/data/managers/' + manager_id + '.json', 'r', encoding='UTF-8') as fp:
        manager_data = json.load(fp)
    return manager_data


def get_view_fund_json(fund_id):
    with open(project_path + '/data/view_funds/' + fund_id + '.json', 'r', encoding='UTF-8') as fp:
        fund_data = json.load(fp)
    return fund_data


def get_feature_fund_json(fund_id):
    with open(project_path + '/data/fund_features/' + fund_id + '.json', 'r', encoding='UTF-8') as fp:
        fund_data = json.load(fp)
    return fund_data


if __name__ == '__main__':
    j = get_view_fund_json('510020')
    print('init')
