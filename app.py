import json
from flask import Flask, request
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
    m_ids = request.get_json()['m_ids']
    m_datetime, start_date, end_date = fund_manager.get_manager_times(m_ids)
    return {'start_date': start_date, 'end_date': end_date}


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
    m_ids = request.get_json()['m_ids']
    manager_asset = fund_manager.get_manager_asset(m_ids)
    return manager_asset


@app.route('/get_manager_asset_value', methods=['POST'])
def get_manager_asset_value():
    m_ids = request.get_json()['m_ids']
    manager_asset = fund_manager.get_manager_asset(m_ids)
    return manager_asset


@app.route('/get_manager_sector', methods=['POST'])
def get_manager_sector():
    m_ids = request.get_json()['m_ids']
    manager_date_sector_dict = fund_manager.get_manager_date_sector(m_ids)
    return manager_date_sector_dict


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


@app.route('/get_fund_nav', methods=['POST'])
def get_fund_nav():
    f_id = request.get_json()['f_ids']
    fund_date_nav = fund_data.get_fund_dict(f_id, 'unit_net_value')
    return fund_date_nav


if __name__ == '__main__':
    app.run(host='10.76.0.165', port='5001')
