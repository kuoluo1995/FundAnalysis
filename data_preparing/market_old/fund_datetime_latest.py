import pandas as pd
import numpy as np
from datetime import datetime
import json

ProjectPath = '/home/kuoluo/projects/FundAnalysis'
with open(ProjectPath+'/data/good_funds_a.json', 'r') as fp:
    fund_data = json.load(fp)

fund_datetime = {}
for fund in fund_data:
    f_id = fund['fund_id']
    for record in fund['indicators_records']:
        datetime = record['datetime']
        if int(datetime[0:4]) < 2020:
            continue
        if datetime not in fund_datetime:
            fund_datetime[datetime] = {'funds': {}}
        if f_id not in fund_datetime[datetime]['funds']:
            fund_datetime[datetime]['funds'][f_id] = []
            fund_record = {'transition_time': fund['transition_time'], 'fund_manager': fund['fund_manager'], 'listed_date':
                            fund['listed_date'], 'de_listed_date': fund['de_listed_date'], 'latest_size': fund['latest_size'],
                           'fund_type': fund['fund_type'], 'amc': fund['amc'], 'exchange': fund['exchange'],
                           'manager_records': fund['manager_records'],  'asset_allocation_records': fund['asset_allocation_records'],
                           'holding_records': fund['holding_records'], 'indicators_records': fund['indicators_records']}
            fund_datetime[datetime]['funds'][f_id].append(fund_record)

with open(ProjectPath + '/data/fund_datetime_latest.json', 'w') as wp:
    json.dump(fund_datetime, wp)

print('over')



