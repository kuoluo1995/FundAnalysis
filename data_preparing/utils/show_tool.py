from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

colors = ['red', 'orange', 'yellow', 'green', 'cyan', 'blue', 'purple', 'black']

plt.rcParams['font.sans-serif'] = ['Noto Serif CJK JP']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
SavePath = '../images/'


def pie_chart(list_value, label_dict, title):
    # 绘制饼图
    print('{}: 开始画饼状图'.format(title), end='')
    # print('{}: 开始画饼状图'.format(title))
    value_dict = Counter(list_value)
    values, labels = [], []
    for key, name in label_dict.items():
        values.append(value_dict[key])
        labels.append(name)
    plt.figure(figsize=(6, 6))  # 将画布设定为正方形，则绘制的饼图是正圆
    plt.pie(values, labels=labels, autopct='%1.2f%%')
    plt.title(title)
    plt.savefig(SavePath + '{}_pie.png'.format(title))
    plt.show()
    print('\r{}: 饼状图绘制完毕'.format(title))


def bar(labels, values, title, re_size=True, align='edge'):
    # 显示高度
    if re_size:
        plt.figure(figsize=(len(values) // 6, 6))

    def auto_label(rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2. - 0.2, 1.03 * height, '%s' % int(height))

    rects = plt.bar(labels, values, color=colors, align=align)
    plt.xticks(labels, labels, rotation=-90)
    auto_label(rects)
    plt.title(title)
    plt.savefig(SavePath + '{}_bar.png'.format(title))
    plt.show()


def bar_chart(list_value, title, has_nan=False, has_none=False, has_nat=False, need_zero=False, gap=None, num_gap=None,
              value_sort=False, is_long=True):
    # 将数组等分
    print('{}: 开始画柱状图'.format(title), end='', flush=True)
    # print('{}: 开始画柱状图'.format(title), flush=True)
    labels, values = [], []
    if has_none:
        labels.append('none')
        values.append(len([_ for _ in list_value if _ is None]))
        list_value = [_ for _ in list_value if _ is not None]
    list_value.sort()
    list_value = np.array(list_value)
    if has_nan:
        labels.append('nan')
        values.append(len(list_value[np.isnan(list_value)]))
        list_value = list_value[~np.isnan(list_value)]
    if need_zero:
        labels.append(str(0))
        values.append(sum(list_value == 0))
        list_value = np.array(list_value).ravel()[np.flatnonzero(list_value)]
    if gap is None and num_gap is not None:
        gap = np.ptp(list_value) // num_gap + 1
    if num_gap is None and gap is not None:
        num_gap = int(np.ptp(list_value) // gap + 1)
    if num_gap is None and gap is None:
        value_dict = Counter(list_value)
    else:
        value_dict = {
            '{:.2f}'.format(gap * i + list_value.min()) if isinstance(gap * i + list_value.min(), float) else str(
                gap * i + list_value.min()): 0 for i in range(num_gap + 1)}
        _num = len(list_value)
        for i, _v in enumerate(list_value):
            gap_value = (_v - list_value.min()) // gap * gap + list_value.min()
            if isinstance(gap_value, float):
                gap_value = '{:.2f}'.format(gap_value)
            else:
                gap_value = str(gap_value)
            value_dict[gap_value] += 1
            print('\r{}:{}/{} {:.2f}%'.format(title, i + 1, _num, (i + 1) / _num * 100), end='')
            # print('\r{}:{}/{} {:.2f}%'.format(title, i + 1, _num, (i + 1) / _num * 100))
    if value_sort:
        value_dict_list = sorted(value_dict.items(), key=lambda d: d[1], reverse=True)
        value_dict = {}
        for _k, _v in value_dict_list:
            value_dict[_k] = _v
    # 将数组按照展示格式分布
    for _k, _v in value_dict.items():
        labels.append(str(_k))
        values.append(_v)
    bar(labels, values, title, re_size=is_long, align='center')
    print('\r{}: 柱状图绘制完毕                                   '.format(title))
