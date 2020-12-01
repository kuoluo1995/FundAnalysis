import json
import numpy as np

ProjectPath = '/home/kuoluo/projects/FundAnalysis'
with open('/home/kuoluo/data/fund_data.json', 'r') as fp:
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
    for key, value in fund.items():
        if key == 'fund_manager':
            if value is None:
                add_error(f_id, 'error', None, 'fund_manager')
                bad_fund = True
        if key == 'de_listed_date':
            if int(value) > 0:
                add_error(f_id, 'error', None, 'de_listed_date')
                bad_fund = True
        if key == 'latest_size':
            if value > 17552660689:
                add_error(f_id, 'error', None, 'latest_size')
                bad_fund = True
        if key == 'manager_records':
            for _records in value:
                if _records['name'] is None or (_records['name']).strip() == '':
                    add_error(f_id, 'manager_records', _records['manager_id'], 'name')
                    bad_fund = True
                if int(_records['days']) == 0:
                    add_error(f_id, 'manager_records', _records['manager_id'], 'days')
                    bad_fund = True
                if np.isnan(_records['return']) or _records['return'] > 625:
                    add_error(f_id, 'manager_records', _records['manager_id'], 'return')
                    bad_fund = True
        if key == 'asset_allocation_records':
            for _records in value:
                if _records['stock'] > 1.0:
                    add_error(f_id, 'asset_allocation_records', _records['datetime'], 'stock')
                    bad_fund = True
                if _records['cash'] > 2.8:
                    add_error(f_id, 'asset_allocation_records', _records['datetime'], 'cash')
                    bad_fund = True
                if _records['other'] < 0 or _records['other'] > 1.3:
                    add_error(f_id, 'asset_allocation_records', _records['datetime'], 'other')
                    bad_fund = True
                if _records['net_asset'] > 48758492574:
                    add_error(f_id, 'asset_allocation_records', _records['datetime'], 'net_asset')
                    bad_fund = True
                if _records['total_asset'] > 49239793398:
                    add_error(f_id, 'asset_allocation_records', _records['datetime'], 'total_asset')
                    bad_fund = True
        if key == 'indicators_records':
            for _records in value:
                if np.isnan(_records['average_size']):
                    add_error(f_id, 'indicators_records', _records['datetime'], 'average_size')
                    bad_fund = True
                if _records['annualized_returns'] > 16872648:
                    add_error(f_id, 'indicators_records', _records['datetime'], 'annualized_returns')
                    bad_fund = True
                if _records['last_three_month_return'] > 48.10:
                    add_error(f_id, 'indicators_records', _records['datetime'], 'last_three_month_return')
                    bad_fund = True
                if _records['total_return'] > 28:
                    add_error(f_id, 'indicators_records', _records['datetime'], 'total_return')
                    bad_fund = True
                if _records['to_date_return'] > 28:
                    add_error(f_id, 'indicators_records', _records['datetime'], 'to_date_return')
                    bad_fund = True
                if _records['total_alpha'] < -103 or _records['total_alpha'] > 365:
                    add_error(f_id, 'indicators_records', _records['datetime'], 'total_alpha')
                    bad_fund = True
                if _records['total_beta'] < -110 or _records['total_beta'] > 27:
                    add_error(f_id, 'indicators_records', _records['datetime'], 'total_beta')
                    bad_fund = True
                if _records['information_ratio'] < -7134 or _records['information_ratio'] > 6696:
                    add_error(f_id, 'indicators_records', _records['datetime'], 'information_ratio')
                    bad_fund = True
        if key == 'holding_records':
            for _records in value:
                for _holding in _records['holdings_list']:
                    if np.isnan(_holding['weight']):
                        add_error(f_id, 'holding_records', _records['datetime'], _holding['order_book_id'] + ':weight')
                        bad_fund = True
                    if np.isnan(_holding['shares']) or _holding['shares'] > 40404445:
                        add_error(f_id, 'holding_records', _records['datetime'], _holding['order_book_id'] + ':shares')
                        bad_fund = True
                    if np.isnan(_holding['market_value']) or _holding['shares'] > 7129867722:
                        add_error(f_id, 'holding_records', _records['datetime'],
                                  _holding['order_book_id'] + ':market_value')
                        bad_fund = True
                    # if _holding['category'] != 'AShare':
                    #     add_error(f_id, 'holding_records', _records['datetime'],
                    #               _holding['order_book_id'] + ':category')
                    #     bad_fund = True
    if not bad_fund:
        good_fund.append(fund)
print('good_fund:{}, error_fund:{}, use_fund:{:.2f}%'.format(len(good_fund), len(error_fund_detail.keys()),
                                                             len(good_fund) * 100 / len(fund_data)))
# max([_return for _return in holding_records_args['holding_list']['weight'] if not pd.isnull(_return)])
# with open(ProjectPath + '/data/error_funds_detail.json', 'w') as wp:
#     json.dump(error_fund_detail, wp)
with open(ProjectPath + '/data/good_funds.json', 'w') as wp:
    json.dump(good_fund, wp)

print('over')
