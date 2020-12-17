import copy
import json
from server import fund_market, fund_data, fund_manager, fund_company, common


ProjectPath = '/home/kuoluo/projects/FundAnalysis/data/explore'

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

#2 某个基金经理下的所有基金的规模
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