import numpy as np
import sys

sys.path.append('/home/kuoluo/projects/FundAnalysis/')
from server import common
from models import tsne


def get_manager_feature(m_ids):
    manager_dict = {}
    max_return = None
    max_car = None
    max_risk = None
    max_size = min_size = None
    max_alpha = None
    max_beta = None
    max_sharp_ratio = None
    max_information_ratio = None
    max_days = min_days = None
    for m_id in m_ids:
        feature = common.manager_features[m_id]
        if max_return is None or max_return < abs(feature['nav_return']):
            max_return = abs(feature['nav_return'])
        if max_car is None or max_car < abs(feature['car']):
            max_car = abs(feature['car'])
        if max_risk is None or max_risk < feature['risk']:
            max_risk = feature['risk']
        if max_size is None or max_size < feature['size']:
            max_size = feature['size']
        if min_size is None or min_size > feature['size']:
            min_size = feature['size']
        if max_days is None or max_days < feature['days']:
            max_days = feature['days']
        if min_days is None or min_days > feature['days']:
            min_days = feature['days']
        if max_alpha is None or max_alpha < abs(feature['alpha']):
            max_alpha = abs(feature['alpha'])
        if max_beta is None or max_beta < abs(feature['beta']):
            max_beta = abs(feature['beta'])
        if max_sharp_ratio is None or max_sharp_ratio < abs(feature['sharp_ratio']):
            max_sharp_ratio = abs(feature['sharp_ratio'])
        if max_information_ratio is None or max_information_ratio < abs(feature['information_ratio']):
            max_information_ratio = abs(feature['information_ratio'])
        manager_dict[m_id] = feature
    x = tsne.get_manager_feature(manager_dict, max_return, max_car, max_risk, max_size, min_size, max_alpha, max_beta,
                                 max_sharp_ratio, max_information_ratio, max_days, min_days)
    num_manager = len(m_ids)
    y, dy, iy, gains = tsne.get_y(num_manager, 2)
    p = tsne.get_p(np.array(x))
    data_2d, dy, iy, gains = tsne.t_sne(p, num_manager, y, dy, iy, gains, 2)
    result = {}
    for i, m_id in enumerate(m_ids):
        result[m_id] = {'loc': (data_2d[i][0], data_2d[i][1]), 'days': common.manager_features[m_id]['days'],
                        'name': common.manager_dict[m_id]['name'],
                        'size': common.manager_features[m_id]['days'] / max_days,
                        'amcs': common.manager_features[m_id]['amcs']}
    return result

def get_manager_name():
    pass

# def get_manager_name():
#     manager_dict = {}
#     for m_id, m_v in common.fund_manager.items():
#         manager_dict[m_id] = m_v['name']
#     return manager_dict  # m_di : m_name
#
#
# def get_manager_times(m_ids):
#     min_start_date = None  # 所有基金经理里最旧的更新
#     max_end_date = None  # 所有基金经理里最新的更新
#     manager_datetime = {}  # m_id m_name[f_id][start_date-end_date]
#     for m_id in m_ids:
#         m_id = m_id.strip()
#         manager_datetime[m_id + ' ' + common.fund_manager[m_id]['name']] = {}
#         for f_id, f_values in common.fund_manager[m_id]['funds'].items():
#             manager_datetime[m_id + ' ' + common.fund_manager[m_id]['name']][f_id] = list()
#             for f_v in f_values:
#                 manager_datetime[m_id + ' ' + common.fund_manager[m_id]['name']][f_id].append(
#                     f_v['start_date'] + '-' + f_v['end_date'])
#                 if min_start_date is None or min_start_date > int(f_v['start_date']):
#                     min_start_date = int(f_v['start_date'])
#                 if max_end_date is None or max_end_date < int(f_v['end_date']):
#                     max_end_date = int(f_v['end_date'])
#     return manager_datetime, min_start_date, max_end_date
#
#
# def get_manager_dict(m_ids, key, sub_key):
#     manager_dict = {}
#     for m_id in m_ids:
#         _key = m_id + ' ' + common.fund_manager[m_id]['name']
#         manager_dict[_key] = {}
#         for f_id, f_values in common.fund_manager[m_id]['funds'].items():
#             if f_id not in manager_dict[_key]:
#                 manager_dict[_key][f_id] = {}
#             for f_v in f_values:
#                 for _v in f_v[key]:
#                     manager_dict[_key][f_id][_v['datetime']] = _v[sub_key]
#     return manager_dict
#
#
# def get_manager_asset(m_ids):
#     return get_manager_dict(m_ids, 'asset_allocation_records', 'net_asset')
#
#
# def get_manager_nav(m_ids):
#     return get_manager_dict(m_ids, 'nav', 'unit_net_value')
#
#
# def get_manager_acc_net(m_ids):
#     return get_manager_dict(m_ids, 'nav', 'acc_net_value')


