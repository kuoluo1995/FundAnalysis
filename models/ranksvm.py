import json

from sklearn import svm
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd


def build_train_data(features, weight, pair_result):
    rows = {}
    data_x = []
    data_y = []
    for _pair in pair_result:
        f_ids = set()
        for f_id in _pair.keys():
            if f_id not in rows:
                cols = []
                for _name, _v in weight.items():
                    cols.append(float(_v) * features[f_id][_name])
                rows[f_id] = np.asarray(cols, 'f')
            f_ids.add(f_id)
        for f_id1 in f_ids:
            for f_id2 in f_ids:
                if f_id1 == f_id2 or _pair[f_id1] == _pair[f_id2]:
                    continue
                data_x.append(rows[f_id1] - rows[f_id2])
                data_y.append(np.sign(_pair[f_id1] - _pair[f_id2]))
    return np.asarray(data_x), np.asarray(data_y), rows


def train_by_pair_data(x, y):
    svc = svm.SVC().fit(x, y)
    return svc


def predict(svc, test_data):
    scores = {}
    for f_id1, _v1 in test_data.items():
        cols = []
        for f_id2, _v2 in test_data.items():
            if f_id1 != f_id2:
                cols.append(test_data[f_id1] - test_data[f_id2])
        scores[f_id1] = sum(svc.predict(np.asarray(cols)))
    return scores


def updata_weight(weights, feature, scores):
    new_features = []
    for f_id, score in scores.items():
        temp = {'score': float(score)}
        for i, (_name, _v) in enumerate(weights.items()):
            temp[_name] = feature[f_id][i]
        new_features.append(temp)
    features = pd.DataFrame(new_features)
    corr_matrix = features.corr()
    new_weights = corr_matrix['score'].sort_values(ascending=False)
    new_weights = new_weights.to_dict()
    new_weights.pop('score')
    for _name, _value in new_weights.items():
        if np.isnan(_value):
            new_weights[_name] = 0
        if _name in ['one_quarter_return', 'one_year_return', 'three_year_return', 'sharp_ratio', 'information_ratio']:
            new_weights[_name] = (new_weights[_name] + 1) / 2
        if _name in ['risk', 'max_drop_down']:
            new_weights[_name] = (new_weights[_name] - 1) / 2
        # new_weights[_name] = (new_weights[_name] + float(weights[_name])) / 2
    return_sum = new_weights['one_quarter_return'] + 1
    return_sum += new_weights['one_year_return'] + 1
    return_sum += new_weights['three_year_return'] + 1
    new_weights['one_quarter_return'] = (new_weights['one_quarter_return'] + 1) / return_sum
    new_weights['one_year_return'] = (new_weights['one_year_return'] + 1) / return_sum
    new_weights['three_year_return'] = (new_weights['three_year_return'] + 1) / return_sum
    return new_weights


def pca(x):
    pca = PCA(n_components='mle', svd_solver='full')
    # pca=PCA(n_components=12,svd_solver='full')
    return pca.fit_transform(x)


if __name__ == '__main__':
    # data
    project_path = '/home/kuoluo/projects/FundAnalysis'
    pairs = [{'001740': 0, '001790': 1}, {'001790': 0, '000717': 1},
             {'000717': 0, '003834': 1}, {'003834': 0, '005911': 1}, {'003745': 0, '002939': 1}]
    weights = {'stock': 0.0, 'bond': 0.0, 'cash': 0.0, 'other': 0.0, 'size': 0.0, 'alpha': 0.0, 'beta': 0.0,
               'sharp_ratio': 0.0, 'max_drop_down': 0.0, 'information_ratio': 0.0, 'nav_return': 1.0, 'risk': 0.0,
               'instl_weight': 0.0, 'car': 0.0}
    with open(project_path + '/data/dictionary/global_fund_features.json', 'r', encoding='UTF-8') as rp:
        global_fund_features = json.load(rp)
    x, y, _rows = build_train_data(global_fund_features, weights, pairs)
    rank_svm = train_by_pair_data(x, y)
    scores = predict(rank_svm, _rows)
    weights = updata_weight(weights, global_fund_features, scores)
    print()
