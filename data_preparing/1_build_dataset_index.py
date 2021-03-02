import os
import csv
import json
import datetime

DATAPath = '/home/kuoluo/data/fund'

if __name__ == '__main__':
    col_index = []
    index_dict = {}
    # files = os.listdir(DATAPath + '/index')
    files = ['沪深300.csv', '中证500.csv']
    for file in files:
        with open(DATAPath + '/index/' + file, 'r', encoding='gbk') as _f:
            index_csv = csv.reader(_f)
            for i, row in enumerate(index_csv):
                if i == 0:
                    col_index = row
                    continue
                if file[:-4] not in index_dict:
                    index_dict[file[:-4]] = {}
                _date = row[0].replace('-', '')
                index_dict[file[:-4]][_date] = {col_index[3]: float(row[3]), col_index[6]: float(row[6])}
        _index = sorted(index_dict[file[:-4]].items(), key=lambda d: int(d[0]), reverse=False)
        temp = dict()
        for _date, _value in _index:
            temp[_date] = _value
        index_dict[file[:-4]] = temp
        print()
    with open(DATAPath + '/index.json', 'w') as wp:
        json.dump(index_dict, wp)
    print('数据集保存成功')
