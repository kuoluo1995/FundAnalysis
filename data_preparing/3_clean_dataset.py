import json
import numpy as np

ProjectPath = '/home/kuoluo/projects/FundAnalysis'
with open('/home/kuoluo/data/fund/fund_data.json', 'r') as fp:
    fund_data = json.load(fp)

good_fund = []
error_fund_detail = {}  # fund_id: {error: [], 'manager_records':  {manager_id: [errors}}


def add_error(_id, _type, _sub_id, _error):
    if _id not in error_fund_detail:
        error_fund_detail[f_id] = {'error': [], 'manager_records': {}, 'asset_allocation_records': {},
                                   'indicators_records': {}, 'holding_records': {}}
    if _sub_id is None:
        error_fund_detail[f_id][_type].append(_error)
    else:
        if _sub_id not in error_fund_detail[f_id][_type]:
            error_fund_detail[f_id][_type][_sub_id] = []
        error_fund_detail[f_id][_type][_sub_id].append(_error)


# 检查一级列表的数据
for fund in fund_data:
    bad_fund = False
    f_id = fund['fund_id']
    if fund['transition_time'] > 0:
        add_error(f_id, 'error', None, 'transition_time')
        bad_fund = True
    # if int(fund['de_listed_date']) > 0:
    #     add_error(f_id, 'error', None, 'de_listed_date')
    #     bad_fund = True
    for _record in fund['indicators_records']:
        if np.isnan(_record['average_size']):
            add_error(f_id, 'indicators_records', _record['datetime'], 'average_size')
            bad_fund = True
    new_date = int(fund['indicators_records'][-1]['datetime'])
    temp_list = list()
    for _record in fund['manager_records']:
        if _record['name'] is None or (_record['name']).strip() == '':
            add_error(f_id, 'manager_records', _record['id'], 'name')
            bad_fund = True
        if int(_record['days']) == 0:
            add_error(f_id, 'manager_records', _record['id'], 'days')
            bad_fund = True
        _record.pop('return')
        if _record['title'] != '基金经理':
            continue
        if new_date <= int(_record['start_date']):
            continue
        temp_list.append(_record)
    fund['manager_records'] = temp_list
    temp_list = list()
    for _record in fund['nav']:
        if int(_record['datetime']) <= new_date:
            temp_list.append(_record)
    fund['nav'] = temp_list
    temp_list = list()
    for _record in fund['rating']:
        if int(_record['datetime']) <= new_date:
            temp_list.append(_record)
    fund['rating'] = temp_list
    temp_list = list()
    for _record in fund['holder_structure']:
        if int(_record['date']) <= new_date:
            temp_list.append(_record)
    fund['holder_structure'] = temp_list
    for _record in fund['holding_records']:
        for _v in _record['holdings_list']:
            if np.isnan(_v['weight']):
                add_error(f_id, 'holding_records', _record['datetime'], _v['order_book_id'] + ':weight')
                bad_fund = True
            if np.isnan(_v['shares']):
                add_error(f_id, 'holding_records', _record['datetime'], _v['order_book_id'] + ':shares')
                bad_fund = True
            if np.isnan(_v['market_value']):
                add_error(f_id, 'holding_records', _record['datetime'], _v['order_book_id'] + ':market_value')
                bad_fund = True
    if not bad_fund:
        good_fund.append(fund)
print('good_fund:{}, error_fund:{}, use_fund:{:.2f}%'.format(len(good_fund), len(error_fund_detail.keys()),
                                                             len(good_fund) * 100 / len(fund_data)))
# max([_return for _return in holding_records_args['holding_list']['weight'] if not pd.isnull(_return)])
# with open(ProjectPath + '/data/error_funds_detail.json', 'w') as wp:
#     json.dump(error_fund_detail, wp)
with open(ProjectPath + '/data/fund_date.json', 'w') as wp:
    json.dump(good_fund, wp)

print('over')
