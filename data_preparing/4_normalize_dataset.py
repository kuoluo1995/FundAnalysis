import json
from collections import defaultdict
from sklearn.manifold import TSNE
import numpy as np

ProjectPath = '/home/kuoluo/projects/FundAnalysis'
with open('/home/kuoluo/data/fund/fund_data.json', 'r', encoding='UTF-8') as fp:
    fund_data = json.load(fp)

good_fund = []
pre_nav = 20190000
attribute_dict = {'stock': defaultdict(list), 'bond': defaultdict(list), 'cash': defaultdict(list),
                  'other': defaultdict(list), 'net_asset': defaultdict(list), 'nav': defaultdict(list),
                  'manager': defaultdict(int), 'company': defaultdict(int)}
for fund in fund_data:
    if int(fund['stop_date']) != 0 and int(fund['stop_date']) < 20190000:
        continue
    bad_fund = False
    for _record in fund['nav']:
        if _record['unit_net_value'] > 20:
            bad_fund = True
            break
    for _record in fund['asset_allocation_records']:
        if _record['cash'] > 2.8:
            bad_fund = True
            break
    if bad_fund:
        continue
    attribute_dict['company'][fund['amc']] += 1
    _temp = list()
    for _record in fund['manager_records']:
        if (int(_record['end_date']) != 0 and int(_record['end_date']) < 20190000) or int(
                _record['start_date']) > 20200000:
            continue
        attribute_dict['manager'][_record['id']] += 1
        _temp.append(_record)
    fund['manager_records'] = _temp
    _temp = list()
    for _record in fund['asset_allocation_records']:
        if int(_record['datetime']) < 20190000 or int(_record['datetime']) > 20200000:
            continue
        attribute_dict['stock'][_record['datetime']].append(_record['stock'])
        attribute_dict['bond'][_record['datetime']].append(_record['bond'])
        attribute_dict['cash'][_record['datetime']].append(_record['cash'])
        attribute_dict['other'][_record['datetime']].append(_record['other'])
        attribute_dict['net_asset'][_record['datetime']].append(_record['net_asset'])
        _record['nav'] = dict()
        for _nav in fund['nav']:
            if pre_nav <= int(_nav['datetime']) <= int(_record['datetime']):
                _record['nav'][_nav['datetime']] = _nav['unit_net_value']
        _temp.append(_record)
    fund['asset_allocation_records'] = _temp
    good_fund.append(fund)
company_count = sorted(attribute_dict['company'].items(), key=lambda d: d[1], reverse=True)
company_count = {_c_c[0]: i for i, _c_c in enumerate(company_count)}
manager_count = sorted(attribute_dict['manager'].items(), key=lambda d: d[1], reverse=True)
manager_count = {_c_c[0]: i for i, _c_c in enumerate(manager_count)}

for _n, _att in attribute_dict.items():
    if _n == 'manager' or _n == 'company':
        continue
    attribute_dict[_n] = {_d: [np.mean(np.array(_l)), np.max(np.array(_l)) - np.mean(np.array(_l))] for _d, _l in
                          _att.items()}

tsne_date_fund = {}
for fund in good_fund:
    for _record in fund['asset_allocation_records']:
        if np.isnan((_record['net_asset'] - attribute_dict['net_asset'][_record['datetime']][0]) /
                    attribute_dict['net_asset'][_record['datetime']][1]):
            continue
        if _record['datetime'] not in tsne_date_fund:
            tsne_date_fund[_record['datetime']] = {}
        tsne_date_fund[_record['datetime']][fund['fund_id']] = {
            'stock': _record['stock'],
            'bond': _record['bond'],
            'cash': _record['cash'],
            'other': _record['other'],
            'net_asset': (_record['net_asset'] - attribute_dict['net_asset'][_record['datetime']][0]) /
                         attribute_dict['net_asset'][_record['datetime']][1],
            'company': company_count[fund['amc']]}

        #         'stock': (_record['stock'] - attribute_dict['stock'][_record['datetime']][0]) /
        #         attribute_dict['stock'][_record['datetime']][1],
        #     'bond': (_record['bond'] - attribute_dict['bond'][_record['datetime']][0]) /
        #     attribute_dict['bond'][_record['datetime']][1],
        # 'cash': (_record['cash'] - attribute_dict['cash'][_record['datetime']][0]) /
        # attribute_dict['cash'][_record['datetime']][1],
        # 'other': (_record['other'] - attribute_dict['other'][_record['datetime']][0]) /
        # attribute_dict['other'][_record['datetime']][1],
        # 'net_asset': (_record['net_asset'] - attribute_dict['net_asset'][_record['datetime']][0]) /
        # attribute_dict['net_asset'][_record['datetime']][1],
        # 'company': company_count[fund['amc']]}
        for _m in fund['manager_records']:
            tsne_date_fund[_record['datetime']][fund['fund_id']]['manager'] = manager_count[_m['id']]
        tsne_date_fund[_record['datetime']][fund['fund_id']]['nav'] = {}
        for _nav in fund['nav']:
            tsne_date_fund[_record['datetime']][fund['fund_id']]['nav'][_nav['datetime']] = _nav['unit_net_value']
        tsne_date_fund[_record['datetime']][fund['fund_id']]['mean_nav'] = np.array(
            [v for _, v in tsne_date_fund[_record['datetime']][fund['fund_id']]['nav'].items()]).mean()
tsne_date_fund_loc = {}
ts = TSNE(n_components=2)
for _, _date_values in tsne_date_fund.items():
    fund_array = []
    for _fid, _v in _date_values.items():
        fund_array.append(
            [_v['company'], _v['manager'], _v['stock'], _v['bond'], _v['cash'], _v['other'], _v['net_asset'],
             _v['mean_nav']])
    ts.fit_transform(np.array(fund_array))
    i = 0
    tsne_date_fund_loc[_] = {}
    for _fid, _v in _date_values.items():
        tsne_date_fund_loc[_][_fid] = {}
        tsne_date_fund_loc[_][_fid]['x'] = float(ts.embedding_[i][0])
        tsne_date_fund_loc[_][_fid]['y'] = float(ts.embedding_[i][1])
        tsne_date_fund_loc[_][_fid]['size'] = float(_v['net_asset'])
        tsne_date_fund_loc[_][_fid]['nav'] = float(_v['mean_nav'])
        i += 1

# max([_return for _return in holding_records_args['holding_list']['weight'] if not pd.isnull(_return)])
# with open(ProjectPath + '/data/error_funds_detail.json', 'w') as wp:
#     json.dump(error_fund_detail, wp)
with open(ProjectPath + '/data/tsne_date_loc.json', 'w') as wp:
    json.dump(tsne_date_fund_loc, wp)

print('over')
