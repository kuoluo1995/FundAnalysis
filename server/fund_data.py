import sys
import numpy as np
from collections import defaultdict

from sklearn.manifold import TSNE

sys.path.append('/home/kuoluo/projects/FundAnalysis/')
from server import common


def get_fund_date_sector(fund_ids):
    fund_dict = {}
    for f_id in fund_ids:
        fund_dict[f_id] = {}
        for holding_record in common.fund_data_dict[f_id]['holding_records']:
            fund_dict[f_id][holding_record['datetime']] = {}
            for hold in holding_record['holdings_list']:
                if hold['order_book_id'][:6] in common.stock_sector:
                    _sector = common.stock_sector[hold['order_book_id'][:6]]
                else:
                    _sector = '未知'
                if _sector not in fund_dict[f_id][holding_record['datetime']]:
                    fund_dict[f_id][holding_record['datetime']][_sector] = 0
                fund_dict[f_id][holding_record['datetime']][_sector] = hold['market_value']
    return fund_dict


def get_fund_date_income(fund_ids, start_date=None, end_date=None):
    fund_dict = {}
    for f_id in fund_ids:
        fund_dict[f_id] = {}
        first_nav = None
        for nav_dict in common.fund_data_dict[f_id]['nav']:
            if (start_date is None and end_date is None) or \
                    (start_date is None and int(nav_dict['datetime']) <= int(end_date)) or \
                    (end_date is None and int(start_date) <= int(nav_dict['datetime'])) or \
                    int(start_date) <= int(nav_dict['datetime']) <= int(end_date):
                if first_nav is None:
                    first_nav = nav_dict['unit_net_value']
                fund_dict[f_id][nav_dict['datetime']] = round((nav_dict['unit_net_value'] / first_nav - 1) * 100,
                                                              2)  # todo
    return fund_dict


def get_fund_dict(fund_ids, key):
    fund_dict = {}
    for f_id in fund_ids:
        fund_dict[f_id] = {}
        for nav_dict in common.fund_data_dict[f_id]['nav']:
            fund_dict[f_id][nav_dict['datetime']] = nav_dict[key]
    return fund_dict


def get_fund_time_nav(fund_ids, start_date=None, end_date=None, nav_type='unit_net_value'):
    fund_dict = {}
    for f_id in fund_ids:
        fund_dict[f_id] = {}
        first_nav = None
        for nav_dict in common.fund_data_dict[f_id]['nav']:
            if (start_date is None and end_date is None) or \
                    (start_date is None and int(nav_dict['datetime']) <= int(end_date)) or \
                    (end_date is None and int(start_date) <= int(nav_dict['datetime'])) or \
                    int(start_date) <= int(nav_dict['datetime']) <= int(end_date):
                if first_nav is None:
                    first_nav = nav_dict[nav_type]
                fund_dict[f_id][nav_dict['datetime']] = nav_dict[nav_type]
    return fund_dict


def get_fund_time_border(fund_ids):
    min_start_date = None
    max_end_date = None
    for f_id in fund_ids:
        if min_start_date is None or int(common.fund_data_dict[f_id]['nav'][0]['datetime']) < min_start_date:
            min_start_date = int(common.fund_data_dict[f_id]['nav'][0]['datetime'])
        if max_end_date is None or max_end_date < int(common.fund_data_dict[f_id]['nav'][-1]['datetime']):
            max_end_date = int(common.fund_data_dict[f_id]['nav'][-1]['datetime'])
    return min_start_date, max_end_date


def get_fund_layout(fund_ids, start_date, end_date):
    fund_features = {}
    for f_id in fund_ids:
        fund = common.fund_data_dict[f_id]
        fund_features[f_id] = [[], [], [], [], [], []]
        pre_nav = start_date
        for _record in fund['asset_allocation_records']:
            if start_date <= int(_record['datetime']) <= end_date:
                fund_features[f_id][0].append(_record['stock'])
                fund_features[f_id][1].append(_record['bond'])
                fund_features[f_id][2].append(_record['cash'])
                fund_features[f_id][3].append(_record['other'])
                fund_features[f_id][4].append(_record['net_asset'])
                temp = []
                for _nav in fund['nav']:
                    if pre_nav <= int(_nav['datetime']) < int(_record['datetime']):
                        temp.append(_nav['unit_net_value'])
                fund_features[f_id][5].append(np.mean(np.array(temp)))
    for _n, _att in attribute_dict.items():
        attribute_dict[_n] = {_d: [np.mean(np.array(_v)), np.max(np.array(_v)) - np.mean(np.array(_v))] for _d, _v in
                              _att.items()}
    fund_features = {}
    for f_id in fund_ids:
        fund = common.fund_data_dict[f_id]
        fund_features[f_id] = defaultdict(list)
        for _record in fund['asset_allocation_records']:
            if start_date <= int(_record['datetime']) <= end_date:
                fund_features[f_id]['stock'].append(_record['stock'])
                fund_features[f_id]['bond'].append(_record['bond'])
                fund_features[f_id]['cash'].append(_record['cash'])
                fund_features[f_id]['other'].append(_record['other'])
                fund_features[f_id]['net_asset'].append(_record['net_asset'])
                fund_features[f_id]['nav'].append(_record['nav'])
                # for _nav in fund['nav']:
                #     if pre_nav <= int(_nav['datetime']) < int(_record['datetime']):
                #         temp.append(_nav['unit_net_value'])
                # attribute_dict['nav'][_record['datetime']].append(np.mean(np.array(temp)))

    ts = TSNE(n_components=2)

    ts.fit_transform()


if __name__ == '__main__':
    # fund_3 test
    # min_start_date, max_end_date = get_fund_time_border(['163402'])
    # fund_date_income = get_fund_dict(['163402'], 'unit_net_value')

    fund_ids = common.fund_data_dict.keys()
    get_fund_layout(fund_ids)
    # print('start')
    # min_start_date, max_end_date = get_fund_time_border(['510310'])
    # fund_date_income = get_fund_date_income(['510310'], min_start_date, max_end_date)
    #
    # min_start_date, max_end_date = get_fund_time_border(fund_ids)
    # fund_date_sector = get_fund_date_sector(fund_ids)
    # fund_date_income = get_fund_date_income(fund_ids, min_start_date, max_end_date)
    # print('over')
