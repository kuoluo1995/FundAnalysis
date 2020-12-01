import json
import re
import threading
from collections import Counter

from utils.show_tool import pie_chart, bar_chart

with open('/home/kuoluo/data/fund/fund_data.json', 'r') as fp:
    fund_data = json.load(fp)

# 检查一级列表的数据
# base_args = {}
# for fund in fund_data:
#     for key, value in fund.items():
#         if isinstance(value, dict) or isinstance(value, list):
#             continue
#         if key not in base_args:
#             base_args[key] = []
#         base_args[key].append(value)

# pie_chart(base_args['transition_time'], {0: '每天', 1: '单周', 2: '双周'}, 'transition_time')
# listed_date = [int(_) for _ in base_args['listed_date']]
# bar_chart(listed_date, 'listed_date', need_zero=True, num_gap=100)
# de_listed_date = [int(_) for _ in base_args['de_listed_date']]
# bar_chart(de_listed_date, 'de_listed_date', need_zero=True, num_gap=100)
# all_names = []
# for str_names in base_args['fund_manager']:
#     if str_names is None:
#         all_names.append(str_names)
#         continue
#     str_names = str_names.strip()
#     if bool(re.search('[a-z]', str_names)):
#
#         names = [_.strip() for _ in str_names.split(',')]
#     else:
#         names = re.split('[,| ]', str_names)
#     all_names += names
# bar_chart(all_names, 'manager_name', has_none=True, value_sort=True)
# bar_chart(base_args['latest_size'], 'latest_size', need_zero=True, num_gap=100)
# pie_chart(base_args['fund_type'], {'StockIndex': '股票指数', 'Hybrid': '混合型', 'Stock': '股票型'}, 'fund_type')
# bar_chart(base_args['amc'], 'amc', value_sort=True)
# pie_chart(base_args['exchange'], {'': '', 'XSHE': '深圳', 'XSHG': '上海'}, 'exchange')

# 检查二级列表的数据
records_args = {'manager_records': {}, 'nav': {}, 'industry_allocation': {}, 'holder_structure': {},
                'instrument_category': {}, 'asset_allocation_records': {}, 'indicators_records': {}}
for fund in fund_data:
    for _records in fund['manager_records']:
        for key, value in _records.items():
            if key not in records_args['manager_records']:
                records_args['manager_records'][key] = []
            records_args['manager_records'][key].append(value)
    for _records in fund['nav']:
        for key, value in _records.items():
            if key not in records_args['nav']:
                records_args['nav'][key] = []
            records_args['nav'][key].append(value)
    for _records in fund['industry_allocation_records']:
        for key, value in _records.items():
            if key not in records_args['industry_allocation_records']:
                records_args['industry_allocation_records'][key] = []
            records_args['industry_allocation_records'][key].append(value)
    for _records in fund['holder_structure']:
        for key, value in _records.items():
            if key not in records_args['holder_structure']:
                records_args['holder_structure'][key] = []
            records_args['holder_structure'][key].append(value)
    for _records in fund['instrument_category']:
        for key, value in _records.items():
            if key not in records_args['instrument_category']:
                records_args['instrument_category'][key] = []
            records_args['instrument_category'][key].append(value)
    # for _asset_allocation_records in fund['asset_allocation_records']:
    #     for key, value in _asset_allocation_records.items():
    #         if key not in records_args['asset_allocation_records']:
    #             records_args['asset_allocation_records'][key] = []
    #         records_args['asset_allocation_records'][key].append(value)
    # for _indicators_records_records in fund['indicators_records']:
    #     for key, value in _indicators_records_records.items():
    #         if key not in records_args['indicators_records']:
    #             records_args['indicators_records'][key] = []
    #         records_args['indicators_records'][key].append(value)
# bar_chart(records_args['manager_records']['days'], 'days', need_zero=True, num_gap=100)
# start_date = [int(_) for _ in records_args['manager_records']['start_date']]
# bar_chart(start_date, 'start_date', need_zero=True, num_gap=100)
# end_date = [int(_) for _ in records_args['manager_records']['end_date']]
# bar_chart(end_date, 'end_date', has_nat=True, need_zero=True, num_gap=100)
# bar_chart(records_args['manager_records']['return'], 'return', has_nan=True, num_gap=300)
pie_chart(records_args['manager_records']['title'],
          {'Warrant': '权证', 'DebtSecu': '债权', 'AShare': 'A股', 'HShare': '港股'}, 'category')
asset_datetime = [int(_) for _ in records_args['asset_allocation_records']['datetime']]
bar_chart(asset_datetime, 'asset_datetime', need_zero=True, num_gap=100)
bar_chart(records_args['asset_allocation_records']['stock'], 'stock', gap=0.1, is_long=False)
bar_chart(records_args['asset_allocation_records']['bond'], 'bond', gap=0.1, is_long=False)
bar_chart(records_args['asset_allocation_records']['cash'], 'cash', gap=0.1, is_long=True)
bar_chart(records_args['asset_allocation_records']['other'], 'other', gap=0.1, is_long=False)
bar_chart(records_args['asset_allocation_records']['net_asset'], 'net_asset', need_zero=False, num_gap=100)
bar_chart(records_args['asset_allocation_records']['total_asset'], 'total_asset', need_zero=False, num_gap=100)

