import json
import os

project_path = '/home/kuoluo/projects/FundAnalysis'
fund_files = os.listdir(project_path + '/data/fund_features')
with open(project_path + '/data/dictionary/manager_features.json', 'r', encoding='UTF-8') as rp:
    manager_dictionary = json.load(rp)
with open(project_path + '/data/dictionary/fund_dict.json', 'r', encoding='UTF-8') as rp:
    fund_dictionary = json.load(rp)
fund_dict = {}
max_stock = min_stock = None
max_bond = min_bond = None
max_cash = min_cash = None
max_other = min_other = None
max_size = min_size = None
max_alpha = min_alpha = None
max_beta = min_beta = None
max_sharp_ratio = min_sharp_ratio = None
max_drop_down = min_drop_down = None
max_information_ratio = min_information_ratio = None
max_return = min_return = None
max_risk = min_risk = None
max_car = min_car = None
max_instl_weight = min_instl_weight = None
max_days = min_days = None
max_manager_days = min_manager_days = None
for file in fund_files:
    with open(project_path + '/data/fund_features/' + file, 'r', encoding='UTF-8') as rp:
        feature = list(json.load(rp).items())[-1][1]
    if max_stock is None or max_stock < feature['stock']:
        max_stock = feature['stock']
    if max_bond is None or max_bond < feature['bond']:
        max_bond = feature['bond']
    if max_cash is None or max_cash < feature['cash']:
        max_cash = feature['cash']
    if max_other is None or max_other < feature['other']:
        max_other = feature['other']
    if max_size is None or max_size < feature['size']:
        max_size = feature['size']
    if max_alpha is None or max_alpha < feature['alpha']:
        max_alpha = feature['alpha']
    if max_beta is None or max_beta < feature['beta']:
        max_beta = feature['beta']
    if max_sharp_ratio is None or max_sharp_ratio < feature['sharp_ratio']:
        max_sharp_ratio = feature['sharp_ratio']
    if max_drop_down is None or max_drop_down < feature['max_drop_down']:
        max_drop_down = feature['max_drop_down']
    if max_information_ratio is None or max_information_ratio < feature['information_ratio']:
        max_information_ratio = feature['information_ratio']
    if max_return is None or max_return < feature['nav_return']:
        max_return = feature['nav_return']
    if max_risk is None or max_risk < feature['risk']:
        max_risk = feature['risk']
    if max_instl_weight is None or max_instl_weight < feature['instl_weight']:
        max_instl_weight = feature['instl_weight']
    if max_car is None or max_car < feature['car']:
        max_car = feature['car']
    feature['days'] = fund_dictionary[file[:-5]]['days']
    if max_days is None or max_days < feature['days']:
        max_days = feature['days']
    is_manager = False
    manager_days = 0
    for m_id, _v in feature['manager_ids'].items():
        if not is_manager and _v['name'] == '基金经理':
            is_manager = True
            manager_days = manager_dictionary[m_id]['days']
            continue
        if is_manager and _v['name'] == '基金经理助理':
            continue
        manager_days = manager_dictionary[m_id]['days'] if manager_days < manager_dictionary[m_id][
            'days'] else manager_days
    if max_manager_days is None or max_manager_days < manager_days:
        max_manager_days = manager_days
    feature['manager_days'] = manager_days
    if min_stock is None or min_stock > feature['stock']:
        min_stock = feature['stock']
    if min_bond is None or min_bond > feature['bond']:
        min_bond = feature['bond']
    if min_cash is None or min_cash > feature['cash']:
        min_cash = feature['cash']
    if min_other is None or min_other > feature['other']:
        min_other = feature['other']
    if min_size is None or min_size > feature['size']:
        min_size = feature['size']
    if min_alpha is None or min_alpha > feature['alpha']:
        min_alpha = feature['alpha']
    if min_beta is None or min_beta > feature['beta']:
        min_beta = feature['beta']
    if min_sharp_ratio is None or min_sharp_ratio > feature['sharp_ratio']:
        min_sharp_ratio = feature['sharp_ratio']
    if min_drop_down is None or min_drop_down > feature['max_drop_down']:
        min_drop_down = feature['max_drop_down']
    if min_information_ratio is None or min_information_ratio > feature['information_ratio']:
        min_information_ratio = feature['information_ratio']
    if min_return is None or min_return > feature['nav_return']:
        min_return = feature['nav_return']
    if min_risk is None or min_risk > feature['risk']:
        min_risk = feature['risk']
    if min_instl_weight is None or min_instl_weight > feature['instl_weight']:
        min_instl_weight = feature['instl_weight']
    if min_car is None or min_car > feature['nav_return'] - feature['hs300_return']:
        min_car = feature['nav_return'] - feature['hs300_return']
    if min_days is None or min_days > feature['days']:
        min_days = feature['days']
    if min_manager_days is None or min_manager_days > manager_days:
        min_manager_days = manager_days
    feature.pop('hs300')
    feature.pop('unit_nav')
    feature.pop('detail_unit_navs')
    feature.pop('detail_hs300s')
    feature.pop('hs300_return')
    feature.pop('manager_ids')
    fund_dict[file[:-5]] = feature

for f_id, _values in fund_dict.items():
    fund_dict[f_id]['stock'] = (_values['stock'] - min_stock) / (max_stock - min_stock)
    fund_dict[f_id]['bond'] = (_values['bond'] - min_bond) / (max_bond - min_bond)
    fund_dict[f_id]['cash'] = (_values['cash'] - min_cash) / (max_cash - min_cash)
    fund_dict[f_id]['other'] = (_values['other'] - min_other) / (max_other - min_other)
    fund_dict[f_id]['size'] = (_values['size'] - min_size) / (max_size - min_size)
    fund_dict[f_id]['alpha'] = (_values['alpha'] - min_alpha) / (max_alpha - min_alpha)
    fund_dict[f_id]['beta'] = (_values['beta'] - min_beta) / (max_beta - min_beta)
    fund_dict[f_id]['sharp_ratio'] = (_values['sharp_ratio'] - min_sharp_ratio) / (max_sharp_ratio - min_sharp_ratio)
    fund_dict[f_id]['max_drop_down'] = (_values['max_drop_down'] - min_drop_down) / (max_drop_down - min_drop_down)
    fund_dict[f_id]['information_ratio'] = (_values['information_ratio'] - min_information_ratio) / (
            max_information_ratio - min_information_ratio)
    fund_dict[f_id]['nav_return'] = (_values['nav_return'] - min_return) / (max_return - min_return)
    fund_dict[f_id]['risk'] = (_values['risk'] - min_risk) / (max_risk - min_risk)
    fund_dict[f_id]['instl_weight'] = (_values['instl_weight'] - min_instl_weight) / (
            max_instl_weight - min_instl_weight)
    fund_dict[f_id]['car'] = (_values['car'] - min_car) / (max_car - min_car)
    fund_dict[f_id]['days'] = (_values['days'] - min_days) / (max_days - min_days)
    fund_dict[f_id]['manager_days'] = (_values['manager_days'] - min_manager_days) / (
            max_manager_days - min_manager_days)
with open(project_path + '/data/dictionary/global_fund_features.json', 'w', encoding='UTF-8') as wp:
    json.dump(fund_dict, wp)
print('over')
