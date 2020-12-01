import json
import pandas as pd
import matplotlib.pyplot as plt

# 整理近5年的数据
# ProjectPath = '/home/kuoluo/projects/FundAnalysis'
# with open(ProjectPath+'/data/good_funds_a.json', 'r') as fp:
#     fund_data = json.load(fp)
#
# fund_datetime = {}
# for fund in fund_data:
#     f_id = fund['fund_id']
#     for record in fund['indicators_records']:
#         datetime = record['datetime']
#         if int(datetime[0:4]) < 2015:
#             continue
#         if datetime not in fund_datetime:
#             fund_datetime[datetime] = {'funds': {}}
#         if f_id not in fund_datetime[datetime]['funds']:
#             fund_datetime[datetime]['funds'][f_id] = []
#         fund_record = {'fund_type': fund['fund_type'], 'latest_size': fund['latest_size'], 'average_size': record['average_size']}
#         fund_datetime[datetime]['funds'][f_id].append(fund_record)
#
# with open(ProjectPath + '/data/fund_datetime_byNumAndSize.json', 'w') as wp:
#     json.dump(fund_datetime, wp)
#
# print('over')


# 画图

SavePath2 = '/home/kuoluo/projects/FundAnalysis/images/'

with open('/home/kuoluo/projects/FundAnalysis/data/fund_datetime_byNumAndSize.json', 'r') as fp:
    fund_datetime = json.load(fp)
# 数据预处理
x_data = list(fund_datetime.keys())
y1_data = []  # 基金个数
y2_data = []  # 基金规模
for record in fund_datetime:
    count = len(fund_datetime[record]['funds'])
    y1_data.append(count)
    for fund_id in fund_datetime[record]['funds']:
        size_sum = 0.0
        size_single = round(fund_datetime[record]['funds'][fund_id][0]['average_size']/10000, 2)
        size_sum += size_single
    y2_data.append(size_sum)



# 构建datetime矩阵 方便聚合
x_data = pd.to_datetime(x_data)
res1 = pd.Series(y1_data, index=x_data)
res2 = pd.Series(y2_data, index=x_data)

# 按月聚合
res1 = res1.resample('M').sum()
res2 = res2.resample('M').sum()

# 画图（基金个数）
plt.plot(list(res1.index), list(res1.values))
plt.title('2015-2020 by fund_num(every month)')
plt.xlabel('time')
plt.ylabel('number')
plt.savefig(SavePath2+'fund_datetime_byNum')
plt.show()

# 画图（基金规模）
# plt.plot(list(res2.index), list(res2.values))
# plt.title('2015-2020 by fund_size(every month)')
# plt.xlabel('time')
# plt.ylabel('size(Unit of Measurement：*10^10 yuan)')
# plt.savefig(SavePath2+'fund_datetime_bySize')
# plt.show()

