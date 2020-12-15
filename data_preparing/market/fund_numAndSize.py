import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 整理近15年的数据,以基金上市时间为基准
ProjectPath = '/home/kuoluo/projects/FundAnalysis'
with open(ProjectPath+'/data/good_funds_a.json', 'r') as fp:
    fund_data = json.load(fp)

fund_market_one = {'fund_id': [], 'latest_size': [], 'fund_type': [], 'fund_num': []}
index_datetime = []
for record in fund_data:
    datetime = record['listed_date']
    if int(datetime[0:4]) < 2005:
        continue
    index_datetime.append(record['listed_date'])
    fund_market_one['fund_id'].append(record['fund_id'])
    fund_market_one['latest_size'].append(round(record['latest_size']/100000000, 2))
    fund_market_one['fund_type'].append(record['fund_type'])
    fund_market_one['fund_num'].append(1)
frame = pd.DataFrame(fund_market_one, index=pd.to_datetime(index_datetime))

# 按月统计
month_frame = frame.resample('M').sum()
x_date_month = []  # 200101-202002
y_size_month = [0]*182
y_num_month = [0]*182
cur_index = 0
for index, row in month_frame.iterrows():
    every_size = round(row.latest_size, 2)
    every_num = int(row.fund_num)
    x_date_month.append(index.strftime("%Y-%m-%d"))
    for i, val in enumerate(y_size_month, cur_index):
        if i >= 182:
            break
        y_size_month[i] += every_size
    for i, val in enumerate(y_num_month, cur_index):
        if i >= 182:
            break
        y_num_month[i] += every_num
    cur_index = cur_index + 1

fund_numAndSize = {'date_month': x_date_month, 'size_month': np.round(y_size_month, 2), 'num_month': y_num_month}

# annual_frame = frame.resample('A-DEC').mean()



# with open('/home/hezijing/project/data/fund_market_one.json', 'w') as wp:
#     json.dump(fund_numAndSize, wp)
print(fund_numAndSize['date_month'][120:])
print(fund_numAndSize['size_month'][120:])
print(fund_numAndSize['num_month'][120:])


print('over')




