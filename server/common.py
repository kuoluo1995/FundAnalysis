import os
import json

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'

fund_ids = [file[:-5] for file in os.listdir(project_path + '/data/view_funds')]
manager_ids = [file[:-5] for file in os.listdir(project_path + '/data/managers')]

with open(project_path + '/data/dictionary/manager_dict.json', 'r', encoding='UTF-8') as rp:
    manager_dict = json.load(rp)

with open(project_path + '/data/dictionary/sector_dict.json', 'r', encoding='UTF-8') as rp:
    sector_dict = json.load(rp)

with open(project_path + '/data/dictionary/fund_manager_dict.json', 'r', encoding='UTF-8') as rp:
    fund_manager_dict = json.load(rp)

with open(project_path + '/data/dictionary/manager_fund_dict.json', 'r', encoding='UTF-8') as rp:
    manager_fund_dict = json.load(rp)

with open(project_path + '/data/dictionary/manager_features.json', 'r', encoding='UTF-8') as rp:
    manager_features = json.load(rp)

with open(project_path + '/data/dictionary/global_fund_features.json', 'r', encoding='UTF-8') as rp:
    global_fund_features = json.load(rp)

with open(project_path + '/data/dictionary/global_manager_features.json', 'r', encoding='UTF-8') as rp:
    global_manager_features = json.load(rp)


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
    print('init')
