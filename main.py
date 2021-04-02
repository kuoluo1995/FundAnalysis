from flask import Flask, request
from flask_cors import CORS
from server import fund_manager, fund_data, common
from tools import color_tool

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 支持跨域


@app.route('/get_fund_ids', methods=['POST'])
def get_fund_ids():
    return {'fund_ids': common.fund_ids}


@app.route('/get_fund_time_border', methods=['POST'])
def get_fund_time_border():
    _json = request.get_json()
    f_ids = _json['f_ids']
    start_date, end_date = fund_data.get_fund_min_time_border(f_ids)
    return {'start_date': start_date, 'end_date': end_date}


@app.route('/get_fund_ranks', methods=['POST'])
def get_fund_ranks():
    _json = request.get_json()
    weights = _json['weights']
    start_date = _json['start_date']
    end_date = _json['end_date']
    sectors = _json['sectors'] if 'sectors' in _json else None
    ranks, manager2fund = fund_data.get_fund_ranks(weights, start_date, end_date, sectors)
    return {'ranking': ranks, 'colors': {_name: color_tool.get_color_value(_name) for _name in weights.keys()},
            'manager2fund': manager2fund}


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
    weights = _json['weights']
    num_top = _json['num_top']
    start_date = _json['start_date']
    end_date = _json['end_date']
    exist_m_id, new_m_ids = fund_manager.get_manager_ranks(_json['f_ids'], weights, start_date, end_date, num_top)
    all_m_ids = list(set(new_m_ids + exist_m_id))
    managers = fund_manager.get_manager_feature(all_m_ids, start_date, end_date)
    new_m_ids = new_m_ids[1:7] + new_m_ids[9:]
    for m_id in new_m_ids:
        managers[m_id]['other'] = True
    objects = []
    for m_id in exist_m_id:
        # if common.manager_dict[m_id]['index'] in [12]:
        #     objects.append(m_id)
        managers[m_id]['other'] = False
    funds, manager_funds = fund_data.get_fund_loc(exist_m_id, new_m_ids, start_date, end_date)
    for i in objects:
        managers.pop(i)
    return {'funds': funds, 'managers': managers, 'manager_funds': manager_funds}


@app.route('/update_weights', methods=['POST'])
def update_weights():
    _json = request.get_json()
    weights = _json['weights']
    pairs = _json['pairs']
    start_date = _json['start_date']
    end_date = _json['end_date']
    weights = fund_data.update_fund_weights(weights, pairs, start_date, end_date)
    return weights


if __name__ == '__main__':
    app.run(host='10.76.0.165', port='8888')
