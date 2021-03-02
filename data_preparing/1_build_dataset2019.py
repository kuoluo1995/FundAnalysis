import json
import os

funds = []

DATAPath = '/home/kuoluo/data/fund'
with open('/home/kuoluo/projects/FundAnalysis/data/stock_concept_sector.json', 'r', encoding='UTF-8') as rp:
    stock_concept_sector = json.load(rp)
stock_sector = {}
for stock_index, value in stock_concept_sector.items():
    stock_sector[stock_index[:6]] = value['sector']

fund_files = os.listdir(DATAPath + '/full_fund_data')
fund_files = set(fund_files)
for z, _file in enumerate(fund_files):
    with open(DATAPath + '/full_fund_data/' + _file, 'r') as fp:
        json_data = json.load(fp)
    start_date = 19190101
    end_date = 20191231
    if 1 < int(json_data['de_listed_date']) < start_date:
        continue

    json_data['manager_records'] = json_data['manager_records']['data'] if 'data' in json_data['manager_records'] else \
        json_data['manager_records']
    for manager_record in json_data['manager_records']:
        manager_record['start_date'] = manager_record['start_date'][:10].replace('-', '')
        if manager_record['end_date'] is None:
            manager_record['end_date'] = '00000000'
        else:
            manager_record['end_date'] = manager_record['end_date'][:10].replace('-', '')

    temp_list = []
    for i, asset in enumerate(json_data['asset_allocation_records']):
        if start_date <= int(json_data['asset_allocation_records'][i]['datetime']) <= end_date:
            json_data['asset_allocation_records'][i].pop('nav')
            temp_list.append(json_data['asset_allocation_records'][i])
    json_data['asset_allocation_records'] = temp_list

    json_data['nav'] = json_data['nav']['data']
    temp_list = []
    for i, _ in enumerate(json_data['nav']):
        json_data['nav'][i].pop('order_book_id')
        json_data['nav'][i]['datetime'] = json_data['nav'][i]['datetime'][:10].replace('-', '')
        if start_date <= int(json_data['nav'][i]['datetime']) <= end_date:
            temp_list.append(json_data['nav'][i])
    json_data['nav'] = temp_list

    json_data.pop('bond_records')

    json_data['rating'] = json_data['rating']['data'] if 'data' in json_data['rating'] else json_data['rating']
    temp_list = []
    for i, _ in enumerate(json_data['rating']):
        json_data['rating'][i].pop('order_book_id')
        json_data['rating'][i]['datetime'] = json_data['rating'][i]['datetime'][:10].replace('-', '')
        if start_date <= int(json_data['rating'][i]['datetime']) <= end_date:
            temp_list.append(json_data['rating'][i])
    json_data['rating'] = temp_list

    json_data['holder_structure'] = json_data['holder_structure']['data'] if 'data' in json_data[
        'holder_structure'] else json_data['holder_structure']
    temp_list = []
    for i, asset in enumerate(json_data['holder_structure']):
        json_data['holder_structure'][i].pop('order_book_id')
        json_data['holder_structure'][i]['date'] = json_data['holder_structure'][i]['date'][:10].replace('-', '')
        if start_date <= int(json_data['holder_structure'][i]['date']) <= end_date:
            temp_list.append(json_data['holder_structure'][i])
    json_data['holder_structure'] = temp_list

    json_data['instrument_category'] = json_data['instrument']['data'] if 'data' in json_data['instrument'] else \
        json_data['instrument']
    json_data.pop('instrument')
    for i, asset in enumerate(json_data['instrument_category']):
        json_data['instrument_category'][i].pop('order_book_id')

    json_data.pop('industry_allocation')

    temp_list = []
    for i, asset in enumerate(json_data['indicators_records']):
        if start_date <= int(json_data['indicators_records'][i]['datetime']) <= end_date:
            temp_list.append(json_data['indicators_records'][i])
    json_data['indicators_records'] = temp_list

    temp_list = []
    for i, holding_records in enumerate(json_data['holding_records']):
        if start_date <= int(holding_records['datetime']) <= end_date:
            for j, holding in enumerate(holding_records['holdings_list']):
                json_data['holding_records'][i]['holdings_list'][j].pop('datetime')
                json_data['holding_records'][i]['holdings_list'][j].pop('type')
                json_data['holding_records'][i]['holdings_list'][j]['sector'] = stock_sector[
                    holding['order_book_id'][:6]] if holding['order_book_id'][:6] in stock_sector else '未知'
            temp_list.append(json_data['holding_records'][i])
    json_data['holding_records'] = temp_list

    funds.append(json_data)
    print('\rprocessing: {}/{} {:.2f}%'.format(z + 1, len(fund_files), (z + 1) / len(fund_files) * 100), end='')
print()
with open(DATAPath + '/fund_data_end_2019.json', 'w') as wp:
    json.dump(funds, wp)
print('数据集保存成功')
