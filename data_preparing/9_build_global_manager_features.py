import json

project_path = '/home/kuoluo/projects/FundAnalysis'
manager_dict = {}
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
max_num_fund = min_num_fund = None

with open(project_path + '/data/dictionary/manager_features.json', 'r', encoding='UTF-8') as rp:
    features = json.load(rp)
for m_id, feature in features.items():
    feature.pop('amcs')
    feature.pop('unit_nav')
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
    if max_days is None or max_days < feature['days']:
        max_days = feature['days']
    if max_num_fund is None or max_num_fund < feature['num_fund']:
        max_num_fund = feature['num_fund']
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
    if min_car is None or min_car > feature['car']:
        min_car = feature['car']
    if min_days is None or min_days > feature['days']:
        min_days = feature['days']
    if min_num_fund is None or min_num_fund > feature['num_fund']:
        min_num_fund = feature['num_fund']
    manager_dict[m_id] = feature

for m_id, _values in manager_dict.items():
    manager_dict[m_id]['stock'] = (_values['stock'] - min_stock) / (max_stock - min_stock)
    manager_dict[m_id]['bond'] = (_values['bond'] - min_bond) / (max_bond - min_bond)
    manager_dict[m_id]['cash'] = (_values['cash'] - min_cash) / (max_cash - min_cash)
    manager_dict[m_id]['other'] = (_values['other'] - min_other) / (max_other - min_other)
    manager_dict[m_id]['size'] = (_values['size'] - min_size) / (max_size - min_size)
    manager_dict[m_id]['alpha'] = (_values['alpha'] - min_alpha) / (max_alpha - min_alpha)
    manager_dict[m_id]['beta'] = (_values['beta'] - min_beta) / (max_beta - min_beta)
    manager_dict[m_id]['sharp_ratio'] = (_values['sharp_ratio'] - min_sharp_ratio) / (max_sharp_ratio - min_sharp_ratio)
    manager_dict[m_id]['max_drop_down'] = (_values['max_drop_down'] - min_drop_down) / (max_drop_down - min_drop_down)
    manager_dict[m_id]['information_ratio'] = (_values['information_ratio'] - min_information_ratio) / (
            max_information_ratio - min_information_ratio)
    manager_dict[m_id]['nav_return'] = (_values['nav_return'] - min_return) / (max_return - min_return)
    manager_dict[m_id]['risk'] = (_values['risk'] - min_risk) / (max_risk - min_risk)
    manager_dict[m_id]['instl_weight'] = (_values['instl_weight'] - min_instl_weight) / (
            max_instl_weight - min_instl_weight)
    manager_dict[m_id]['car'] = (_values['car'] - min_car) / (max_car - min_car)
    manager_dict[m_id]['days'] = (_values['days'] - min_days) / (max_days - min_days)
    manager_dict[m_id]['num_fund'] = (_values['num_fund'] - min_num_fund) / (max_num_fund - min_num_fund)
with open(project_path + '/data/dictionary/global_manager_features.json', 'w', encoding='UTF-8') as wp:
    json.dump(manager_dict, wp)
print('over')
