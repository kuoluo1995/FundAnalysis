import json
import pandas as pd
from pandas import Series
import numpy as np
import math

# 按季度：遍历每个基金，取当前基金的各个资产的比例，并求平均比例。
ProjectPath = '/home/kuoluo/projects/FundAnalysis'
# with open(ProjectPath+'/data/good_funds.json', 'r') as fp:
#     fund_data = json.load(fp)
#
# asset_distribution_byQuarter = {}  # 最后存的json数据
#
#
# def distribution(param, year_param, quarter_param, asset_type):
#     intervals = {'%.1f~%.1f' % (0 + 0.2 * x, 0 + 0.2 * (x + 1)): 0 for x in range(5)}
#
#     for interval in intervals:
#         start, end = tuple(interval.split('~'))
#         if float(start) <= param <= float(end):
#             asset_distribution_byQuarter[year_param][quarter_param][asset_type][interval] += 1
#             break
#
#
# res = {}
# for record in fund_data:
#     fund_id = record['fund_id']
#     for asset_allocation_record in record['asset_allocation_records']:  # list
#         year = asset_allocation_record['datetime'][0:4]
#         month = asset_allocation_record['datetime'][4:6]
#         if fund_id not in res:
#             res[fund_id] = {}
#         if year not in res[fund_id]:
#             res[fund_id][year] = {'01~03': {'stock': {'values': [], 'avg': 0}, 'bond': {'values': [], 'avg': 0}, 'cash': {'values': [], 'avg': 0}}, '04~06':  {'stock': {'values': [], 'avg': 0}, 'bond': {'values': [], 'avg': 0}, 'cash': {'values': [], 'avg': 0}}, '07~09':  {'stock': {'values': [], 'avg': 0}, 'bond': {'values': [], 'avg': 0}, 'cash': {'values': [], 'avg': 0}}, '10~12':  {'stock': {'values': [], 'avg': 0}, 'bond': {'values': [], 'avg': 0}, 'cash': {'values': [], 'avg': 0}}}  # 年
#         # 判断当月属于哪个季度
#         for quarter in res[fund_id][year].keys():
#             start,end = tuple(quarter.split('~'))
#             if int(start) <= int(month) <= int(end):
#                 res.get(fund_id).get(year).get(quarter).get('stock').get('values').append(asset_allocation_record['stock'])
#                 res.get(fund_id).get(year).get(quarter).get('stock')['avg'] = np.mean(res.get(fund_id).get(year).get(quarter).get('stock').get('values'))
#                 res.get(fund_id).get(year).get(quarter).get('bond').get('values').append(asset_allocation_record['bond'])
#                 res.get(fund_id).get(year).get(quarter).get('bond')['avg'] = np.mean(res.get(fund_id).get(year).get(quarter).get('bond').get('values'))
#                 res.get(fund_id).get(year).get(quarter).get('cash').get('values').append(asset_allocation_record['cash'])
#                 res.get(fund_id).get(year).get(quarter).get('cash')['avg'] = np.mean(res.get(fund_id).get(year).get(quarter).get('cash').get('values'))
#                 break
#
# for fund in res:
#     for year,year_value in res[fund].items():
#         if year not in asset_distribution_byQuarter:
#             asset_distribution_byQuarter[year] = {}
#         for quarter,quarter_value in res[fund][year].items():
#             if quarter not in asset_distribution_byQuarter[year]:
#                 asset_distribution_byQuarter[year][quarter] = {
#                     'stock': {'%.1f~%.1f' % (0 + 0.2 * x, 0 + 0.2 * (x + 1)): 0 for x in range(5)},
#                     'bond': {'%.1f~%.1f' % (0 + 0.2 * x, 0 + 0.2 * (x + 1)): 0 for x in range(5)},
#                     'cash': {'%.1f~%.1f' % (0 + 0.2 * x, 0 + 0.2 * (x + 1)): 0 for x in range(5)}}
#             distribution(res[fund][year][quarter]['stock']['avg'], year, quarter, 'stock')
#             distribution(res[fund][year][quarter]['bond']['avg'], year, quarter, 'bond')
#             distribution(res[fund][year][quarter]['cash']['avg'], year, quarter, 'cash')
#
# with open(ProjectPath + '/data/explore/asset_distribution_byQuarter.json', 'w') as wp:
#     json.dump(asset_distribution_byQuarter, wp)


# 二次处理成可展示的数据
asset_distribution_byQuarter_value = {}
with open(ProjectPath+'/data/explore/asset_distribution_byQuarter.json', 'r') as fp:
    data = json.load(fp)

for year in data:
    if year not in asset_distribution_byQuarter_value:
        asset_distribution_byQuarter_value[year] = {'stock':{'%.1f~%.1f' % (0 + 0.2 * x, 0 + 0.2 * (x + 1)): [] for x in range(5)},
                                                    'bond':{'%.1f~%.1f' % (0 + 0.2 * x, 0 + 0.2 * (x + 1)): [] for x in range(5)},
                                                    'cash':{'%.1f~%.1f' % (0 + 0.2 * x, 0 + 0.2 * (x + 1)): [] for x in range(5)}}
    for quarter, quarter_value in data[year].items():
        for type, distribution_value in quarter_value.items():
            for distributionArea, value in distribution_value.items():
                asset_distribution_byQuarter_value[year][type][distributionArea].append(data[year][quarter][type][distributionArea])
with open(ProjectPath + '/data/explore/asset_distribution_byQuarter_value.json', 'w') as wp:
    json.dump(asset_distribution_byQuarter_value, wp)

print('over')




