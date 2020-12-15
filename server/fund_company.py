import sys

sys.path.append('/home/kuoluo/projects/FundAnalysis/')
from server import common


def get_all_date():
    all_date = set()
    for fund in common.fund_data:
        all_date.add(fund['listed_date'])
        if int(fund['de_listed_date']) != 0:
            all_date.add(fund['de_listed_date'])
    all_date = sorted(list(all_date), key=lambda d: int(d), reverse=False)
    return all_date


def get_company_date_fund(all_date):
    company_dict = {}
    for fund in common.fund_data:
        if fund['amc'] not in company_dict:
            company_dict[fund['amc']] = {date: [] for date in all_date}
        for date in all_date:
            if int(fund['listed_date']) <= int(date) and (
                    int(fund['de_listed_date']) == 0 or int(date) <= int(fund['de_listed_date'])):
                company_dict[fund['amc']][date].append(fund['fund_id'])
    return company_dict


def get_company_date_manager(all_date):
    company_dict = {}
    for fund in common.fund_data:
        if fund['amc'] not in company_dict:
            company_dict[fund['amc']] = {date: [] for date in all_date}
        for manager in fund['manager_records']:
            for date in all_date:
                if int(manager['start_date']) <= int(date) and (
                        int(manager['end_date']) == 0 or int(date) <= int(manager['end_date'])):
                    company_dict[fund['amc']][date].append(manager['id'])
    return company_dict


def get_company_date_asset():
    company_dict = {}
    for fund in common.fund_data:
        if fund['amc'] not in company_dict:
            company_dict[fund['amc']] = {}
        for record in fund['asset_allocation_records']:
            if record['datetime'] not in company_dict[fund['amc']]:
                company_dict[fund['amc']][record['datetime']] = 0
            company_dict[fund['amc']][record['datetime']] += record['net_asset']
    return company_dict


if __name__ == '__main__':
    all_date = get_all_date()
    company_date_fund = get_company_date_fund(all_date)
    company_date_manager = get_company_date_manager(all_date)
    company_date_asset = get_company_date_asset()
    print('over')
