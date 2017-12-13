# Conversion parameters Calculater
#  计算转换参数

from math import radians, sqrt, cos, sin, tan

shcs = [[60000.0000, -22000.0000],
        [54000.0000, 2500.0000],
        [31000.0000, 39000.0000],
        [10000.0000, -30000.0000],
        [18000.0000, 1000.0000],
        [10000.0000, 39000.0000],
        [-21000.0000, -54000.0000],
        [-57000.0000, -11000.0000],
        [37000.0000, 34000.0000]]


wgs84 = [[31.46349499, 121.14056683],
         [31.43208826, 121.29367521],
         [31.30517420, 121.52398457],
         [31.19309388, 121.09070483],
         [31.23520553, 121.28396116],
         [31.19299231, 121.52368592],
         [31.02413296, 120.54052805],
         [30.43166168, 121.21082481],
         [30.54044340, 121.49220014]]

# values will be used in the calculate
a = 6378137
b = 6356752.3142
alfa = (a - b) / a
e = sqrt((a * a - b * b) / (a * a))


def lb2xy(lb, l0):
    '''
    大地经纬度lb -> 高斯平面 x,y
    :param lb: 大地经纬度lb
    :return: xy,子午线收敛角 gamma,投影长度比 m
    '''
    l = radians(lb[0] - l0)
    b = radians(lb[1])
    n = a / (sqrt(1 - e * e * sin(b) * sin(b)))
    nn = sqrt(e * e / (1 - e * e)) * cos(b)
    t = tan(b)

    aa = 1 + 3 / 4 * e ** 2 + 45 / 64 * e ** 4 + 175 / 256 * \
        e ** 6 + 11025 / 16384 * e ** 8 + 43659 / 65536 * e ** 10
    bb = 3 / 4 * e ** 2 + 15 / 16 * e ** 4 + 525 / 512 * \
        e ** 6 + 2205 / 2048 * e ** 8 + 72765 / 65536 * e ** 10
    cc = 15 / 64 * e ** 4 + 105 / 256 * e ** 6 + \
        2205 / 4096 * e ** 8 + 10395 / 16384 * e ** 10
    dd = 35 / 512 * e ** 6 + 315 / 2048 * e ** 8 + 31185 / 131072 * e ** 10
    ee = 315 / 16384 * e ** 8 + 3465 / 65536 * e ** 10
    ff = 639 / 131072 * e ** 10

    xx = a * (1 - e ** 2) * (
        aa * b - bb / 2 * sin(2 * b) + cc / 4 * sin(4 * b) - dd / 6 * sin(6 * b) + ee / 8 * sin(8 * b) - ff / 10 * sin(
            10 * b))
    # m=l*cos(b)

    x = xx + n / 2 * sin(b) * cos(b) * l * l \
        + n / 24 * sin(b) * cos(b) ** 3 * (5 - t * t + 9 * nn * nn + 4 * nn ** 4) * l ** 4 \
        + n / 720 * sin(b) * cos(b) ** 5 * (61 - 58 * t ** 2 + t ** 4) * l ** 6 \
        + n / 40320 * sin(b) * cos(b) ** 7 * (1385 - 311 *
                                              t * t + 543 * t ** 4 - t ** 6) * l ** 8

    y = n * cos(b) * l \
        + n / 6 * cos(b) ** 3 * (1 - t * t + nn * nn) * l ** 3 \
        + n / 120 * cos(b) ** 5 * (5 - 18 * t * t + t ** 4 + 14 * nn * nn - 58 * nn * nn * t * t) * l ** 5 \
        + n / 5040 * cos(b) ** 7 * (61 - 479 * t * t +
                                    179 * t ** 4 - t ** 6) * l ** 7

    gammar = sin(b) * l \
        + 1 / 3 * sin(b) * cos(b) ** 2 * (1 + 3 * nn ** 2 + 2 * nn ** 4) * l ** 3 \
        + 1 / 15 * sin(b) * cos(b) ** 4 * (2 - t ** 2 + 15 * nn ** 2 - 15 * t * t * nn * nn) * l ** 5 \
        + 1 / 315 * sin(b) * cos(b) ** 6 * \
        (17 - 26 * t ** 2 + 2 * t ** 4) * l ** 7
    m = 1 + 1 / 2 * cos(b) ** 2 * (1 + nn ** 2) * l ** 2 \
        + 1 / 24 * cos(b) ** 4 * (5 - 4 * t ** 2 + 14 * nn ** 2 - 28 * t ** 2 * nn ** 2) * l ** 4 \
        + 1 / 720 * cos(b) ** 6 * (61 - 148 * t ** 2 + 16 * t ** 4) * l ** 6
    return x, y + 500000
    '''
    大地经纬度lb -> 高斯平面 x,y
    :param lb: 大地经纬度lb
    :return: xy,子午线收敛角 gamma,投影长度比 m
    '''
    l = radians(lb[0] - l0)
    b = radians(lb[1])
    n = a / (sqrt(1 - e * e * sin(b) * sin(b)))
    nn = sqrt(e * e / (1 - e * e)) * cos(b)
    t = tan(b)

    aa = 1 + 3 / 4 * e ** 2 + 45 / 64 * e ** 4 + 175 / 256 * \
        e ** 6 + 11025 / 16384 * e ** 8 + 43659 / 65536 * e ** 10
    bb = 3 / 4 * e ** 2 + 15 / 16 * e ** 4 + 525 / 512 * \
        e ** 6 + 2205 / 2048 * e ** 8 + 72765 / 65536 * e ** 10
    cc = 15 / 64 * e ** 4 + 105 / 256 * e ** 6 + \
        2205 / 4096 * e ** 8 + 10395 / 16384 * e ** 10
    dd = 35 / 512 * e ** 6 + 315 / 2048 * e ** 8 + 31185 / 131072 * e ** 10
    ee = 315 / 16384 * e ** 8 + 3465 / 65536 * e ** 10
    ff = 639 / 131072 * e ** 10

    xx = a * (1 - e ** 2) * (
        aa * b - bb / 2 * sin(2 * b) + cc / 4 * sin(4 * b) - dd / 6 * sin(6 * b) + ee / 8 * sin(8 * b) - ff / 10 * sin(
            10 * b))
    # m=l*cos(b)

    x = xx + n / 2 * sin(b) * cos(b) * l * l \
        + n / 24 * sin(b) * cos(b) ** 3 * (5 - t * t + 9 * nn * nn + 4 * nn ** 4) * l ** 4 \
        + n / 720 * sin(b) * cos(b) ** 5 * (61 - 58 * t ** 2 + t ** 4) * l ** 6 \
        + n / 40320 * sin(b) * cos(b) ** 7 * (1385 - 311 *
                                              t * t + 543 * t ** 4 - t ** 6) * l ** 8

    y = n * cos(b) * l \
        + n / 6 * cos(b) ** 3 * (1 - t * t + nn * nn) * l ** 3 \
        + n / 120 * cos(b) ** 5 * (5 - 18 * t * t + t ** 4 + 14 * nn * nn - 58 * nn * nn * t * t) * l ** 5 \
        + n / 5040 * cos(b) ** 7 * (61 - 479 * t * t +
                                    179 * t ** 4 - t ** 6) * l ** 7

    gammar = sin(b) * l \
        + 1 / 3 * sin(b) * cos(b) ** 2 * (1 + 3 * nn ** 2 + 2 * nn ** 4) * l ** 3 \
        + 1 / 15 * sin(b) * cos(b) ** 4 * (2 - t ** 2 + 15 * nn ** 2 - 15 * t * t * nn * nn) * l ** 5 \
        + 1 / 315 * sin(b) * cos(b) ** 6 * \
        (17 - 26 * t ** 2 + 2 * t ** 4) * l ** 7
    m = 1 + 1 / 2 * cos(b) ** 2 * (1 + nn ** 2) * l ** 2 \
        + 1 / 24 * cos(b) ** 4 * (5 - 4 * t ** 2 + 14 * nn ** 2 - 28 * t ** 2 * nn ** 2) * l ** 4 \
        + 1 / 720 * cos(b) ** 6 * (61 - 148 * t ** 2 + 16 * t ** 4) * l ** 6
    return x, y + 0


def dmmss2d(dmmss):
    strdms = str(dmmss)
    deg = int(dmmss)
    min = int((dmmss - deg) * 100)
    sec = (dmmss - deg - min / 100) * 10000
    deg = deg + min / 60 + sec / 3600
    return deg


def para(f, t):


if __name__ == "__main__":
    xy84 = []
    for item in wgs84:
        lb = (dmmss2d(item[1]), dmmss2d(item[0]))
        xy84.append(lb2xy(lb, 121))

    print(xy84)