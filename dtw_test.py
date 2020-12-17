import numpy as np
import matplotlib.pyplot as plt

from models.dtw import dtw
from server import common
from server.fund_data import get_fund_time_border, get_fund_date_income

fund_ids = common.fund_data_dict.keys()
min_start_date, max_end_date = get_fund_time_border(fund_ids)
fund_date_income = get_fund_date_income(fund_ids, min_start_date, max_end_date)

source_id = '510310'
l2_norm = lambda x, y: (x - y) ** 2

x = np.array([_v for _date, _v in fund_date_income[source_id].items()]).reshape(-1, 1)
ranks = {}
i = 1
length = len(fund_date_income)
for f_id, _list in fund_date_income.items():
    print('进度:{:>4}/{:>4}'.format(i, length))
    if source_id != f_id:
        y = list()
        for _date, _v in _list.items():
            y.append(_v)
        y = np.array(y).reshape(-1, 1)
        dist, cost_matrix, acc_cost_matrix, path = dtw(x, y, dist=l2_norm)
        ranks[f_id] = dist
ranks = sorted(ranks.items(), key=lambda d: d[1])
for i in range(0, 5):
    series = list()
    print(ranks[i][0]+' '+ranks[i][1])
    for _date, _v in fund_date_income[ranks[i][0]]:
        series.append(_v)
    plt.plot(series, label=ranks[i][0])
plt.title('income_similarity')
plt.legend()
