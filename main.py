import json
from flask import Flask, request
from flask_cors import CORS
from server import fund_manager, fund_market, fund_data, common
from tools.show_tool import normalize_dict_by_month

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 支持跨域
@app.route('/get_fund_ids', methods=['POST'])
def get_fund_ids():
    return common.fund_ids

@app.route('/get_market_overview', methods=['POST'])
def get_market_fund_size():
    market_fund_number = fund_market.get_market_fund_number_by_month()
    market_fund_return = fund_market.get_market_fund_income_by_month()
    market_fund_size = fund_market.get_market_fund_size_by_month()
    market_fund_size = normalize_dict_by_month(market_fund_size, market_fund_number.keys())
    overview = {'fund_number': dict(), 'fund_return': dict(), 'fund_size': dict()}
    for _date in market_fund_number.keys():
        overview['fund_number'][_date] = market_fund_number[_date]
        overview['fund_return'][_date] = market_fund_return[_date]
        overview['fund_size'][_date] = market_fund_size[_date]
    return overview


@app.route('/get_last_income_by_ids', methods=['POST'])
def get_last_income_by_ids():
    _json = request.get_json()
    if 'f_ids' in _json:
        f_ids = _json['f_ids']
    else:
        f_ids = common.fund_ids
    return fund_data.get_fund_last_income(f_ids)


@app.route('/get_last_size_by_ids', methods=['POST'])
def get_last_size_by_ids():
    _json = request.get_json()
    if 'f_ids' in _json:
        f_ids = _json['f_ids']
    else:
        f_ids = common.fund_ids
    return fund_data.get_fund_last_size(f_ids)


@app.route('/get_last_holder_by_ids', methods=['POST'])
def get_last_holder_by_ids():
    _json = request.get_json()
    if 'f_ids' in _json:
        f_ids = _json['f_ids']
    else:
        f_ids = common.fund_ids
    return fund_data.get_fund_last_holder(f_ids)


@app.route('/get_last_risk_by_ids', methods=['POST'])
def get_last_risk_by_ids():
    _json = request.get_json()
    if 'f_ids' in _json:
        f_ids = _json['f_ids']
    else:
        f_ids = common.fund_ids
    return fund_data.get_fund_last_sharp_ratio(f_ids)


@app.route('/get_last_max_drop_by_ids', methods=['POST'])
def get_last_max_drop_by_ids():
    _json = request.get_json()
    if 'f_ids' in _json:
        f_ids = _json['f_ids']
    else:
        f_ids = common.fund_ids
    return fund_data.get_fund_last_max_drop(f_ids)


@app.route('/get_fund_tsnes', methods=['POST'])
def get_fund_tsnes():
    _json = request.get_json()
    f_ids = _json['f_ids']
    return fund_data.get_fund_t_sne(f_ids)


if __name__ == '__main__':
    app.run(host='10.76.0.165', port='8888')
