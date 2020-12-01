import json
import pandas as pd
from pandas import Series
import numpy as np
import math

# 按月：遍历每个基金，取当前基金的nav中的净值，并求平均值。看当月的净值分布情况。

ProjectPath = '/home/kuoluo/projects/FundAnalysis'
with open(ProjectPath+'/data/good_funds.json', 'r') as fp:
    fund_data = json.load(fp)

nav_distribution_byMonth = {} # 最后存的json数据


def distribution(total_list, year, month):
    countblock = 21
    intervals = {'%.1f~%.1f' % (0 + 0.2 * x, 0 + 0.2 * (x + 1)): 0 for x in range(countblock)}
    for ls in total_list:
        for interval in intervals:
            start, end = tuple(interval.split('~'))
            if float(start) <= ls <= float(end):
                intervals[interval] += 1
    for i in intervals:
        nav_distribution_byMonth[year][month][i] = intervals[i]


res = {}
for record in fund_data:
    for nav_data in record['nav']:
        key = nav_data['datetime'][0:6]
        fund_id = record['fund_id']
        if key not in res:
            res[key] = {}
        if fund_id not in res[key]:
            res[key][fund_id] = {'nav_values': [], 'nav_avg': 0}
        tmp = res.get(key).get(fund_id)['nav_values']
        tmp.append(nav_data['unit_net_value'])
        res.get(key).get(fund_id)['nav_avg'] = np.mean(tmp)

# 二次处理 按月
data = {}
for k_date, v in res.items():
    year = k_date[0:4]
    if year not in data:
        data[year] = {}
    data[year][k_date] = []
    for k_id, value in v.items():
        data[year][k_date].append(value['nav_avg'])

for k,v in data.items(): #处理每一年的数据
    if k not in nav_distribution_byMonth:
        nav_distribution_byMonth[k] = {}
    for month,values in data.get(k).items():
        if month not in nav_distribution_byMonth[k]:
            nav_distribution_byMonth[k][month] = {}
            distribution(values, k, month)

with open(ProjectPath + '/data/nav_distribution_byMonth.json', 'w') as wp:
    json.dump(nav_distribution_byMonth, wp)

print('over')


# 按年整理 最后每年生成一张图
# draw_data = {}
# for k_month, v_navs in data.items():
#     year = k_month[0:4]
#     if year not in draw_data:
#         draw_data[year] = {}
#     draw_data[year][k_month] = {'0~0.6': 0, '0.6~1.2': 0, '1.2~1.8': 0, '1.8~2.4': 0, '2.4~3.0': 0, '3.0~3.6': 0, '3.6~4.2': 0}
#     for x in v_navs:
#         if 0<x<=0.6:
#             draw_data.get(year).get(k_month)['0~0.6'] += 1
#         elif 0.6<x<=1.2:
#             draw_data.get(year).get(k_month)['0.6~1.2'] += 1
#         elif 1.2<x<=1.8:
#             draw_data.get(year).get(k_month)['1.2~1.8'] += 1
#         elif 1.8<x<=2.4:
#             draw_data.get(year).get(k_month)['1.8~2.4'] += 1
#         elif 2.4<x<=3.0:
#             draw_data.get(year).get(k_month)['2.4~3.0'] += 1
#         elif 3.0<x<=3.6:
#             draw_data.get(year).get(k_month)['3.0~3.6'] += 1
#         elif 3.6<x<=4.2:
#             draw_data.get(year).get(k_month)['3.6~4.2'] += 1

# for year,month_v in draw_data.items():
#     print(year)
#     for month,nav_v in month_v.items():
#         print(month)
#         print(nav_v.values())
#
#
# print(draw_data)



