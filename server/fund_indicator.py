import calendar
import pandas as pd
import numpy as np
from server.common import Interval


def get_income(date_navs, start_date, end_date=None, interval=Interval.Daily, need_first_nav=False):
    first_nav = None
    income_dict = {}
    for date_nav in date_navs:
        if int(start_date) <= int(date_nav['datetime']) and (
                end_date is None or int(date_nav['datetime']) <= int(end_date)):
            if first_nav is None:
                first_nav = date_nav['unit_net_value']
                datetime = Interval.format_date(interval, date_nav['datetime'])
                if datetime not in income_dict:
                    income_dict[datetime] = 0
                income_dict[datetime] += (date_nav['unit_net_value'] / first_nav - 1) * 100
    if need_first_nav:
        return income_dict, first_nav
    return income_dict


def get_return(date_navs, start_date, end_date=None, interval=Interval.Daily):
    # 累积收益率
    date_incomes, first_nav = get_income(date_navs, start_date, end_date, interval, need_first_nav=True)
    pre_date = None
    for _date, _income in date_incomes.items():
        if pre_date is None:
            pre_date = _date
            continue
        date_incomes[_date] += date_incomes[pre_date]
    for _date, _income in date_incomes.items():
        date_incomes[_date] /= first_nav
    return date_incomes

def get_sharpe_ratio():
    year_list = []
    month_list = []
    rtn_list = []
    for year in range(2006, 2017):
        for month in [6, 12]:
            year_list.append(year)
            month_list.append(month)
            rtn = round((-1) ** (month / 6) * (month / 6 / 10), 3) + (np.random.random() - 0.5) * 0.1
            rtn_list.append(rtn)
    # 生成半年为周期的收益率df
    df = pd.DataFrame()
    df['year'] = year_list
    df['month'] = month_list
    df['rtn'] = rtn_list
    df_year = df.groupby(['year']).sum()
    del df_year['month']
    round(df_year['rtn'].mean() / df_year['rtn'].std(), 3)
    #由于我们要计算的是年化的值，所以收益率要乘以2，波动率要乘以[公式]（一年是半年的2倍）。
    # 生成每年的收益数据df_year（对数收益率可以直接相加）
    df_year = df.groupby(['year']).sum()
    del df_year['month']
    round(df_year['rtn'].mean() / df_year['rtn'].std(), 3)


if __name__ == '__main__':
    pass
