import numpy as np
import sys

from tools.show_tool import dict2labels, dict2values, object_merge_fund

sys.path.append('/home/kuoluo/projects/FundAnalysis/')
from server import common


def get_manager_name():
    manager_dict = {}
    for m_id, m_v in common.fund_manager.items():
        manager_dict[m_id] = m_v['name']
    return manager_dict  # m_di : m_name


def get_manager_times(m_ids):
    min_start_date = None  # 所有基金经理里最旧的更新
    max_end_date = None  # 所有基金经理里最新的更新
    manager_datetime = {}  # m_id m_name[f_id][start_date-end_date]
    for m_id in m_ids:
        m_id = m_id.strip()
        manager_datetime[m_id + ' ' + common.fund_manager[m_id]['name']] = {}
        for f_id, f_values in common.fund_manager[m_id]['funds'].items():
            manager_datetime[m_id + ' ' + common.fund_manager[m_id]['name']][f_id] = list()
            for f_v in f_values:
                manager_datetime[m_id + ' ' + common.fund_manager[m_id]['name']][f_id].append(
                    f_v['start_date'] + '-' + f_v['end_date'])
                if min_start_date is None or min_start_date > int(f_v['start_date']):
                    min_start_date = int(f_v['start_date'])
                if max_end_date is None or max_end_date < int(f_v['end_date']):
                    max_end_date = int(f_v['end_date'])
    return manager_datetime, min_start_date, max_end_date


def get_manager_dict(m_ids, key, sub_key):
    manager_dict = {}
    for m_id in m_ids:
        _key = m_id + ' ' + common.fund_manager[m_id]['name']
        manager_dict[_key] = {}
        for f_id, f_values in common.fund_manager[m_id]['funds'].items():
            if f_id not in manager_dict[_key]:
                manager_dict[_key][f_id] = {}
            for f_v in f_values:
                for _v in f_v[key]:
                    manager_dict[_key][f_id][_v['datetime']] = _v[sub_key]
    return manager_dict


def get_manager_asset(m_ids):
    return get_manager_dict(m_ids, 'asset_allocation_records', 'net_asset')


def get_manager_nav(m_ids):
    return get_manager_dict(m_ids, 'nav', 'unit_net_value')


def get_manager_acc_net(m_ids):
    return get_manager_dict(m_ids, 'nav', 'acc_net_value')


def get_manager_income(m_ids, start_date=None, end_date=None):
    manager_income = {}
    for m_id in m_ids:
        _key = m_id + ' ' + common.fund_manager[m_id]['name']
        manager_income[_key] = {}
        for f_id, _values in common.fund_manager[m_id]['funds'].items():
            first_nav = None
            manager_income[_key][f_id] = {}
            for _value in _values:
                for _nav in _value['nav']:
                    if (start_date is None and end_date is None) or \
                            (start_date is None and int(_nav['datetime']) <= int(end_date)) or \
                            (end_date is None and int(start_date) <= int(_nav['datetime'])) or \
                            int(start_date) <= int(_nav['datetime']) <= int(end_date):
                        if first_nav is None:
                            first_nav = _nav['unit_net_value']
                        manager_income[_key][f_id][_nav['datetime']] = (_nav['unit_net_value'] / first_nav - 1) * 100
    return manager_income


def get_manager_sector(m_ids):
    manager_dict = {}
    for m_id in m_ids:
        _key = m_id + ' ' + common.fund_manager[m_id]['name']
        manager_dict[_key] = {}
        for f_id, _values in common.fund_manager[m_id]['funds'].items():
            manager_dict[_key][f_id] = {}
            for _value in _values:
                for _, holding_list in _value['holding_records'].items():
                    for holding in holding_list:
                        if holding['order_book_id'][:6] not in common.stock_sector:
                            _sector = '未知'
                        else:
                            _sector = common.stock_sector[holding['order_book_id'][:6]]
                        if _sector not in manager_dict[_key][f_id]:
                            manager_dict[_key][f_id][_sector] = 0
                        manager_dict[_key][f_id][_sector] += holding['market_value']
    return manager_dict


if __name__ == '__main__':
    manager_name_dict = get_manager_name()
    manager_time_dict, start_date, end_date = get_manager_times(manager_name_dict.keys())
    # 基金经理规模
    manager_asset_dict = get_manager_asset(manager_name_dict.keys())
    manager_asset = object_merge_fund(manager_asset_dict, merge_type='sum', sort_type='key')
    all_labels = dict2labels(manager_asset, is_sort=True)
    value_dict = dict2values(manager_asset, all_labels, none_value='previous')
    # 基金经理净值
    manager_nav_dict = get_manager_nav(manager_name_dict.keys())
    manager_nav = object_merge_fund(manager_nav_dict, merge_type='mean', sort_type='key')
    all_labels = dict2labels(manager_nav, is_sort=True)
    value_dict = dict2values(manager_nav, all_labels, none_value='previous')
    # 基金经理行业分布
    manager_sector_dict = get_manager_sector(manager_name_dict.keys())
    manager_sector = object_merge_fund(manager_sector_dict, merge_type='sum', sort_type='value')
    all_labels = dict2labels(manager_sector, is_sort=False)
    value_dict = dict2values(manager_sector, all_labels, none_value='zero')
    # 基金经理收益，按时间切片取出就可以直接看收益排行
    manager_income_dict = get_manager_income(manager_name_dict.keys(), start_date, end_date)
    manager_income = object_merge_fund(manager_income_dict, merge_type='mean', sort_type='key')
    all_labels = dict2labels(manager_income, is_sort=True)
    value_dict = dict2values(manager_income, all_labels, none_value='previous')
    print('over')
