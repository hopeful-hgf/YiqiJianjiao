# Conversion parameters Calculater
#  计算转换参数

from math import cos, degrees, radians, sin, sqrt, tan

from scipy.optimize import leastsq, minimize

shcs = [[60000.0000, -22000.0000],
        [54000.0000, 2500.0000],
        [31000.0000, 39000.0000],
        [10000.0000, -30000.0000],
        [18000.0000, 1000.0000],
        [10000.0000, 39000.0000],
        [-21000.0000, -54000.0000],
        [-57000.0000, -11000.0000],
        [-37000.0000, 34000.0000]]


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
    return x, y + 0


def xy2lb(xy, l0):
    '''
    高斯反算: 高斯平面坐标xy -> 大地经纬度lb
    :param xy: 高斯平面坐标
    :return: 大地经纬度lb
    '''
    x = xy[0]
    y = xy[1] - 0
    l0 = radians(l0)
    aa = 1 + 3 / 4 * e ** 2 + 45 / 64 * e ** 4 + 175 / 256 * \
        e ** 6 + 11025 / 16384 * e ** 8 + 43659 / 65536 * e ** 10
    bb = 3 / 4 * e ** 2 + 15 / 16 * e ** 4 + 525 / 512 * \
        e ** 6 + 2205 / 2048 * e ** 8 + 72765 / 65536 * e ** 10
    cc = 15 / 64 * e ** 4 + 105 / 256 * e ** 6 + \
        2205 / 4096 * e ** 8 + 10395 / 16384 * e ** 10
    dd = 35 / 512 * e ** 6 + 315 / 2048 * e ** 8 + 31185 / 131072 * e ** 10
    ee = 315 / 16384 * e ** 8 + 3465 / 65536 * e ** 10

    bf0 = 0
    bf = x / (a * aa * (1 - e ** 2))

    while abs(bf0 - bf) > 1.0e-13:
        bf0 = bf
        bf = x / (a * aa * (1 - e ** 2)) + 1 / aa * (
            bb / 2 * sin(2 * bf0) - cc / 4 * sin(4 * bf0) + dd / 6 * sin(6 * bf0) - ee / 8 * sin(8 * bf0))

    mf = a * (1 - e ** 2) / sqrt(1 - e ** 2 * sin(bf) ** 2)**3
    tf = tan(bf)
    nf = a / (sqrt(1 - e * e * sin(bf) ** 2))
    nnf = sqrt(e * e / (1 - e * e)) * cos(bf)
    b = bf - tf / (2 * mf * nf) * y ** 2 * (
        1 - y ** 2 / (12 * nf ** 2) * (5 * nnf ** 2 + 3 *
                                       tf ** 2 - 9 * nnf ** 2 * tf ** 2)
        + y ** 4 / (360 * nf ** 4) * (61 + 90 * tf ** 2 + 45 * tf ** 4))

    l = l0 + y / (nf * cos(bf)) * (
        1 - y ** 2 / (6 * nf ** 2) * (1 + nnf ** 2 + 2 * tf ** 2)
        + y ** 4 / (120 * nf ** 4) * (5 + 6 * nnf ** 2 + 28 *
                                      tf**2 + 8 * nnf ** 2 * tf ** 2 + 24 * tf ** 4)
    )

    return degrees(l), degrees(b)


def dmmss2d(dmmss):
    strdms = str(dmmss)
    deg = int(dmmss)
    min = int((dmmss - deg) * 100)
    sec = (dmmss - deg - min / 100) * 10000
    deg = deg + min / 60 + sec / 3600
    return deg


def deg2dmmss(deg):
    d = int(deg)
    m = int((deg - d) * 60)
    s = (((deg - d) * 60 - m) * 60)
    return d * 10000 + m * 100 + s


def para(f, t):
    nd = len(f)

    L = []
    B = []
    for i in range(nd):
        L.append(t[i][0])
        L.append(t[i][1])
        B.append([1, 0, f[i][0], f[i][1]])
        B.append([0, 1, -f[i][1], f[i][0]])
    return L, B


if __name__ == "__main__":

    l0 = 121.465
    xy84 = []
    wgsd = []
    for item in wgs84:
        wgsd.append([dmmss2d(item[1]), dmmss2d(item[0])])
    for it in wgsd:
        xy84.append(lb2xy(it, l0))

    lb = []
    for it in xy84:
        lb.append(xy2lb(it, l0))
    # print(lb)s

    print(dmmss2d(121.275570169))
    import numpy as np

    # print(np.array(lb) - np.array(wgsd))

    # delt=np.array(wgsd) - np.array(lb)

    # dist1 = []
    # dist2 = []
    # for i in range(9):
    # for j in range(i + 1, 9):
    # dist1.append(sqrt((xy84[i][0] - xy84[j][0])
    #   ** 2 + (xy84[i][1] - xy84[j][1])**2))
    # dist2.append(sqrt((shcs[i][0] - shcs[j][0])
    #   ** 2 + (shcs[i][1] - shcs[j][1])**2))
    # print(dist1)
    # print(dist2)

    # delt = np.array(dist1) - np.array(dist2)
    # print(delt)

    L, B = para(xy84, shcs)
    L = np.array(L)
    B = np.array(B)
    x = np.mat(B).I * np.mat(L).T

    shcs1 = np.mat(B) * x
    print(shcs1)
    # delt = shcs - shcs1.reshape(9, 2)

    # scipy.optimize.leastsq
    def func(p, x):
        tx, ty, k, s, c = p
        x0, y0 = x
        x1 = tx + k * x0 + c * x0 + s * y0
        y1 = ty + k * y0 + c * y0 - s * x0
        ret = np.array((x1, y1))
        return ret

    def error(p, x, y):
        rt = func(p, x) - y
        rt1 = np.abs(rt).mean()
        return rt1

    p0 = [-3457089, -129, 1, 0, 1]
    x = np.array(xy84).transpose()
    y = np.array(shcs).transpose()
    # x=np.array(xy84)
    # y=np.array(shcs)
    # ppp = leastsq(error, p0, args=(x, y, 'oo'),method = 'Nelder-Mead')
    ppp = minimize(error, p0, method='Nelder-Mead', args=(x, y))

    print(ppp)
    # print(xy84)
