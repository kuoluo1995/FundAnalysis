from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import csv
import json
import yaml
from sklearn import decomposition, manifold
from pandas import DataFrame
from skfda.preprocessing.dim_reduction.projection import FPCA


def get_init_fund_feature(fund_datas):
    features = []
    clasz = []
    for f_id, _values in fund_datas.items():
        x = []
        y = []
        for _key, _v in _values.items():
            if _key == 'manager_ids':
                for m_id, _ in _v.items():
                    y.append(m_id)
            else:
                x.append(_v['norm'])
        features.append(x)
        clasz.append(y)
    return features, clasz


def update_features(features, clasz, funds, date):
    index_funds = {}
    for i, (f_id, fund) in enumerate(funds.items()):
        if date not in fund:
            continue
        x = []
        y = []
        for _key, _v in fund[date].items():
            if _key == 'manager_ids':
                for m_id, _ in _v.items():
                    y.append(m_id)
            else:
                x.append(_v['norm'])
        features[i] = x
        clasz[i] = y
        index_funds[i] = f_id
    return features, clasz, index_funds


def train(x, init=None):
    # data = decomposition.TruncatedSVD(n_components=3, random_state=999).fit_transform(x)  # PCA svd_solver='full',
    # data = manifold.Isomap(n_components=2).fit_transform(x)
    # pca = decomposition.IncrementalPCA(n_components=3)
    # lr_sgd = pca.partial_fit(x)
    model = manifold.MDS(n_components=2)
    # data = manifold.MDS(n_components=2, random_state=999).fit_transform(x, init=init)
    # data = decomposition.TruncatedSVD(n_components=2, random_state=999).fit_transform(x)
    # model = decomposition.PCA(n_components=2, svd_solver='full', random_state=999)
    _d = model.fit_transform(x)
    # _w = model.components_
    # data = decomposition.KernelPCA(n_components=2, kernel="linear", random_state=9).fit_transform(x)  # rbf
    # import skfda
    # dataset = skfda.datasets.fetch_weather()
    # fd = dataset['data']
    # fpca = FPCA(n_components=3)
    # fpca.fit(fd)
    # fpca.components_.plot()
    # y = dataset['target']
    # fd.plot()
    return _d


if __name__ == '__main__':
    digits = load_digits()
    X = digits.data
    Y = digits.target
    data, weights = train(X)
    plt.scatter(data[:, 0], data[:, 1], c=Y)
    data2 = X.dot(weights.T)
    SavePath = '../images/'
    plt.savefig(SavePath + '{}_pie.png'.format(1))
    plt.close()
    plt.scatter(data2[:, 0], data2[:, 1], c=Y)
    plt.savefig(SavePath + '{}_pie.png'.format(2))
    # Xtrans = mds.fit_transform(X)
    # plt.scatter(Xtrans[:, 0], Xtrans[:, 1], c=Y)
    # plt.savefig(SavePath + '{}_pie.png'.format(2))
    # plt.show()
    print(11)
    print()
