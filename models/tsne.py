import numpy as np
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
import time

np.random.seed(42)


def cal_pairwise_dist(x):
    '''计算pairwise 距离, x是matrix
       (a-b)^2 = a^2 + b^2 - 2*a*b
    '''
    sum_x = np.sum(np.square(x), 1)
    dist = np.add(np.add(-2 * np.dot(x, x.T), sum_x).T, sum_x)
    return dist  # 返回任意两个点之间距离的平方


def cal_perplexity(dist, idx=0, beta=1.0):
    '''计算perplexity, D是距离向量，
       idx指dist中自己与自己距离的位置，beta是高斯分布参数
       这里的perp仅计算了熵，方便计算
    '''
    prob = np.exp(-dist * beta)
    prob[idx] = 0  # 设置自身prob为0
    sum_prob = np.sum(prob)
    if sum_prob < 1e-12:
        prob = np.maximum(prob, 1e-12)
        perp = -12
    else:
        perp = np.log(sum_prob) + beta * np.sum(dist * prob) / sum_prob
        prob /= sum_prob
    return perp, prob  # 困惑度和pi\j的概率分布


def seach_prob(x, tol=1e-5, perplexity=30.0):  # 二分搜索寻找beta,并计算pairwise的prob
    # 初始化参数
    print("Computing pairwise distances...")
    (n, d) = x.shape
    dist = cal_pairwise_dist(x)
    dist[dist < 0] = 0
    pair_prob = np.zeros((n, n))
    beta = np.ones((n, 1))
    base_perp = np.log(perplexity)  # 取log，方便后续计算
    for i in range(n):
        if i % 500 == 0:
            print("Computing pair_prob for point %s of %s ..." % (i, n))
        beta_min = -np.inf
        beta_max = np.inf
        perp, this_prob = cal_perplexity(dist[i], i, beta[i])
        # 二分搜索,寻找最佳sigma下的prob
        perp_diff = perp - base_perp
        tries = 0
        while np.abs(perp_diff) > tol and tries < 50:
            if perp_diff > 0:
                beta_min = beta[i].copy()
                if beta_max == np.inf or beta_max == -np.inf:
                    beta[i] = beta[i] * 2
                else:
                    beta[i] = (beta[i] + beta_max) / 2
            else:
                beta_max = beta[i].copy()
                if beta_min == np.inf or beta_min == -np.inf:
                    beta[i] = beta[i] / 2
                else:
                    beta[i] = (beta[i] + beta_min) / 2
            perp, this_prob = cal_perplexity(dist[i], i, beta[i])  # 更新perb,prob值
            perp_diff = perp - base_perp
            tries = tries + 1
        pair_prob[i,] = this_prob  # 记录prob值
    print("Mean value of sigma: ", np.mean(np.sqrt(1 / beta)))
    return pair_prob  # 每个点对其他点的条件概率分布pi\j


def t_sne(P, n, y, dy, iy, gains, no_dims=2, max_iter=1000, initial_momentum=0.5, final_momentum=0.8, eta=500,
          min_gain=0.01):
    # early exaggeration
    print("T-SNE DURING:%s" % time.clock())
    for iter in range(max_iter):  # Run iterations
        # Compute pairwise affinities
        sum_y = np.sum(np.square(y), 1)
        num = 1 / (1 + np.add(np.add(-2 * np.dot(y, y.T), sum_y).T, sum_y))
        num[range(n), range(n)] = 0
        Q = num / np.sum(num)  # qij
        Q = np.maximum(Q, 1e-12)  # X与Y逐位比较取其大者

        # Compute gradient
        PQ = P - Q  # pij-qij
        for i in range(n):  # 梯度dy
            dy[i, :] = np.sum(np.tile(PQ[:, i] * num[:, i], (no_dims, 1)).T * (y[i, :] - y), 0)
        # Perform the update
        if iter < 20:
            momentum = initial_momentum
        else:
            momentum = final_momentum

        gains = (gains + 0.2) * ((dy > 0) != (iy > 0)) + (gains * 0.8) * ((dy > 0) == (iy > 0))
        gains[gains < min_gain] = min_gain
        iy = momentum * iy - eta * (gains * dy)  # 迭代
        y = y + iy
        y = y - np.tile(np.mean(y, 0), (n, 1))
        # Compute current value of cost function\
        if (iter + 1) % 100 == 0:
            C = np.sum(P * np.log(P / Q))
            print("Iteration ", (iter + 1), ": error is ", C)
            if (iter + 1) != 100:
                ratio = C / oldC
                print("ratio ", ratio)
                if ratio >= 0.95:
                    break
            oldC = C
    print("finished training!")
    return y, dy, iy, gains


