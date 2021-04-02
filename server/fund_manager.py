import numpy as np
import sys

sys.path.append('/home/kuoluo/projects/FundAnalysis/')
from server import common
from models import tsne, pca
from tools import color_tool, normal_tool


def get_manager_ranks(source_f_ids, weights, start_date, end_date, num_top=10):
    m_ids = set()
    for _date, managers in common.manager_fund_dict.items():
        if int(start_date) <= int(_date) <= int(end_date):
            for m_id, f_ids in managers.items():
                for f_id in f_ids:
                    if f_id in source_f_ids:
                        m_ids.add(m_id)
    ranks = {}
    managers = common.manager_features
    for _date, manager_features in managers.items():
        if int(start_date) <= int(_date) <= int(end_date):
            for _id, _feature in manager_features.items():
                _sum = 0
                for _name, _v in weights.items():
                    if _name not in _feature:
                        continue
                    _sum += float(weights[_name]) * _feature[_name]
                ranks[_id] = _sum
    ranks = sorted(ranks.items(), key=lambda v: v[1], reverse=True)
    i = 0
    new_m_ids = list()
    for m_id, _ in ranks:
        if i >= num_top:
            break
        if m_id in m_ids:
            continue
        new_m_ids.append(m_id)
        i += 1
    return list(m_ids), new_m_ids


def get_manager_feature(m_ids, start_date, end_date):
    manager_dict = {m_id: {} for m_id in m_ids}
    keys = {'one_year_car', 'three_year_car'}
    for _date, managers in common.manager_features.items():
        if int(start_date) <= int(_date) <= int(end_date):
            for m_id in m_ids:
                if m_id in managers.keys():
                    if len(manager_dict[m_id]) == 0:
                        for name, _value in managers[m_id].items():
                            if 'hs300' in name or 'return' in name:
                                continue
                            manager_dict[m_id][name] = list()
                        manager_dict[m_id]['three_year_car'] = list()
                        manager_dict[m_id]['one_year_car'] = list()
                    for name, _value in managers[m_id].items():
                        if 'hs300' in name or 'return' in name:
                            continue
                        manager_dict[m_id][name].append(_value)
                        keys.add(name)
    manager_dict = {m_id: {_name: np.mean(_list) for _name, _list in _values.items()} for m_id, _values in
                    manager_dict.items()}

    min_max_dict = normal_tool.get_max_min_feature(manager_dict, keys)
    manager_dict = normal_tool.get_normal_feature(manager_dict, min_max_dict)
    x = tsne.get_manager_feature(manager_dict)
    data_2d = pca.train(x)
    colors = color_tool.get_hex_colors_by_num(len(m_ids))
    result = {}
    for i, m_id in enumerate(m_ids):
        size = [manager_dict[m_id]['one_quarter_car']['norm']]
        if not np.isnan(manager_dict[m_id]['one_year_car']['norm']):
            size.append(manager_dict[m_id]['one_year_car']['norm'])
        if not np.isnan(manager_dict[m_id]['three_year_car']['norm']):
            size.append(manager_dict[m_id]['three_year_car']['norm'])
        result[m_id] = {'loc': [float(data_2d[i][0]), float(data_2d[i][1])], 'days': common.manager_dict[m_id]['days'],
                        'cn_name': common.manager_dict[m_id]['cn_name'], 'size': np.mean(size), 'color': colors[i],
                        'en_name': common.manager_dict[m_id]['en_name'], 'id': common.manager_dict[m_id]['index']}
        if result[m_id]['en_name'] == 'HanDong':
            result[m_id]['color'] = '#3A9E85'
        if result[m_id]['en_name'] == 'HuangWei':
            result[m_id]['color'] = '#6EEBCB'
        if result[m_id]['en_name'] == 'GouFei':
            result[m_id]['color'] = '#9E8742'
        if result[m_id]['en_name'] == 'WangYanfei':
            result[m_id]['color'] = '#9E8742'
        # case 1 149 去掉207
        if result[m_id]['en_name'] == 'ZhaoHang':
            result[m_id]['color'] = '#e41a1c'
        if result[m_id]['en_name'] == 'ChenHu':
            result[m_id]['color'] = '#377eb8'
        if result[m_id]['en_name'] == 'WangYihuan':
            result[m_id]['color'] = '#4daf4a'
        if result[m_id]['en_name'] == 'ChenWeiyan':
            result[m_id]['color'] = '#984ea3'

        if result[m_id]['id'] == 606:
            result[m_id]['color'] = '#984ea3'
        if result[m_id]['id'] == 321:
            result[m_id]['color'] = '#4daf4a'
        if result[m_id]['id'] == 417:
            result[m_id]['color'] = '#377eb8'
    return result


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
    weights = {'one_quarter_return': 1.0, 'one_year_return': 1.0, 'three_year_return': 1.0, 'max_drop_down': 0.0,
               'risk': 1.0, 'sharp_ratio': 0.0, 'information_ratio': 0.0, 'alpha': 0.0, 'beta': 0.0, 'size': 1.0,
               'instl_weight': 0.0}
    m_ids, exet_m_ids = get_manager_ranks(['001740'], weights, '20130425', '20191231')
    _ = get_manager_feature(list(m_ids) + exet_m_ids, '20130425', '20191231')
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
