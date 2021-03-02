import copy
import json
from server import fund_market, fund_data, fund_manager, fund_company, common

ProjectPath = '/home/kuoluo/projects/FundAnalysis/data/explore'
#  fund_market.py
# def get_market_nav_distribution():
#     nav_distribution_by_month = {}
#     res = {}
#     for record in common.fund_data:
#         for nav_data in record['nav']:
#             key = nav_data['datetime'][0:6]
#             fund_id = record['fund_id']
#             if key not in res:
#                 res[key] = {}
#             if fund_id not in res[key]:
#                 res[key][fund_id] = {'nav_values': [], 'nav_avg': 0}
#             tmp = res.get(key).get(fund_id)['nav_values']
#             tmp.append(nav_data['unit_net_value'])
#             res.get(key).get(fund_id)['nav_avg'] = np.mean(tmp)
#     # 二次处理 按月
#     data = {}
#     for k_date, v in res.items():
#         year = k_date[0:4]
#         if year not in data:
#             data[year] = {}
#         data[year][k_date] = []
#         for k_id, value in v.items():
#             data[year][k_date].append(value['nav_avg'])
#     # 处理每一年的数据 聚合到范围中
#     for k, v in data.items():
#         if k not in nav_distribution_by_month:
#             nav_distribution_by_month[k] = {}
#         for month, values in data.get(k).items():
#             if month not in nav_distribution_by_month[k]:
#                 nav_distribution_by_month[k][month] = {}
#                 common.nav_distribution(values, k, month, nav_distribution_by_month)
#     return nav_distribution_by_month
# def get_market_monthly_return_distribution():
#     fund_ids = common.fund_data_dict.keys()
#     unit_net_value = fund_data.get_fund_dict(fund_ids, 'unit_net_value')
#     monthly_return_distribution = {}
#     for fund_id, unit_net_values in unit_net_value.items():
#         fund_nav = {}
#         for date, unit_net_value in unit_net_values.items():
#             year = date[0:4]
#             if year not in fund_nav:
#                 fund_nav[year] = {}
#             month = date[0:6]
#             if month not in fund_nav[year]:
#                 fund_nav[year][month] = 0
#                 first_unit_net_value = unit_net_value
#             fund_nav[year][month] = (unit_net_value / first_unit_net_value - 1) * 100
#         for year, value in fund_nav.items():
#             if year not in monthly_return_distribution:
#                 monthly_return_distribution[year] = {}
#             for month, return_value in value.items():
#                 if month not in monthly_return_distribution[year]:
#                     monthly_return_distribution[year][month] = {'%d~%d' % (-20 + 2 * x, -20 + 2 * (x + 1)): 0 for x in
#                                                                 range(20)}
#                 for interval in monthly_return_distribution[year][month]:
#                     start, end = tuple(interval.split('~'))
#                     if float(start) <= return_value <= float(end):
#                         monthly_return_distribution[year][month][interval] += 1
#                         break
#             monthly_return_distribution[year] = common.sortByKey(monthly_return_distribution[year])
#     monthly_return_distribution = common.sortByKey(monthly_return_distribution)
#     pre_year = None
#     for _year, _value in monthly_return_distribution.items():
#         if int(_year) < 2000:
#             pre_year = _year
#             continue
#         monthly_return_distribution[pre_year][pre_year + '13'] = monthly_return_distribution[_year][_year + '01']
#         pre_year = _year
#     return monthly_return_distribution
#
#
# def get_market_monthly_avg_return():
#     fund_ids = common.fund_data_dict.keys()
#     unit_net_value = fund_data.get_fund_dict(fund_ids, 'unit_net_value')
#     monthly_avg_return = {}
#     for fund_id, unit_net_values in unit_net_value.items():
#         fund_nav = {}
#         for date, unit_net_value in unit_net_values.items():
#             year = date[0:4]
#             if year not in fund_nav:
#                 fund_nav[year] = {}
#             month = date[0:6]
#             if month not in fund_nav[year]:
#                 fund_nav[year][month] = 0
#                 first_unit_net_value = unit_net_value
#             fund_nav[year][month] = (unit_net_value / first_unit_net_value - 1) * 100
#         for year, value in fund_nav.items():
#             if year not in monthly_avg_return:
#                 monthly_avg_return[year] = {}
#             for month, return_value in value.items():
#                 if month not in monthly_avg_return[year]:
#                     monthly_avg_return[year][month] = []
#                 monthly_avg_return[year][month].append(return_value)
#             monthly_avg_return[year] = common.sortByKey(monthly_avg_return[year])
#     monthly_avg_return = common.sortByKey(monthly_avg_return)
#     for _year, _values in monthly_avg_return.items():
#         for _month, _return_values in monthly_avg_return[_year].items():
#             monthly_avg_return[_year][_month] = round(np.mean(_return_values), 2)
#     return monthly_avg_return
# nav_distribution_value = get_market_nav_distribution()
# sector_date_value = get_market_sector_value()
# market_monthly_return_distribution_value = get_market_monthly_return_distribution()
# market_monthly_avg_return_value = get_market_monthly_avg_return()

