import json

ProjectPath = '/home/kuoluo/projects/FundAnalysis'
with open(ProjectPath + '/data/good_funds_a.json', 'r') as fp:
    fund_data = json.load(fp)

fund_manager = {}

# 检查一级列表的数据
for fund in fund_data:
    bad_fund = False
    f_id = fund['fund_id']
    for records in fund['manager_records']:
        m_id = records['manager_id']
        if m_id not in fund_manager:
            fund_manager[m_id] = {'name': records['name'], 'funds': {}}
        if f_id not in fund_manager[m_id]['funds']:
            fund_manager[m_id]['funds'][f_id] = []
        fund_record = {'amc': fund['amc'], 'exchange': fund['exchange'], 'fund_type': fund['fund_type'],
                       'days': records['days'], 'start_date': records['start_date'], 'end_date': records['end_date'],
                       'return': records['return'], 'asset_allocation_records': [], 'holding_records': {},
                       'indicators_records': []}
        for asset in fund['asset_allocation_records']:
            if int(asset['datetime']) < int(records['start_date']):  # 之前的日期不算
                continue
            if int(records['end_date']) != 0 or int(records['end_date']) < int(asset['datetime']):
                continue
            fund_record['asset_allocation_records'].append(asset)
        for indicators in fund['indicators_records']:
            if int(indicators['datetime']) < int(records['start_date']):  # 之前的日期不算
                continue
            if int(records['end_date']) != 0 or int(records['end_date']) < int(indicators['datetime']):
                continue
            fund_record['indicators_records'].append(indicators)
        for holding_dict in fund['holding_records']:
            if int(holding_dict['datetime']) < int(records['start_date']):
                continue
            if int(records['end_date']) != 0 or int(records['end_date']) < int(holding_dict['datetime']):
                continue
            if holding_dict['datetime'] in fund_record['holding_records']:
                print('error')
            fund_record['holding_records'][holding_dict['datetime']] = holding_dict['holdings_list']
        fund_manager[m_id]['funds'][f_id].append(fund_record)

with open(ProjectPath + '/data/fund_manager.json', 'w') as wp:
    json.dump(fund_manager, wp)

print('over')
