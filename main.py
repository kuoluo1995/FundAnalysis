import json
from flask import Flask, request
from flask_cors import CORS
from server import fund_manager, fund_data, common

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 支持跨域


@app.route('/get_fund_ids', methods=['POST'])
def get_fund_ids():
    return {'fund_ids': common.fund_ids}


@app.route('/get_fund_time_border', methods=['POST'])
def get_fund_time_border():
    _json = request.get_json()
    f_ids = _json['f_ids']
    start_date, end_date = fund_data.get_fund_time_border(f_ids)
    return {'start_date': start_date, 'end_date': end_date}


@app.route('/get_view_funds', methods=['POST'])
def get_view_funds():
    _json = request.get_json()
    f_ids = _json['f_ids']
    start_date = _json['start_date']
    end_date = _json['end_date']
    details, summary = fund_data.get_view_fund(f_ids, start_date, end_date)
    return {'detail': details, 'total': summary}


@app.route('/get_manager_fund_local', methods=['POST'])
def get_manager_fund_local():
    _json = request.get_json()
    m_ids = []
    for f_id in _json['f_ids']:
        m_ids += common.fund_manager_dict[f_id]
    f_ids = []
    for m_id in m_ids:
        f_ids += common.manager_fund_dict[m_id]
    f_ids = list(set(f_ids))
    managers = fund_manager.get_manager_feature(m_ids)
    funds = fund_data.get_fund_t_sne(f_ids)
    return {'funds': funds, 'managers': managers}


@app.route('/get_fund_ranks', methods=['POST'])
def get_fund_ranks():
    _json = request.get_json()
    weights = _json['weights']
    fund_ids = fund_data.get_fund_ranks(weights)
    return {'ranks': fund_data.get_fund_last_dict(fund_ids, list(weights.keys()))}


if __name__ == '__main__':
    app.run(host='10.76.0.165', port='8888')