# def get_manager_income(m_ids, start_date=None, end_date=None):
#     manager_income = {}
#     for m_id in m_ids:
#         _key = m_id + ' ' + common.fund_manager[m_id]['name']
#         manager_income[_key] = {}
#         for f_id, _values in common.fund_manager[m_id]['funds'].items():
#             first_nav = None
#             manager_income[_key][f_id] = {}
#             for _value in _values:
#                 for _nav in _value['nav']:
#                     if (start_date is None and end_date is None) or \
#                             (start_date is None and int(_nav['datetime']) <= int(end_date)) or \
#                             (end_date is None and int(start_date) <= int(_nav['datetime'])) or \
#                             int(start_date) <= int(_nav['datetime']) <= int(end_date):
#                         if first_nav is None:
#                             first_nav = _nav['unit_net_value']
#                         manager_income[_key][f_id][_nav['datetime']] = (_nav['unit_net_value'] / first_nav - 1) * 100
#     return manager_income


# def get_manager_date_sector(m_ids):
#     manager_dict = {}
#     for m_id in m_ids:
#         _key = m_id + ' ' + common.fund_manager[m_id]['name']
#         manager_dict[_key] = {}
#         for f_id, _values in common.fund_manager[m_id]['funds'].items():
#             for _value in _values:
#                 for _date, holding_list in _value['holding_records'].items():
#                     if _date not in manager_dict[_key]:
#                         manager_dict[_key][_date] = {}
#                     if f_id not in manager_dict[_key][_date]:
#                         manager_dict[_key][_date][f_id] = {}
#                     for holding in holding_list:
#                         if holding['order_book_id'][:6] not in common.stock_sector:
#                             _sector = '未知'
#                         else:
#                             _sector = common.stock_sector[holding['order_book_id'][:6]]
#                         if _sector not in manager_dict[_key][_date][f_id]:
#                             manager_dict[_key][_date][f_id][_sector] = 0
#                         manager_dict[_key][_date][f_id][_sector] += holding['market_value']
#     return manager_dict


if __name__ == '__main__':
    get_manager_feature(list(common.manager_dict.keys()))
    #     manager_name_dict = get_manager_name()
    #     manager_time_dict, start_date, end_date = get_manager_times(manager_name_dict.keys())
    #     # 基金经理规模
    #     manager_asset_dict = get_manager_asset(manager_name_dict.keys())
    #     manager_asset = object_merge_fund(manager_asset_dict, merge_type='sum', sort_type='key')
    #     all_labels = dict2labels(manager_asset, is_sort=True)
    #     value_dict = dict2values(manager_asset, all_labels, none_value='previous')
    #     # 基金经理净值
    #     manager_nav_dict = get_manager_nav(manager_name_dict.keys())
    #     manager_nav = object_merge_fund(manager_nav_dict, merge_type='mean', sort_type='key')
    #     all_labels = dict2labels(manager_nav, is_sort=True)
    #     value_dict = dict2values(manager_nav, all_labels, none_value='previous')
    #     # 基金经理收益，按时间切片取出就可以直接看收益排行
    #     manager_income_dict = get_manager_income(manager_name_dict.keys(), start_date, end_date)
    #     manager_income = object_merge_fund(manager_income_dict, merge_type='mean', sort_type='key')
    #     all_labels = dict2labels(manager_income, is_sort=True)
    #     value_dict = dict2values(manager_income, all_labels, none_value='previous')
    print('over')
