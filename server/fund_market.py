from server import common, fund_data
import numpy as np
import sys


def get_market_nav_distribution():
    nav_distribution_byMonth = {}
    res = {}
    for record in common.fund_data:
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
                common.nav_distribution(values, k, month, nav_distribution_byMonth)
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


def get_market_monthly_return_distribution():
	fund_ids = common.fund_data_dict.keys()
	unit_net_value = fund_data.get_fund_dict(fund_ids, 'unit_net_value')
	monthly_return_distribution = {}
	for fund_id, unit_net_values in unit_net_value.items():
		fund_nav = {}
		for date, unit_net_value in unit_net_values.items():
			year = date[0:4]
			if year not in fund_nav:
				fund_nav[year] = {}
			month = date[0:6]
			if month not in fund_nav[year]:
				fund_nav[year][month] = 0
				first_unit_net_value = unit_net_value
			fund_nav[year][month] = (unit_net_value/first_unit_net_value - 1) * 100
		for year, value in fund_nav.items():
			if year not in monthly_return_distribution:
				monthly_return_distribution[year] = {}
			for month, return_value in value.items():
				if month not in monthly_return_distribution[year]:
					monthly_return_distribution[year][month] = {'%d~%d' % (-20 + 2 * x, -20 + 2 * (x + 1)): 0 for x in range(20)}
				for interval in monthly_return_distribution[year][month]:
					start, end = tuple(interval.split('~'))
					if float(start) <= return_value <= float(end):
						monthly_return_distribution[year][month][interval] += 1
						break
			monthly_return_distribution[year] = common.sortByKey(monthly_return_distribution[year])
	monthly_return_distribution = common.sortByKey(monthly_return_distribution)
	pre_year = None
	for _year, _value in monthly_return_distribution.items():
		if int(_year)<2000:
			pre_year=_year
			continue
		monthly_return_distribution[pre_year][pre_year+'13'] = monthly_return_distribution[_year][_year+'01']
		pre_year=_year
	return monthly_return_distribution


def get_market_monthly_avg_return():
	fund_ids = common.fund_data_dict.keys()
	unit_net_value = fund_data.get_fund_dict(fund_ids, 'unit_net_value')
	monthly_avg_return = {}
	for fund_id, unit_net_values in unit_net_value.items():
		fund_nav = {}
		for date, unit_net_value in unit_net_values.items():
			year = date[0:4]
			if year not in fund_nav:
				fund_nav[year] = {}
			month = date[0:6]
			if month not in fund_nav[year]:
				fund_nav[year][month] = 0
				first_unit_net_value = unit_net_value
			fund_nav[year][month] = (unit_net_value/first_unit_net_value - 1) * 100
		for year, value in fund_nav.items():
			if year not in monthly_avg_return:
				monthly_avg_return[year] = {}
			for month, return_value in value.items():
				if month not in monthly_avg_return[year]:
					monthly_avg_return[year][month] = []
				monthly_avg_return[year][month].append(return_value)
			monthly_avg_return[year] = common.sortByKey(monthly_avg_return[year])
	monthly_avg_return = common.sortByKey(monthly_avg_return)
	for _year, _values in monthly_avg_return.items():
		for _month, _return_values in monthly_avg_return[_year].items():
			monthly_avg_return[_year][_month] = round(np.mean(_return_values), 2)
	return monthly_avg_return


if __name__ == '__main__':
	# nav_distribution_value = get_market_nav_distribution()
	# sector_date_value = get_market_sector_value()
	# market_monthly_return_distribution_value = get_market_monthly_return_distribution()
	market_monthly_avg_return_value = get_market_monthly_avg_return()

	print('over')
