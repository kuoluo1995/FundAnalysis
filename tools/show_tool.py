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


def bar(labels, values, title, re_size=True, align='edge', save_path=None):
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
    plt.gcf().subplots_adjust(bottom=0.21)
    plt.title(title)
    if save_path is None:
        plt.savefig(SavePath + '{}_bar.png'.format(title))
    else:
        plt.savefig(save_path)
    plt.show()


def bar_chart(list_value, title, has_nan=False, has_none=False, has_nat=False, need_zero=False, gap=None, num_gap=None,
              value_sort=False, is_long=True, save_path=None, align='center'):
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
    bar(labels, values, title, re_size=is_long, align=align, save_path=save_path)
    print('\r{}: 柱状图绘制完毕                                   '.format(title))


def object_merge_fund(_dict, merge_type, sort_type=None):
    object_date_value = {}
    for id_name, funds in _dict.items():
        object_date_value[id_name] = {}
        for f_id, values in funds.items():
            for _date, _value in values.items():
                if _date not in object_date_value[id_name]:
                    object_date_value[id_name][_date] = []
                object_date_value[id_name][_date].append(_value)
    for id_name, values in object_date_value.items():
        for _date, _value in values.items():
            if merge_type == 'sum':
                object_date_value[id_name][_date] = np.sum(_value)
            elif merge_type == 'mean':
                object_date_value[id_name][_date] = np.mean(_value)
            elif merge_type == 'weight':
                object_date_value[id_name][_date] = np.sum(np.array(_value))
        if sort_type is not None:
            if sort_type == 'key':
                date_values = sorted(object_date_value[id_name].items(), key=lambda d: int(d[0]), reverse=False)
            elif sort_type == 'value':
                date_values = sorted(object_date_value[id_name].items(), key=lambda d: d[1], reverse=True)
            else:
                print('error: sort_type={}'.format(sort_type))
            object_date_value[id_name] = {}
            for _date, _value in date_values:
                object_date_value[id_name][_date] = _value
    return object_date_value


def dict2labels(_dict, is_sort=True):
    all_labels = set()
    for _, date_value in _dict.items():
        all_labels.update(date_value.keys())
    all_labels = list(all_labels)
    if is_sort:
        all_labels = sorted(list(all_labels), key=lambda d: int(d), reverse=False)
    return all_labels


def dict2values(_dict, all_labels, none_value='zero'):
    dict_values = {}
    for id_name, date_value in _dict.items():
        dict_values[id_name] = []
        for _date in all_labels:
            if _date in date_value:
                dict_values[id_name].append(date_value[_date])
            else:
                if len(dict_values[id_name]) == 0 or none_value == 'zero':
                    dict_values[id_name].append(0)
                elif none_value == 'previous':
                    dict_values[id_name].append(dict_values[id_name][-1])
                else:
                    print('error')
    return dict_values
