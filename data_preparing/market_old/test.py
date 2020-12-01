import json
import pandas as pd
import matplotlib.pyplot as plt

# with open('/home/kuoluo/projects/FundAnalysis/data/fund_datetime_latest.json', 'r',errors='ignore') as fp:
#     data = json.load(fp)
#
# print(data['20191001'])

# with open('/home/kuoluo/projects/FundAnalysis/data/fund_datetime.json', 'r', encoding='utf-8') as f:
#     objects = ijson.items(f, 'earth.europe.item')
#     #这个objects在这里就是相当于一个生成器，可以调用next函数取它的下一个值
#     while True:
#         try:
#             print(objects.__next__())
#         except StopIteration as e:
#             print("数据读取完成")
#             break
SavePath = '/home/kuoluo/projects/FundAnalysis/images/'

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
# plt.plot(list(res1.index), list(res1.values))
# plt.savefig(SavePath+'fund_datetime_byNum')
# plt.show()

# 画图（基金规模）
plt.plot(list(res2.index), list(res2.values))
plt.title('2015年-2020年基金规模时序图（按月聚合）')
plt.xlabel('时间')
plt.ylabel('规模（单位：万元）')
plt.savefig(SavePath+'fund_datetime_bySize')
plt.show()

# 画图（基金类型）



