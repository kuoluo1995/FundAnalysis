import json

from flask import Flask, url_for, redirect, render_template, request
from flask_cors import CORS
from server import fund_manager, fund_market, fund_data

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 支持跨域


@app.route('/')
def index():
    managers = fund_manager.get_manager_name()
    # managers = sorted(managers.items(), key=lambda d: d[1], reverse=True)
    return managers


@app.route('/get_manager_times', methods=['POST'])
def get_manager_times():
    m_ids = request.form['m_ids'].strip()
    if m_ids[0] == '[':
        m_ids = m_ids[1:]
    if m_ids[-1] == ']':
        m_ids = m_ids[0:-1]
    m_ids = m_ids.split(',')
    m_datetime, start_date, end_date = fund_manager.get_manager_times(m_ids)
    return render_template('test.html', message=json.dumps(m_datetime), start_date=start_date, end_date=end_date,
                           manager_ids=request.form['m_ids'].strip())


@app.route('/get_manager_nav', methods=['POST'])
def get_manager_nav():
    m_ids = request.get_json()['m_ids']
    manager_nav = fund_manager.get_manager_nav(m_ids)
    return manager_nav


@app.route('/get_manager_acc_net', methods=['POST'])
def get_manager_acc_net():
    m_ids = request.get_json()['m_ids']
    manager_nav = fund_manager.get_manager_acc_net(m_ids)
    return manager_nav


@app.route('/get_manager_asset', methods=['POST'])
def get_manager_asset():
    m_ids = request.form['m_ids'].strip()
    manager_asset = fund_manager.get_manager_asset(m_ids)
    return manager_asset


@app.route('/get_manager_asset_value', methods=['POST'])
def get_manager_asset_value():
    m_ids = request.get_json()['m_ids']
    manager_asset = fund_manager.get_manager_asset(m_ids)
    return manager_asset


@app.route('/get_manager_income', methods=['POST'])
def get_manager_income():
    m_ids = request.get_json()['m_ids']
    start_date = request.get_json()['start_date'][0]
    manager_income = fund_manager.get_manager_income(m_ids, start_date)
    return manager_income


@app.route('/get_manager_sector', methods=['POST'])
def get_manager_sector():
    m_ids = request.get_json()['m_ids']
    manager_sector_dict = fund_manager.get_manager_sector(m_ids)
    manager_sector = fund_manager.object_merge_fund(manager_sector_dict, merge_type='sum', sort_type='value')
    return manager_sector


@app.route('/get_market_nav_distribution', methods=['POST'])
def get_market_nav_distribution():
    # nav_distribution_value = fund_market.get_market_nav_distribution() 实时的读取
    with open('/home/kuoluo/projects/FundAnalysis/data/explore/nav_distribution_value.json', 'r') as fp:
        nav_distribution_value = json.load(fp)
    return nav_distribution_value


@app.route('/get_market_asset_distribution', methods=['POST'])
def get_market_asset_distribution():
    with open('/home/kuoluo/projects/FundAnalysis/data/explore/asset_distribution_byQuarter_value.json', 'r') as fp:
        asset_distribution_byQuarter_value = json.load(fp)
    return asset_distribution_byQuarter_value


@app.route('/get_market_sector', methods=['POST'])
def get_market_sector():
    with open('/home/kuoluo/projects/FundAnalysis/data/explore/sector_date_value.json', 'r') as fp:
        market_sector_value = json.load(fp)
    return market_sector_value


@app.route('/get_fund_sector', methods=['POST'])
def get_fund_sector():
    f_id = request.get_json()['f_ids']
    fund_date_sector = fund_data.get_fund_date_sector(f_id)
    return fund_date_sector


@app.route('/get_fund_income_rate', methods=['POST'])
def get_fund_income_rate():
    f_id = request.get_json()['f_ids']
    min_start_date, max_end_date = fund_data.get_fund_time_border(f_id)
    fund_date_income = fund_data.get_fund_date_income(f_id, min_start_date, max_end_date)
    return fund_date_income


if __name__ == '__main__':
    app.run(host='10.76.0.165', port='5000')