def get_p(x, perplexity=30.0):
    P = seach_prob(x, 1e-5, perplexity)  # 对称化
    P = P + np.transpose(P)
    P = P / np.sum(P)  # pij  pi\j，提前夸大
    P = np.maximum(P, 1e-12)
    return P


def get_y(n, d):
    y = np.random.randn(n, d)
    dy = np.zeros((n, d))  # dy梯度
    iy = np.zeros((n, d))  # iy是什么
    gains = np.ones((n, d))
    return y, dy, iy, gains


def get_fund_feature(fund_datas, max_return, max_risk, max_sharp_ratio, max_information_ratio, max_alpha, max_beta,
                     max_size, min_size):
    features = []
    clasz = []
    for f_id, _value in fund_datas.items():
        x = []
        y = []
        x.append(_value['nav_return'] / max_return)
        x.append(_value['risk'] / max_risk)
        x.append(_value['sharp_ratio'] / max_sharp_ratio)
        x.append(_value['information_ratio'] / max_information_ratio)
        x.append(_value['alpha'] / max_alpha)
        x.append(_value['beta'] / max_beta)
        x.append((_value['size'] - min_size) / (max_size - min_size))
        for m_id, _ in _value['manager_ids'].items():
            y.append(m_id)
        features.append(x)
        clasz.append(y)
    return features, clasz


def get_manager_feature(manager_dict, max_return, max_car, max_risk, max_size, min_size, max_alpha, max_beta,
                        max_sharp_ratio, max_information_ratio, max_days, min_days):
    features = []
    for m_id, _value in manager_dict.items():
        x = []
        x.append(_value['nav_return'] / max_return)
        x.append(_value['car'] / max_car)
        x.append(_value['risk'] / max_risk)
        x.append((_value['size'] - min_size) / (max_size - min_size))
        x.append((_value['days'] - min_days) / (max_days - min_days))
        x.append(_value['alpha'] / max_alpha)
        x.append(_value['beta'] / max_beta)
        x.append(_value['sharp_ratio'] / max_sharp_ratio)
        x.append(_value['information_ratio'] / max_information_ratio)
        features.append(x)
    return features


def update_features(features, clasz, funds, date, max_return, max_risk, max_sharp_ratio, max_information_ratio,
                    max_alpha, max_beta, max_size, min_size):
    index_funds = {}
    for i, (f_id, fund) in enumerate(funds.items()):
        if date not in fund:
            continue
        x = []
        y = []
        x.append(fund[date]['nav_return'] / max_return)
        x.append(fund[date]['risk'] / max_risk)
        x.append(fund[date]['sharp_ratio'] / max_sharp_ratio)
        x.append(fund[date]['information_ratio'] / max_information_ratio)
        x.append(fund[date]['alpha'] / max_alpha)
        x.append(fund[date]['beta'] / max_beta)
        x.append((fund[date]['size'] - min_size) / (max_size - min_size))
        for m_id, _ in fund[date]['manager_ids'].items():
            y.append(m_id)
        features[i] = x
        clasz[i] = y
        index_funds[i] = f_id
    return features, clasz, index_funds


if __name__ == "__main__":
    digits = load_digits()
    X = digits.data
    Y = digits.target
    # 随机初始化Y
    (n, d) = X.shape
    no_dims = 2
    y, dy, iy, gains = get_y(n, no_dims)
    p = get_p(X)
    data_2d, dy, iy, gains = t_sne(p, n, y, dy, iy, gains, no_dims)
    plt.scatter(data_2d[:, 0], data_2d[:, 1], c=Y)
    plt.show()

    data_2d, dy, iy, gains = t_sne(p, n, y, dy, iy, gains, no_dims, max_iter=500)
    plt.scatter(data_2d[:, 0], data_2d[:, 1], c=Y)
    plt.show()
    print(11)
