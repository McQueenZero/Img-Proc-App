from cv2.cv2 import resize
from numpy import histogram, cumsum, clip, zeros, ix_
from math import sqrt


# 线性拉伸处理
# 去掉最大最小0.5%的像素值 线性拉伸至[0,1]
def stretchImage(data, s=0.005, bins=2000):
    ht = histogram(data, bins)
    d = cumsum(ht[0]) / float(data.size)
    lmin = 0
    lmax = bins - 1
    while lmin < bins:
        if d[lmin] >= s:
            break
        lmin += 1
    while lmax >= 0:
        if d[lmax] <= 1 - s:
            break
        lmax -= 1
    return clip((data - ht[1][lmin]) / (ht[1][lmax] - ht[1][lmin]), 0, 1)


# 根据半径计算权重参数矩阵
g_para = {}


def getPara(radius=5):
    global g_para
    m = g_para.get(radius, None)
    if m is not None:
        return m
    size = radius * 2 + 1
    m = zeros((size, size))
    for h in range(-radius, radius + 1):
        for w in range(-radius, radius + 1):
            if h == 0 and w == 0:
                continue
            m[radius + h, radius + w] = 1.0 / sqrt(h ** 2 + w ** 2)
    m /= m.sum()
    g_para[radius] = m
    return m


# 常规的ACE实现
def aceNaive(I, ratio=4, radius=300):
    para = getPara(radius)
    height, width = I.shape
    zh = []
    zw = []
    n = 0
    while n < radius:
        zh.append(0)
        zw.append(0)
        n += 1
    for n in range(height):
        zh.append(n)
    for n in range(width):
        zw.append(n)
    n = 0
    while n < radius:
        zh.append(height - 1)
        zw.append(width - 1)
        n += 1
    # print(zh)
    # print(zw)

    Z = I[ix_(zh, zw)]
    res = zeros(I.shape)
    for h in range(radius * 2 + 1):
        for w in range(radius * 2 + 1):
            if para[h][w] == 0:
                continue
            res += (para[h][w] * clip((I - Z[h:h + height, w:w + width]) * ratio, -1, 1))
    return res


# 单通道ACE快速增强实现
def aceFast(I, ratio, radius):
    # print(I)
    height, width = I.shape[:2]
    if min(height, width) <= 2:
        return zeros(I.shape) + 0.5
    Rs = resize(I, (int((width + 1) / 2), int((height + 1) / 2)))
    Rf = aceFast(Rs, ratio, radius)  # 递归调用
    Rf = resize(Rf, (width, height))
    Rs = resize(Rs, (width, height))

    return Rf + aceNaive(I, ratio, radius) - aceNaive(Rs, ratio, radius)


# rgb三通道分别增强 ratio是对比度增强因子 radius是卷积模板半径
def aceRGB(I, ratio=4, radius=3):
    res = zeros(I.shape)
    for k in range(3):
        res[:, :, k] = stretchImage(aceFast(I[:, :, k], ratio, radius))
    return res
