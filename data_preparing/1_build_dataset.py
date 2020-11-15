import json
import os

# with open('../data/error_funds.json', 'r') as fp:
#     error_fund = json.load(fp)

DATAPath = '/home/kuoluo/data/fund_data'
funds = []
fund_files = os.listdir(DATAPath)
print('开始生成数据集')
for z, _file in enumerate(fund_files):
    with open(DATAPath + '/' + _file, 'r') as fp:
        json_data = json.load(fp)
        json_data[0].pop('_id')
        json_data[0].pop('symbol')
        json_data[0].pop('establishment_date')
        json_data[0].pop('stop_date')
        json_data[0].pop('benchmark')
        json_data[0].pop('accrued_daily')
        json_data[0].pop('round_lot')
        for i, asset in enumerate(json_data[0]['asset_allocation_records']):
            if json_data[0]['asset_allocation_records'][i]['nav'] != json_data[0]['asset_allocation_records'][i][
                'net_asset']:
                print('error')
            json_data[0]['asset_allocation_records'][i].pop('nav')
        for i, holding_records in enumerate(json_data[0]['holding_records']):
            for j, holding in enumerate(holding_records['holdings_list']):
                if json_data[0]['holding_records'][i]['holdings_list'][j]['datetime'] != \
                        json_data[0]['holding_records'][i]['datetime']:
                    print('error')
                json_data[0]['holding_records'][i]['holdings_list'][j].pop('datetime')
                json_data[0]['holding_records'][i]['holdings_list'][j].pop('type')
                json_data[0]['holding_records'][i]['holdings_list'][j].pop('symbol')
        funds.append(json_data[0])
    print('\rprocessing: {}/{} {:.2f}%'.format(z + 1, len(fund_files), (z + 1) / len(fund_files) * 100), end='')
print()
with open('/home/kuoluo/data/fund_data.json', 'w') as wp:
    json.dump(funds, wp)
print('数据集保存成功')