# common.py
# def nav_distribution(total_list, year, month, nav_distribution_byMonth):
#     countblock = 21
#     intervals = {'%.1f~%.1f' % (0 + 0.2 * x, 0 + 0.2 * (x + 1)): 0 for x in range(countblock)}
#     for ls in total_list:
#         for interval in intervals:
#             start, end = tuple(interval.split('~'))
#             if float(start) <= ls <= float(end):
#                 intervals[interval] += 1
#     for i in intervals:
#         nav_distribution_byMonth[year][month][i] = intervals[i]
# def monthly_return_distribution(value, year, month, result):
#     countblock = 21
#     intervals = {'%.1f~%.1f' % (-90 + 10 * x, -90 + 10 * (x + 1)): 0 for x in range(countblock)}
#     for interval in intervals:
#         start, end = tuple(interval.split('~'))
#         if float(start) <= value <= float(end):
#             intervals[interval] += 1
#             break
#     for i in intervals:
#         result[year][month][i] = intervals[i]
# def sortByKey(v_dict):
#     v_keys = list(v_dict.keys())
#     v_keys.sort()
#     return dict(zip(v_keys, [v_dict[key] for key in v_keys]))

# market 市场
# data1 = fund_market.get_market_sector_value()
# sector_date_value = {}
# for sector,values in data1.items():
#     sector_date_value[sector] = {}
#     for date, num in values.items():
#         year = str(date)[0:4]
#         if year not in sector_date_value[sector]:
#             sector_date_value[sector][year] = 0
#         sector_date_value[sector][year] = round((num/10000),2) # 万为单位
# with open(ProjectPath + '/sector_date_value.json', 'w') as wp:
#     json.dump(sector_date_value, wp)

# market 净值分布
# nav_distribution_value = fund_market.get_market_nav_distribution()
# with open(ProjectPath + '/nav_distribution_value.json', 'w') as wp:
#     json.dump(nav_distribution_value, wp)

# # market 收益率分布
# monthly_return_distribution_value = fund_market.get_market_monthly_return_distribution()
# with open(ProjectPath + '/return_distribution_value.json', 'w') as wp:
#     json.dump(monthly_return_distribution_value, wp)

# market 平均收益率 by month
market_monthly_avg_return_value = fund_market.get_market_monthly_avg_return()
with open(ProjectPath + '/return_avg_value.json', 'w') as wp:
    json.dump(market_monthly_avg_return_value, wp)

# fund_data.py 基金
# 2
# fund_ids = common.fund_data_dict.keys()
# fund_date_sector =fund_data.get_fund_date_sector(['100020'])
# with open(ProjectPath + '/fund_date_sector.json', 'w') as wp:
#     json.dump(fund_date_sector, wp)

# 二次处理成可展示的数据
# fund_date_sector_value = {}
# with open(ProjectPath+'/fund_date_sector.json', 'r') as fp:
#     data = json.load(fp)
#
#
# def create_datetime(list1):
#     list2 = [0 for x in range(0, len(list1))]
#     dic = dict(map(lambda x, y: [x, y], list1, list2))
#     return dic
#
#
# for fund_id in data:
#     if fund_id not in fund_date_sector_value:
#         fund_date_sector_value[fund_id] = {}
#     datetime_value = create_datetime(data[fund_id].keys())
#     for quarter, quarter_value in data[fund_id].items():
#         for sector_type, value in data[fund_id][quarter].items():
#             if sector_type not in fund_date_sector_value[fund_id]:
#                 fund_date_sector_value[fund_id][sector_type] = copy.deepcopy(datetime_value)
#             if sector_type in data[fund_id][quarter]:
#                 value = data[fund_id][quarter][sector_type]
#                 fund_date_sector_value[fund_id].get(sector_type)[quarter] = value
#
# with open(ProjectPath + '/fund_date_sector_value.json', 'w') as wp:
#     json.dump(fund_date_sector_value, wp)

# 3
# min_start_date, max_end_date = fund_data.get_fund_time_border(fund_ids)
# fund_date_income = fund_data.get_fund_date_income(fund_ids, min_start_date, max_end_date)
# with open(ProjectPath + '/fund_date_income.json', 'w') as wp:
#     json.dump(fund_date_income, wp)

# fund_manager 基金经理
# 1 某个基金经理下的所有基金的净值
# manager_name_dict = fund_manager.get_manager_name()
# manager_nav_dict = fund_manager.get_manager_nav(manager_name_dict.keys())
# with open(ProjectPath + '/manager_nav_value.json', 'w') as wp:
#     json.dump(manager_nav_dict, wp)

# 2 某个基金经理下的所有基金的规模
# manager_asset_dict = fund_manager.get_manager_asset(manager_name_dict.keys())
# with open(ProjectPath + '/manager_asset_value.json', 'w') as wp:
#     json.dump(manager_asset_dict, wp)
#
# # 3 某个基金经理下的所有基金的收益
# manager_time_dict, start_date, end_date = fund_manager.get_manager_times(manager_name_dict.keys())
# manager_income_dict = fund_manager.get_manager_income(manager_name_dict.keys(), start_date, end_date)
# with open(ProjectPath + '/manager_income_value.json', 'w') as wp:
#     json.dump(manager_income_dict, wp)

# fund_company 公司
# 1 基金产品数量变化
# all_date = fund_company.get_all_date()
# company_date_fund_value = fund_company.get_company_date_fund(all_date)
# with open(ProjectPath + '/company_date_fund_value.json', 'w') as wp:
#     json.dump(company_date_fund_value, wp)
# 2 基金经理数量变化
# company_date_manager_value = fund_company.get_company_date_manager(all_date)
# with open(ProjectPath + '/company_date_manager_value.json', 'w') as wp:
#     json.dump(company_date_manager_value, wp)
# 3 基金规模变化
# company_date_asset_value = fund_company.get_company_date_asset()
# with open(ProjectPath + '/company_date_asset_value.json', 'w') as wp:
#     json.dump(company_date_asset_value, wp)

print('over')
