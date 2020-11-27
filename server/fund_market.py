from server import common


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


if __name__ == '__main__':
    sector_date_value = get_market_sector_value()
    print('over')
