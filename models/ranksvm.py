import csv
from sklearn import svm
from sklearn.decomposition import PCA
import numpy as np


def pair(x, y):
    x2 = []
    y2 = []
    for i in range(len(x)):
        for k in range(len(x)):
            if i == k or y[i, 0] == y[k, 0] or y[i, 1] != y[k, 1]:
                continue
            x2.append(x[i] - x[k])
            y2.append(np.sign(y[i, 0] - y[k, 0]))
    return np.asarray(x2), np.asarray(y2)


def train(x, y):
    x2, y2 = pair(x, y)
    svc = svm.SVC(kernel='linear').fit(x2, y2)
    return svc


def sort(s):
    r = []
    for i in range(len(s)):
        r.append((str(i + 1), s[i]))
    r.sort(key=lambda tup: tup[1], reverse=True)
    r = np.asarray(r)
    return r


def predict(svc, x):
    s = []
    for i in range(len(x)):
        t = []
        for k in range(len(x)):
            if i != k:
                t.append(x[i] - x[k])
        s.append(sum(svc.predict(np.asarray(t))))
    return sort(np.asarray(s))


def pca(x):
    pca = PCA(n_components='mle', svd_solver='full')
    # pca=PCA(n_components=12,svd_solver='full')
    return pca.fit_transform(x)


if __name__ == '__main__':
    # data
    _train = np.arange(92)
    _test = np.arange(88)

    x = []
    for t in csv.reader(open('./data/model/x.csv', 'r')):
        x.append(t)
    x = np.asarray(x, 'f')

    y = []
    for t in csv.reader(open('./data/model/y.csv', 'r')):
        y.append(t)
    y = np.asarray(y, 'd')

    # train
    rsvm = train(x[_train], y[_train])
    # rank
    r = predict(rsvm, x[_test])
