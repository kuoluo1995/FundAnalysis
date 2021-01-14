import json

ProjectPath = '/home/kuoluo/projects/FundAnalysis'

fund_data_dict = {}
with open(ProjectPath + '/data/fund_date.json', 'r', encoding='UTF-8') as fp:
    fund_data = json.load(fp)
for fund in fund_data:
    fund_data_dict[fund['fund_id']] = {**fund}
with open(ProjectPath + '/data/fund_manager.json', 'r', encoding='UTF-8') as wp:
    fund_manager = json.load(wp)

with open(ProjectPath + '/data/stock_concept_sector.json', 'r', encoding='UTF-8') as rp:
    stock_concept_sector = json.load(rp)
stock_sector = {}
for stock_index, value in stock_concept_sector.items():
    stock_sector[stock_index[:6]] = value['sector']


def nav_distribution(total_list, year, month, nav_distribution_byMonth):
    countblock = 21
    intervals = {'%.1f~%.1f' % (0 + 0.2 * x, 0 + 0.2 * (x + 1)): 0 for x in range(countblock)}
    for ls in total_list:
        for interval in intervals:
            start, end = tuple(interval.split('~'))
            if float(start) <= ls <= float(end):
                intervals[interval] += 1
    for i in intervals:
        nav_distribution_byMonth[year][month][i] = intervals[i]


def monthly_return_distribution(value, year, month, result):
	countblock = 21
	intervals = {'%.1f~%.1f' % (-90 + 10 * x, -90 + 10 * (x + 1)): 0 for x in range(countblock)}
	for interval in intervals:
		start, end = tuple(interval.split('~'))
		if float(start) <= value <= float(end):
			intervals[interval] += 1
			break
	for i in intervals:
		result[year][month][i] = intervals[i]


def check_time(_attr, start_date, end_date, str_date):
    _list = list()
    for _v in _attr:
        if int(_v[str_date]) < int(start_date):  # 之前的日期不算
            continue
        if int(end_date) != 0 and int(end_date) < int(_v[str_date]):
            continue
        _list.append(_v)
    return _list


from enum import Enum


class Interval(Enum):
    Daily = 'daily'
    Week = 'week'
    Month = 'month'
    Year = 'year'
    Total = 'total'

    @staticmethod
    def format_date(_type, date):
        if _type == Interval.Daily:
            return date
        elif _type == Interval.Month:
            return date[:6]
        elif _type == Interval.Year:
            return date[:4]
        elif _type == Interval.Total:
            return 'total'
        else:
            print('interval enum:error')


def build_fund_manager_dict(fund_data):
    manager_dict = {}
    for fund in fund_data:
        f_id = fund['fund_id']
        for records in fund['manager_records']:
            m_id = records['id']
            if m_id not in manager_dict:
                manager_dict[m_id] = {'name': records['name'], 'funds': {}}
            if f_id not in manager_dict[m_id]['funds']:
                manager_dict[m_id]['funds'][f_id] = []
            fund_record = dict()
            fund_record['amc'] = fund['amc']
            fund_record['exchange'] = fund['exchange']
            fund_record['fund_type'] = fund['fund_type']
            fund_record['days'] = records['days']
            fund_record['start_date'] = records['start_date']
            fund_record['end_date'] = records['end_date']
            fund_record['asset_allocation_records'] = check_time(fund['asset_allocation_records'],
                                                                 records['start_date'], records['end_date'], 'datetime')
            fund_record['nav'] = check_time(fund['nav'], records['start_date'], records['end_date'], 'datetime')
            fund_record['rating'] = check_time(fund['rating'], records['start_date'], records['end_date'], 'datetime')
            fund_record['holder_structure'] = check_time(fund['holder_structure'], records['start_date'],
                                                         records['end_date'], 'date')
            fund_record['instrument_category'] = fund['instrument_category']
            fund_record['indicators_records'] = check_time(fund['indicators_records'], records['start_date'],
                                                           records['end_date'], 'datetime')
            fund_record['holding_records'] = {}
            for _v in fund['holding_records']:
                if int(records['start_date']) <= int(_v['datetime']):
                    if int(records['end_date']) == 0 or int(_v['datetime']) <= int(records['end_date']):
                        fund_record['holding_records'][_v['datetime']] = _v['holdings_list']
            manager_dict[m_id]['funds'][f_id].append(fund_record)
    return manager_dict


def sortByKey(v_dict):
    v_keys = list(v_dict.keys())
    v_keys.sort()
    return dict(zip(v_keys, [v_dict[key] for key in v_keys]))


if __name__ == '__main__':
    # fund_manager = build_fund_manager_dict(fund_data)
    # with open(ProjectPath + '/data/fund_manager.json', 'w') as wp:
    #     json.dump(fund_manager, wp)
    with open(ProjectPath + '/data/fund_data_dict.json', 'w') as wp:
        json.dump(fund_data_dict, wp)
    print('init')
