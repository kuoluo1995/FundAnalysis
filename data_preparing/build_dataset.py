import json
import os

with open('data/error_funds.json', 'r') as fp:
    error_fund = json.load(fp)

DATAPath = '/home/kuoluo/data/fund_data'
good_funds = []
for _file in os.listdir(DATAPath):
    with open(DATAPath + '/' + _file, 'r') as fp:
        json_data = json.load(fp)
        if json_data[0]['fund_id'] not in error_fund:
            json_data[0].pop('_id')
            json_data[0].pop('benchmark')
            json_data[0].pop('symbol')
            json_data[0].pop('accrued_daily')
            json_data[0].pop('exchange')
            json_data[0].pop('round_lot')
            for i, asset in enumerate(json_data[0]['asset_allocation_records']):
                if json_data[0]['asset_allocation_records'][i]['nav'] != json_data[0]['asset_allocation_records'][i]['net_asset']:
                    print('error')
                json_data[0]['asset_allocation_records'][i].pop('nav')
            for i, holding_records in enumerate(json_data[0]['holding_records']):
                for j, holding in enumerate(holding_records['holdings_list']):
                    if json_data[0]['holding_records'][i]['holdings_list'][j]['datetime']!= json_data[0]['holding_records'][i]['datetime']:
                        print('error')
                    json_data[0]['holding_records'][i]['holdings_list'][j].pop('datetime')
                    json_data[0]['holding_records'][i]['holdings_list'][j].pop('type')
                    json_data[0]['holding_records'][i]['holdings_list'][j].pop('symbol')
            good_funds.append(json_data[0])
with open('data/good_funds.json', 'w') as wp:
    json.dump(good_funds, wp)

