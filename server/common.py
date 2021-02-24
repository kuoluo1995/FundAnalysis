import os
import json

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'

fund_ids = [file[:-5] for file in os.listdir(project_path + '/data/source')]
manager_ids = [file[:-5] for file in os.listdir(project_path + '/data/managers')]

with open(project_path + '/data/stock_concept_sector.json', 'r', encoding='UTF-8') as rp:
    stock_sector = json.load(rp)

with open(project_path + '/data/manager_dict.json', 'r', encoding='UTF-8') as rp:
    manager_dict = json.load(rp)


def get_source_fund_json(fund_id):
    with open(project_path + '/data/source/' + fund_id + '.json', 'r', encoding='UTF-8') as fp:
        fund_data = json.load(fp)
    return fund_data


def get_manager_json(manager_id):
    with open(project_path + '/data/managers/' + manager_id + '.json', 'r', encoding='UTF-8') as fp:
        manager_data = json.load(fp)
    return manager_data


def get_view_fund_json(fund_id):
    with open(project_path + '/data/funds/' + fund_id + '.json', 'r', encoding='UTF-8') as fp:
        fund_data = json.load(fp)
    return fund_data


from enum import Enum


class Interval(Enum):
    Daily = 'daily'
    Week = 'week'
    Month = 'month'
    Year = 'year'
    Total = 'total'

    @staticmethod
    def format_date(_type, date):
        if _type == Interval.Daily:
            return date
        elif _type == Interval.Month:
            return date[:6]
        elif _type == Interval.Year:
            return date[:4]
        elif _type == Interval.Total:
            return 'total'
        else:
            print('interval enum:error')


if __name__ == '__main__':
    print('init')
