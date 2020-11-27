import json
import os
import time

funds = []

DATAPath = '/home/kuoluo/data/fund'
fund_files = os.listdir(DATAPath + '/full_fund_data')
fund_files = set(fund_files)
for z, _file in enumerate(fund_files):
    with open(DATAPath + '/full_fund_data/' + _file, 'r') as fp:
        json_data = json.load(fp)
    json_data.pop('benchmark')
    start_date = None
    end_date = None
    for indicator in json_data['indicators_records']:
        if start_date is None or start_date > int(indicator['datetime']):
            start_date = int(indicator['datetime'])
        if end_date is None or end_date < int(indicator['datetime']):
            end_date = int(indicator['datetime'])
    json_data['manager_records'] = json_data['manager_records']['data'] if 'data' in json_data['manager_records'] else \
        json_data['manager_records']
    for manager_record in json_data['manager_records']:
        manager_record['start_date'] = manager_record['start_date'][:10].replace('-', '')
        if manager_record['end_date'] is None:
            manager_record['end_date'] = '00000000'
        else:
            manager_record['end_date'] = manager_record['end_date'][:10].replace('-', '')
    for i, asset in enumerate(json_data['asset_allocation_records']):
        json_data['asset_allocation_records'][i].pop('nav')
    json_data['nav'] = json_data['nav']['data']
    temp_list = []
    for i, _t in enumerate(json_data['nav']):
        json_data['nav'][i].pop('order_book_id')
        json_data['nav'][i]['datetime'] = json_data['nav'][i]['datetime'][:10].replace('-', '')
        if int(json_data['nav'][i]['datetime']) <= end_date:
            temp_list.append(json_data['nav'][i])
    json_data['nav'] = temp_list
    json_data.pop('bond_records')
    # json_data['bond_records'] = json_data['bond_records']['data'] if 'data' in json_data['bond_records'] else json_data['bond_records']
    # for i, asset in enumerate(json_data['bond_records']):
    #     json_data['bond_records'][i].pop('order_book_id')
    json_data['industry_allocation'] = json_data['industry_allocation']['data'] if 'data' in json_data[
        'industry_allocation'] else json_data['industry_allocation']
    temp_dict = {}
    for i, industry_allocation in enumerate(json_data['industry_allocation']):
        industry_allocation.pop('order_book_id')
        if industry_allocation['datetime'] not in temp_dict:
            temp_dict[industry_allocation['datetime']] = []
        temp_dict[industry_allocation['datetime']].append({**industry_allocation})
        temp_dict[industry_allocation['datetime']][-1].pop('datetime')
    temp_list = []
    for key, value in temp_dict.items():
        key = key[:10].replace('-', '')
        if int(key) <= end_date:
            temp_list.append({'datatime': key, 'industry_allocation': value})
    json_data.pop('industry_allocation')
    json_data['industry_allocation_records'] = temp_list
    temp_list = []
    json_data['rating'] = json_data['rating']['data'] if 'data' in json_data['rating'] else json_data['rating']
    for i, asset in enumerate(json_data['rating']):
        json_data['rating'][i].pop('order_book_id')
        json_data['rating'][i]['datetime'] = json_data['rating'][i]['datetime'][:10].replace('-', '')
        if int(json_data['rating'][i]['datetime']) <= end_date:
            temp_list.append(json_data['rating'][i])
    json_data['rating'] = temp_list
    json_data['holder_structure'] = json_data['holder_structure']['data'] if 'data' in json_data[
        'holder_structure'] else json_data['holder_structure']
    temp_list = []
    for i, asset in enumerate(json_data['holder_structure']):
        json_data['holder_structure'][i].pop('order_book_id')
        json_data['holder_structure'][i]['date'] = json_data['holder_structure'][i]['date'][:10].replace('-', '')
        if int(json_data['holder_structure'][i]['date']) <= end_date:
            temp_list.append(json_data['holder_structure'][i])
    json_data['holder_structure'] = temp_list
    json_data['instrument_category'] = json_data['instrument']['data'] if 'data' in json_data['instrument'] else \
        json_data['instrument']
    json_data.pop('instrument')
    for i, asset in enumerate(json_data['instrument_category']):
        json_data['instrument_category'][i].pop('order_book_id')
    for i, holding_records in enumerate(json_data['holding_records']):
        for j, holding in enumerate(holding_records['holdings_list']):
            if json_data['holding_records'][i]['holdings_list'][j]['datetime'] != \
                    json_data['holding_records'][i]['datetime']:
                print('error')
            json_data['holding_records'][i]['holdings_list'][j].pop('datetime')
            json_data['holding_records'][i]['holdings_list'][j].pop('type')
            # json_data['holding_records'][i]['holdings_list'][j].pop('symbol')
    funds.append(json_data)
    print('\rprocessing: {}/{} {:.2f}%'.format(z + 1, len(fund_files), (z + 1) / len(fund_files) * 100), end='')
print()
with open(DATAPath + '/fund_data.json', 'w') as wp:
    json.dump(funds, wp)
print('数据集保存成功')
