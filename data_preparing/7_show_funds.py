import os
import sys
import json

sys.path.append('/home/kuoluo/projects/FundAnalysis/')
from tools.show_tool import bar_chart

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'

fund_files = os.listdir(project_path + '/data/view_funds')

return_3list = list()
risk = list()

sharp_ratio = list()
information_ratio = list()

alpha = list()
beta = list()

return_list = list()
hs300_return_list = list()
car_list = list()
size_list = list()

for file in fund_files:
    with open(project_path + '/data/fund_features/' + file, 'r', encoding='UTF-8') as rp:
        view_fund = json.load(rp)
    for _date, _value in view_fund.items():
        _value.pop('manager_ids')
        _value.pop('detail_unit_navs')
        keys = list(_value.keys())
        with open(project_path + '/data/dictionary/weight_key.json', 'w', encoding='UTF-8') as wp:
            json.dump(keys, wp)
        break
    break

for file in fund_files:
    with open(project_path + '/data/view_funds/' + file, 'r', encoding='UTF-8') as rp:
        view_fund = json.load(rp)
    for _date, _value in view_fund.items():
        return_3list.append(_value['nav_return'])
        risk.append(_value['risk'])
        sharp_ratio.append(_value['sharp_ratio'])
        information_ratio.append(_value['information_ratio'])
        alpha.append(_value['alpha'])
        beta.append(_value['beta'])
        size_list.append(_value['size'])
        pre_return = None
        pre_hs300_return = None
        for _d, _v in _value['detail_unit_navs'].items():
            if pre_return is None:
                pre_return = _v
                pre_hs300_return = _value['detail_hs300s'][_d]
            return_list.append(_v / pre_return - 1)
            hs300_return_list.append(_value['detail_hs300s'][_d] / pre_hs300_return - 1)
            car_list.append(return_list[-1] - hs300_return_list[-1])

bar_chart(return_3list, 'return_3month', need_zero=False, gap=0.1)
print('return_3month: min:{} max:{}'.format(min(return_3list), max(return_3list)))
bar_chart(risk, 'risk', need_zero=False, gap=0.1)
print('risk: min:{} max:{}'.format(min(risk), max(risk)))
bar_chart(sharp_ratio, 'sharp_ratio', need_zero=False, gap=0.5)
print('sharp_ratio: min:{} max:{}'.format(min(sharp_ratio), max(sharp_ratio)))
bar_chart(information_ratio, 'information_ratio', need_zero=False, gap=0.1)
print('information_ratio: min:{} max:{}'.format(min(information_ratio), max(information_ratio)))
bar_chart(alpha, 'alpha', need_zero=False, gap=0.1)
print('alpha: min:{} max:{}'.format(min(alpha), max(alpha)))
bar_chart(beta, 'beta', need_zero=False, gap=0.1)
print('beta: min:{} max:{}'.format(min(beta), max(beta)))
bar_chart(size_list, 'size', need_zero=False, num_gap=100)
print('size: min:{} max:{}'.format(min(size_list), max(size_list)))
# bar_chart(car_list, 'car_list', need_zero=False, gap=0.1)
print('car_list: min:{} max:{}'.format(min(car_list), max(car_list)))
# bar_chart(return_list, 'return_list', need_zero=False, gap=0.1)
print('return_list: min:{} max:{}'.format(min(return_list), max(return_list)))
# bar_chart(hs300_return_list, 'hs300_return', need_zero=False, gap=0.1)
print('hs300_return: min:{} max:{}'.format(min(hs300_return_list), max(hs300_return_list)))
