import colorsys
import json
import random
from colour import Color

project_path = '/home/kuoluo/projects/FundAnalysis'
# project_path = 'E:/Projects/PythonProjects/FundAnalysis'
with open(project_path + '/data/dictionary/color_dict.json', 'r', encoding='UTF-8') as rp:
    color_dict = json.load(rp)


def get_hls_colors_by_num(num):
    hls_colors = []
    step = 360.0 / num
    _i = 0
    while _i < 360.0:
        _h = _i
        _s = 80 + random.random() * 10
        _l = 40 + random.random() * 5
        _hls = [_h / 360.0, _l / 100.0, _s / 100.0]
        hls_colors.append(_hls)
        _i += step
    return hls_colors


def get_rgb_colors_by_num(num):
    rgb_colors = []
    if num < 1:
        return rgb_colors
    hls_colors = get_hls_colors_by_num(num)
    for _hls in hls_colors:
        _r, _g, _b = colorsys.hls_to_rgb(_hls[0], _hls[1], _hls[2])
        r, g, b = [int(x * 255.0) for x in (_r, _g, _b)]
        rgb_colors.append([r, g, b])
    return rgb_colors


def get_hex_colors_by_num(num):
    hex_colors = []
    rgb_colors = get_rgb_colors_by_num(num)  # 将RGB格式划分开来
    for _rgb in rgb_colors:
        _sc = '#'
        for i in _rgb:
            num = int(i)  # 将str转int
            _sc += str(hex(num))[-2:].replace('x', '0').upper()  # 将R、G、B分别转化为16进制拼接转换并大写
        hex_colors.append(_sc)
    return hex_colors


def get_red_dict_by_num(num): #ffffbf
    gray = Color("#ecf7e4")#DBB622
    colors = list(gray.range_to(Color("red"), num)) #DB302C
    result = {}
    for i in range(num):
        result[i] = colors[i]
    return result


def get_green_dict_by_num(num):
    # gray = Color("white") #DBB622
    gray = Color("#ecf7e4") #DBB622
    colors = list(gray.range_to(Color("green"), num)) #18DB58
    result = {}
    for i in range(num):
        result[i] = colors[i]
    return result


def get_green2red_dict_by_num(num):
    green = Color("#ffffb3")
    colors = list(green.range_to(Color("#FF8B85"), num))
    result = {}
    for i in range(num):
        result[i] = colors[i]
    return result


def get_color_value(_key):
    return color_dict[_key]


if __name__ == '__main__':
    _red = get_red_dict_by_num(100)
    _green = get_green_dict_by_num(100)
    print()