indicator_datetime = [int(_) for _ in records_args['indicators_records']['datetime']]
bar_chart(indicator_datetime, 'indicator_datetime', need_zero=True, num_gap=100)
bar_chart(records_args['indicators_records']['average_size'], 'average_size', has_nan=True, num_gap=100)
bar_chart(records_args['indicators_records']['annualized_returns'], 'annualized_returns', num_gap=100)
bar_chart(records_args['indicators_records']['annualized_risk'], 'annualized_risk', num_gap=122, gap=1)
bar_chart(records_args['indicators_records']['last_three_month_return'], 'last_three_month_return', num_gap=55, gap=1)
bar_chart(records_args['indicators_records']['total_return'], 'total_return', num_gap=55, gap=1)
bar_chart(records_args['indicators_records']['to_date_return'], 'to_date_return', num_gap=55, gap=1)
bar_chart(records_args['indicators_records']['total_alpha'], 'total_alpha', num_gap=100)
bar_chart(records_args['indicators_records']['total_beta'], 'total_beta', num_gap=100)
bar_chart(records_args['indicators_records']['sharp_ratio'], 'sharp_ratio', num_gap=43, gap=1)
bar_chart(records_args['indicators_records']['max_drop_down'], 'max_drop_down', gap=0.1, is_long=False)
bar_chart(records_args['indicators_records']['information_ratio'], 'information_ratio', num_gap=100)

# 检查三级列表的数据
holding_records_args = {'datetime': [], 'holding_list': {}}
for fund in fund_data:
    for _holding_records in fund['holding_records']:
        holding_records_args['datetime'].append(_holding_records['datetime'])
        for _holding in _holding_records['holdings_list']:
            for key, value in _holding.items():
                if key not in holding_records_args['holding_list']:
                    holding_records_args['holding_list'][key] = []
                holding_records_args['holding_list'][key].append(value)

holding_datetime = [int(_) for _ in holding_records_args['datetime']]
bar_chart(holding_datetime, 'holding_datetime', need_zero=True, num_gap=100)
bar_chart(holding_records_args['holding_list']['weight'], 'weight', has_nan=True, gap=0.1, is_long=False)
bar_chart(holding_records_args['holding_list']['shares'], 'shares', has_nan=True, num_gap=100)
bar_chart(holding_records_args['holding_list']['market_value'], 'market_value', has_nan=True, num_gap=100)
pie_chart(holding_records_args['holding_list']['category'],
          {'Warrant': '权证', 'DebtSecu': '债权', 'AShare': 'A股', 'HShare': '港股'}, 'category')

# 多线程绘制
# threads = list()
# threads.append(threading.Thread(target=bar_chart,
#                                 kwargs={'list_value': records_args['indicators_records']['total_return'],
#                                         'title': 'total_return', 'num_gap': 55, 'gap': 1}))
# threads.append(threading.Thread(target=bar_chart,
#                                 kwargs={'list_value': records_args['indicators_records']['to_date_return'],
#                                         'title': 'to_date_return', 'num_gap': 55, 'gap': 1}))
# threads.append(threading.Thread(target=bar_chart,
#                                 kwargs={'list_value': records_args['indicators_records']['total_alpha'],
#                                         'title': 'total_alpha', 'num_gap': 100}))
# threads.append(threading.Thread(target=bar_chart,
#                                 kwargs={'list_value': records_args['indicators_records']['total_beta'],
#                                         'title': 'total_beta', 'num_gap': 100}))
# threads.append(threading.Thread(target=bar_chart,
#                                 kwargs={'list_value': records_args['indicators_records']['sharp_ratio'],
#                                         'title': 'sharp_ratio', 'num_gap': 43, 'gap': 1}))
# threads.append(threading.Thread(target=bar_chart,
#                                 kwargs={'list_value': records_args['indicators_records']['max_drop_down'],
#                                         'title': 'max_drop_down', 'gap': 0.1, 'is_long': False}))
# threads.append(threading.Thread(target=bar_chart,
#                                 kwargs={'list_value': records_args['indicators_records']['information_ratio'],
#                                         'title': 'information_ratio', 'num_gap': 100}))
# for _t in threads:
#     _t.start()

# threads2 = list()
# threads2.append(threading.Thread(target=bar_chart,
#                                  kwargs={'list_value': holding_datetime, 'title': 'holding_datetime', 'need_zero': True,
#                                          'num_gap': 100}))
# threads2.append(threading.Thread(target=bar_chart, kwargs={'list_value': holding_records_args['holding_list']['weight'],
#                                                            'title': 'weight', 'has_nan': True, 'gap': 0.1,
#                                                            'is_long': False}))
# threads2.append(threading.Thread(target=bar_chart, kwargs={'list_value': holding_records_args['holding_list']['shares'],
#                                                            'title': 'shares', 'has_nan': True, 'num_gap': 100}))
# threads2.append(threading.Thread(target=bar_chart,
#                                  kwargs={'list_value': holding_records_args['holding_list']['market_value'],
#                                          'title': 'market_value', 'has_nan': True, 'num_gap': 100}))
# threads2.append(threading.Thread(target=pie_chart,
#                                  kwargs={'list_value': holding_records_args['holding_list']['category'],
#                                          'title': 'category',
#                                          'list_values': {'Warrant': '权证', 'DebtSecu': '债权', 'AShare': 'A股',
#                                                          'HShare': '港股'}}))
# for _t in threads2:
#     _t.start()
