import json
import os

# ProjectPath = '/home/kuoluo/projects/FundAnalysis'
project_path = 'E:/Projects/PythonProjects/FundAnalysis'
fund_files = os.listdir(project_path + '/data/source')


def check_time(_attr, start_date, end_date, str_date):
    _list = list()
    for _v in _attr:
        if int(_v[str_date]) < int(start_date):  # 之前的日期不算
            continue
        if int(end_date) != 0 and int(end_date) < int(_v[str_date]):
            continue
        _list.append(_v)
    return _list


def build_fund_manager_dict(files):
    manager_dict = {}
    _len = len(files)
    for i, file in enumerate(files):
        with open(project_path + '/data/source/' + file, 'r', encoding='UTF-8') as fp:
            fund = json.load(fp)
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
            # fund_record['rating'] = check_time(fund['rating'], records['start_date'], records['end_date'], 'datetime')
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
        print('\rbuild manager: {}/{} {:.2f}%'.format(i + 1, _len, (i + 1) * 100 / _len), end='')
    return manager_dict


print('start save manager')
fund_manager = build_fund_manager_dict(fund_files)
i = 1
_len = len(fund_manager)
for m_id, funds in fund_manager.items():
    with open(project_path + '/data/managers/' + m_id + '.json', 'w') as wp:
        json.dump(funds, wp)
    print('\rsaving manager:{}/{} {:.2f}%'.format(i, _len, i * 100 / _len), end='', flush=True)
    i += 1
print()
print('over')
