import json
import matplotlib.pyplot as plt
import sys
import numpy as np

plt.rcParams['font.sans-serif'] = ['Noto Serif CJK JP']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

sys.path.append('/home/kuoluo/projects/FundAnalysis/')

with open('/home/kuoluo/data/fund/index.json', 'r') as fp:
    index_data = json.load(fp)

for _name, _value in index_data.items():
    x_date = [i for i in _value.keys()]
    x_date.sort()
    _close = list()
    pre_close = None
    for x in x_date:
        if pre_close is None:
            pre_close = _value[x]['收盘价']
        _close.append(_value[x]['收盘价'] / pre_close - 1)
    plt.plot(x_date, _close, color='blue', linewidth=1.0, linestyle='-', label='close')
    plt.xticks(x_date, x_date, rotation=-90)
    plt.title(_name)
    ax = plt.gca()
    ax.spines['right'].set_color('none')  # right边框属性设置为none 不显示
    ax.spines['top'].set_color('none')  # top边框属性设置为none 不显示
    plt.show()
    print()
