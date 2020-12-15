# 在 fund_datetime_byNumAndSize 数据集的基础上进一步处理基金类型
from pandas import Series,DataFrame
import json
import pandas as pd
import matplotlib.pyplot as plt

SavePath = '/home/kuoluo/projects/FundAnalysis/images/'

with open('/home/kuoluo/projects/FundAnalysis/data/fund_datetime_byNumAndSize.json', 'r') as fp:
    fund_datetime = json.load(fp)

# 数据预处理，整合成DataFrame
index_datetime = pd.to_datetime(list(fund_datetime.keys()))

type_num_day ={'StockIndex': [], 'Hybrid': [], 'Stock': []}
for record in fund_datetime:
    StockIndex, Hybrid, Stock = 0, 0, 0
    for fund_id in fund_datetime[record]['funds']:
        if fund_datetime[record]['funds'][fund_id][0]['fund_type'] == 'StockIndex':
            StockIndex += 1
        elif fund_datetime[record]['funds'][fund_id][0]['fund_type'] == 'Hybrid':
            Hybrid += 1
        elif fund_datetime[record]['funds'][fund_id][0]['fund_type'] == 'Stock':
            Stock += 1
    type_num_day['StockIndex'].append(StockIndex)
    type_num_day['Hybrid'].append(Hybrid)
    type_num_day['Stock'].append(Stock)
frame = pd.DataFrame(type_num_day, index=index_datetime)

# 按3个月聚合
frame = frame.resample('3M').sum()

# 画图
df = DataFrame(frame, columns=['StockIndex', 'Hybrid', 'Stock'])
df.plot(kind='bar', stacked=True, alpha=0.5)
plt.title('2015-2020 by fund_type（every three months）')
plt.xlabel('time')
plt.ylabel('number')
plt.tight_layout()
plt.savefig(SavePath+'fund_datetime_byType')
plt.show()



