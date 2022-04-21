from cv2.cv2 import erode, boxFilter
from numpy import ones, histogram, cumsum, mean, minimum, zeros, clip, log
from numpy import min as np_min


def MinFilterGray(src, r=7):
    '''
    最小值滤波，r是滤波器半径
    if r <= 0:
        return src
    h, w = src.shape[:2]
    I = src
    res = minimum(I  , I[[0]+range(h-1)  , :])
    res = minimum(res, I[range(1,h)+[h-1], :])
    I = res
    res = minimum(I  , I[:, [0]+range(w-1)])
    res = minimum(res, I[:, range(1,w)+[w-1]])
    return zmMinFilterGray(res, r-1)
    '''
    return erode(src, ones((2 * r + 1, 2 * r + 1)))  # 使用opencv的erode函数更高效


def guidedfilter(I, p, r, eps):
    '''引导滤波，直接参考网上的matlab代码'''
    height, width = I.shape
    m_I = boxFilter(I, -1, (r, r))
    m_p = boxFilter(p, -1, (r, r))
    m_Ip = boxFilter(I * p, -1, (r, r))
    cov_Ip = m_Ip - m_I * m_p

    m_II = boxFilter(I * I, -1, (r, r))
    var_I = m_II - m_I * m_I

    a = cov_Ip / (var_I + eps)
    b = m_p - a * m_I

    m_a = boxFilter(a, -1, (r, r))
    m_b = boxFilter(b, -1, (r, r))
    return m_a * I + m_b


def getV1(m, r, eps, w, maxV1):  # 输入rgb图像，值范围[0,1]
    '''计算大气遮罩图像V1和光照值A, V1 = 1-t/A'''
    V1 = np_min(m, 2)  # 得到暗通道图像
    V1 = guidedfilter(V1, MinFilterGray(V1, 7), r, eps)  # 使用引导滤波优化
    bins = 2000
    ht = histogram(V1, bins)  # 计算大气光照A
    d = cumsum(ht[0]) / float(V1.size)
    for lmax in range(bins - 1, 0, -1):
        if d[lmax] <= 0.999:
            break
    A = mean(m, 2)[V1 >= ht[1][lmax]].max()

    V1 = minimum(V1 * w, maxV1)  # 对值范围进行限制

    return V1, A


def defogging(m, r=81, eps=0.001, w=0.95, maxV1=0.80, bGamma=True):
    Y = zeros(m.shape)
    V1, A = getV1(m, r, eps, w, maxV1)  # 得到遮罩图像和大气光照
    for k in range(3):
        Y[:, :, k] = (m[:, :, k] - V1) / (1 - V1 / A)  # 颜色校正
    Y = clip(Y, 0, 1)
    if bGamma:
        Y = Y ** (log(0.5) / log(Y.mean()))  # gamma校正,默认进行该操作
    return Y

