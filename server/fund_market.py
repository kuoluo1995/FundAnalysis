from server import common
import numpy as np


def get_market_nav_distribution():
    nav_distribution_byMonth = {}
    res = {}
    for record in common.fund_data_values:
        for nav_data in record['nav']:
            key = nav_data['datetime'][0:6]
            fund_id = record['fund_id']
            if key not in res:
                res[key] = {}
            if fund_id not in res[key]:
                res[key][fund_id] = {'nav_values': [], 'nav_avg': 0}
            tmp = res.get(key).get(fund_id)['nav_values']
            tmp.append(nav_data['unit_net_value'])
            res.get(key).get(fund_id)['nav_avg'] = np.mean(tmp)
    # 二次处理 按月
    data = {}
    for k_date, v in res.items():
        year = k_date[0:4]
        if year not in data:
            data[year] = {}
        data[year][k_date] = []
        for k_id, value in v.items():
            data[year][k_date].append(value['nav_avg'])
    # 处理每一年的数据 聚合到范围中
    for k, v in data.items():
        if k not in nav_distribution_byMonth:
            nav_distribution_byMonth[k] = {}
        for month, values in data.get(k).items():
            if month not in nav_distribution_byMonth[k]:
                nav_distribution_byMonth[k][month] = {}
                common.distribution(values, k, month,nav_distribution_byMonth)
    return nav_distribution_byMonth


def get_market_sector_value():
    market_dict = {}
    for fund in common.fund_data:
        for _record in fund['holding_records']:
            for holding in _record['holdings_list']:
                if holding['order_book_id'][:6] in common.stock_sector:
                    _sector = common.stock_sector[holding['order_book_id'][:6]]
                else:
                    _sector = '未知'
                if _sector not in market_dict:
                    market_dict[_sector] = {}
                if _record['datetime'] not in market_dict[_sector]:
                    market_dict[_sector][_record['datetime']] = 0
                market_dict[_sector][_record['datetime']] += holding['market_value']
    for _sector, date_value in market_dict.items():
        date_value = sorted(date_value.items(), key=lambda d: int(d[0]), reverse=False)
        temp = dict()
        for _date, _value in date_value:
            temp[_date] = _value
        market_dict[_sector] = temp
    return market_dict


if __name__ == '__main__':
    nav_distribution_value = get_market_nav_distribution()
    sector_date_value = get_market_sector_value()
    print('over')

