import json


def normalize_fund(f_ids):
    funds = {}
    for f_id in fund_ids:
        fund = common.get_view_fund_json(f_id)
        for _date, _value in fund.items():
            dates.add(_date)
            if min_nav_len > len(_value['risks']):
                min_nav_len = len(_value['risks'])
            _value.pop('holding')
            if 'instl_weight' in _value:
                _value.pop('instl_weight')
                _value.pop('retail_weight')
            fund[_date] = _value
            init_fund_data[f_id] = _value
            if 'size' in _value and (max_size is None or max_size < _value['size']):
                max_size = _value['size']
        funds[f_id] = fund