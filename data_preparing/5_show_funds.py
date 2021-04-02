import os
import sys
import json

sys.path.append('/home/kuoluo/projects/FundAnalysis/')
from tools.show_tool import bar_chart

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'

fund_files = os.listdir(project_path + '/data/view_funds2')

size_list = list()
alpha = list()
beta = list()
sharp_ratio = list()
information_ratio = list()
risk = list()
one_quarter_return_list = list()
one_quarter_hs300_return_list = list()
one_year_return_list = list()
one_year_hs300_return_list = list()
three_year_return_list = list()
three_year_hs300_return_list = list()
for file in fund_files:
    with open(project_path + '/data/view_funds2/' + file, 'r', encoding='UTF-8') as rp:
        view_fund = json.load(rp)
    for _date, _value in view_fund.items():
        size_list.append(_value['size'])
        alpha.append(_value['alpha'])
        beta.append(_value['beta'])
        sharp_ratio.append(_value['sharp_ratio'])
        information_ratio.append(_value['information_ratio'])
        risk.append(_value['risk'])
        one_quarter_return_list.append(_value['one_quarter_return'])
        one_quarter_hs300_return_list.append(_value['one_quarter_hs300_return'])
        if 'one_year_return' in _value:
            one_year_return_list.append(_value['one_year_return'])
            one_year_hs300_return_list.append(_value['one_year_hs300_return'])
        if 'three_year_return' in _value:
            three_year_return_list.append(_value['three_year_return'])
            three_year_hs300_return_list.append(_value['three_year_hs300_return'])
bar_chart(size_list, 'size', need_zero=False, num_gap=100)
print('size: min:{} max:{}'.format(min(size_list), max(size_list)))
bar_chart(alpha, 'alpha', need_zero=False, gap=0.1)
print('alpha: min:{} max:{}'.format(min(alpha), max(alpha)))
bar_chart(beta, 'beta', need_zero=False, gap=0.1)
print('beta: min:{} max:{}'.format(min(beta), max(beta)))
bar_chart(sharp_ratio, 'sharp_ratio', need_zero=False, gap=0.5)
print('sharp_ratio: min:{} max:{}'.format(min(sharp_ratio), max(sharp_ratio)))
bar_chart(information_ratio, 'information_ratio', need_zero=False, gap=0.1)
print('information_ratio: min:{} max:{}'.format(min(information_ratio), max(information_ratio)))
bar_chart(risk, 'risk', need_zero=False, gap=0.1)
print('risk: min:{} max:{}'.format(min(risk), max(risk)))
bar_chart(one_quarter_return_list, 'one_quarter_return_list', need_zero=False, gap=0.1)
print('one_quarter_return_list: min:{} max:{}'.format(min(one_quarter_return_list), max(one_quarter_return_list)))
bar_chart(one_quarter_hs300_return_list, 'one_quarter_hs300_return_list', need_zero=False, gap=0.1)
print('one_quarter_hs300_return_list: min:{} max:{}'.format(min(one_quarter_hs300_return_list),
                                                            max(one_quarter_hs300_return_list)))
bar_chart(one_year_return_list, 'one_year_return_list', need_zero=False, gap=0.1)
print('one_year_return_list: min:{} max:{}'.format(min(one_year_return_list), max(one_year_return_list)))
bar_chart(one_year_hs300_return_list, 'one_year_hs300_return_list', need_zero=False, gap=0.1)
print('one_year_hs300_return_list: min:{} max:{}'.format(min(one_year_hs300_return_list),
                                                         max(one_year_hs300_return_list)))
bar_chart(three_year_return_list, 'three_year_return_list', need_zero=False, gap=0.1)
print('three_year_return_list: min:{} max:{}'.format(min(three_year_return_list), max(three_year_return_list)))
bar_chart(three_year_hs300_return_list, 'three_year_hs300_return_list', need_zero=False, gap=0.1)
print('three_year_hs300_return_list: min:{} max:{}'.format(min(three_year_hs300_return_list),
                                                           max(three_year_hs300_return_list)))
