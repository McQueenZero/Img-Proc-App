from numpy import (fromfile, uint8, array, zeros, ones, float32, mean, where, sqrt, trunc)
from cv2.cv2 import (imdecode, imread, merge, cvtColor, imencode, imwrite, GaussianBlur, Sobel, subtract,
                     convertScaleAbs, split, filter2D, addWeighted, bitwise_not, equalizeHist, fastNlMeansDenoising,
                     adaptiveThreshold, resize, flip, rotate, getRotationMatrix2D, warpAffine, medianBlur,
                     getPerspectiveTransform, warpPerspective)
from cv2.cv2 import (IMREAD_ANYCOLOR, COLOR_BGRA2RGBA, COLOR_BGR2RGB, CV_32F, ADAPTIVE_THRESH_GAUSSIAN_C,
                     THRESH_BINARY, COLOR_BGR2GRAY, COLOR_BGR2HSV, COLOR_HSV2BGR, INTER_LINEAR, INTER_AREA,
                     COLOR_BGR2HSV_FULL, COLOR_BGR2BGRA, COLOR_BGRA2BGR,)
from PyQt5.QtGui import QImage, QColor
from PyQt5.QtCore import QPoint, QPointF, QLineF


class AppImg(object):
    '''
    自编AppImg类
    '''
    def __init__(self):
        '''
        初始化自编AppImg类的属性
        '''
        self.img = None
        self.h, self.w, self.ch, self.bp = None, None, None, None

    @staticmethod
    def _iscontaincnc(check_str: str):  # Contain Chinese Characters Check
        '''
        AppImg类的静态方法，检查输入字符串是否含有中文字符
        '''
        for ch in check_str:
            if 0x4e00 <= ord(ch) <= 0x9fa5:
                return True
        else:
            return False

    def loadimg(self, imgfilepath):
        '''
        加载图片，同时针对性处理路径或文件名含中文字符情况
        根据文件路径用OPENCV读入图片，得到图片数据以及其宽、高、通道数
        AppImg类的实例方法
        '''
        if imgfilepath:
            if self._iscontaincnc(imgfilepath):
                self.img = imdecode(fromfile(imgfilepath, dtype=uint8), -1)
                if self.img.shape[2] > 3:  # 针对含中文路径的PNG图像读出4通道的BUG(本APP不支持处理4通道图像)
                    self.img = merge([self.img[:, :, 0], self.img[:, :, 1], self.img[:, :, 2]])  # 转为3通道
            else:
                self.img = imread(imgfilepath, IMREAD_ANYCOLOR)  # 参数使得即使读取PNG也会只读取前3通道
            try:
                self.h, self.w, self.ch = self.img.shape
                self.bp = self.ch * self.w  # bytesPerline
            except ValueError:  # 针对单通道灰度图，转成三通道假灰度图
                self.img = merge([self.img, self.img, self.img])
                self.h, self.w, self.ch = self.img.shape
                self.bp = self.ch * self.w  # bytesPerline

    def CV2Qimg(self, GRAYFLAG=False, PNGFLAG=False):
        '''
        判断输出CV图无属性需要再计算
        将OPENCV图片转化成QImage图片
        AppImg类的实例方法
        '''
        if self.img is not None:
            if GRAYFLAG:
                self.h, self.w = self.img.shape
                self.bp = self.w  # bytesPerline
                # Qimg_temp = cvt2Gray(self.img)
                Qimg_temp = self.img
                Qimg = QImage(Qimg_temp.data, self.w, self.h, self.bp, QImage.Format_Grayscale8)
            else:
                self.h, self.w, self.ch = self.img.shape
                self.bp = self.ch * self.w  # bytesPerline
                if PNGFLAG:
                    Qimg_temp = cvtColor(self.img, COLOR_BGRA2RGBA)
                    Qimg = QImage(Qimg_temp.data, self.w, self.h, self.bp, QImage.Format_RGBA8888)
                else:
                    Qimg_temp = cvtColor(self.img, COLOR_BGR2RGB)
                    Qimg = QImage(Qimg_temp.data, self.w, self.h, self.bp, QImage.Format_RGB888)

            return Qimg

    def saveimg(self, imgfilepath):
        '''
        保存图片，同时针对性处理路径或文件名含中文字符情况
        根据文件路径用OPENCV写入图片
        AppImg类的实例方法
        '''
        if imgfilepath and self.img is not None:
            if self._iscontaincnc(imgfilepath):
                ext = imgfilepath[imgfilepath.rindex('.'):]  # 文件扩展名
                imencode(ext, self.img)[1].tofile(imgfilepath)
            else:
                imwrite(imgfilepath, self.img)

    def Q2CVimg(self, Qimg: QImage):
        '''
        将QImage图片转化为OPENCV图片
        '''
        if Qimg.depth() != 0:
            if Qimg.width() % 4 != 0:  # 保持原比例将宽放缩为4的倍数, 是OPENCV图像的要求
                Qimg = Qimg.scaled(Qimg.width() % 4 + Qimg.width(), Qimg.height(), 2, 1)
            try:  # PNG图像，四通道
                temp_shape = (Qimg.height(), Qimg.bytesPerLine() * 8 // Qimg.depth())
                temp_shape += (4,)
                ptr = Qimg.bits()
                ptr.setsize(Qimg.byteCount())
                CVimg = array(ptr, dtype=uint8).reshape(temp_shape)
                CVimg = CVimg[..., :3]
            except ValueError:  # 灰度图，单通道
                try:
                    temp_shape = (Qimg.height(), Qimg.bytesPerLine() * 8 // Qimg.depth())
                    ptr = Qimg.bits()
                    ptr.setsize(Qimg.byteCount())
                    CVimg = array(ptr, dtype=uint8).reshape(temp_shape)
                except ValueError:  # JPG图像，三通道
                    temp_shape = (Qimg.height(), Qimg.bytesPerLine() * 8 // Qimg.depth())
                    temp_shape += (3,)
                    ptr = Qimg.bits()
                    ptr.setsize(Qimg.byteCount())
                    CVimg = array(ptr, dtype=uint8).reshape(temp_shape)
                    CVimg = CVimg[..., ::-1]

            self.img = CVimg


def blur_gauss(imSrc, kernal=(9, 9)):
    '''
    应用9x9的高斯滤波
    '''
    if imSrc is not None and imSrc.data is not None:
        imBlur = GaussianBlur(imSrc, kernal, 0)

        return imBlur


def edge_sobel(imSrc):
    '''
    Sobel算子来计算x、y方向梯度
    输出x-y方向的梯度
    '''
    if imSrc is not None and imSrc.data is not None:
        gradX = Sobel(imSrc, ddepth=CV_32F, dx=1, dy=0)
        gradY = Sobel(imSrc, ddepth=CV_32F, dx=0, dy=1)

        imGrad = subtract(gradX, gradY)
        imGrad = convertScaleAbs(imGrad)

        imGrad = cvt2Gray(imGrad)

        return imGrad


def channel_extract(imSrc):
    '''
    通道提取
    输出分别三个通道的图片
    '''
    if imSrc is not None and imSrc.data is not None:
        b, g, r = split(imSrc)
        # imDst_b = merge([b, zeros(b.shape, uint8), zeros(b.shape, uint8)])
        # imDst_g = merge([zeros(g.shape, uint8), g, zeros(g.shape, uint8)])
        # imDst_r = merge([zeros(r.shape, uint8), zeros(r.shape, uint8), r])
        # imDst_b = merge([b, b, b])
        # imDst_g = merge([g, g, g])
        # imDst_r = merge([r, r, r])
        imDst_b = b
        imDst_g = g
        imDst_r = r

        return imDst_r, imDst_g, imDst_b


def sharpen_laplace(imSrc, k=0):
    '''
    用拉普拉斯算子锐化并输出锐化后的图片
    注意锐化的结果是叠加在原图上的
    '''
    if imSrc is not None and imSrc.data is not None:
        kernel = array([[-1, -1, -1],
                          [-1, 8, -1],
                          [-1, -1, -1]])
        imGrad = filter2D(imSrc, -1, kernel)
        imDst = addWeighted(imSrc, 1, imGrad, k, 0)

        return imDst


def invert_color(imSrc):
    '''
    图片反色
    输出反色后的图片
    '''
    if imSrc is not None and imSrc.data is not None:
        imDst = bitwise_not(imSrc)

        return imDst


def hist_eq(imSrc):
    '''
    直方图均衡化
    注意OPENCV的equalizeHist只接受单通道输入
    所以彩色图片需要拆分后histeq再融合输出
    '''
    if imSrc is not None and imSrc.data is not None:
        b, g, r = split(imSrc)
        bH = equalizeHist(b)
        gH = equalizeHist(g)
        rH = equalizeHist(r)
        imDst = merge((bH, gH, rH))

        return imDst


def threshold_adaptive(imSrc, blockSize=15, C=5):
    '''
    自适应二值化（增强锐化）
    '''
    if imSrc is not None and imSrc.data is not None:
        imTemp = cvt2Gray(imSrc)
        imTemp = fastNlMeansDenoising(imTemp, 5, 5, 7, 21)
        imDst = adaptiveThreshold(imTemp, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, blockSize, C)

        return imDst


def cvt2Gray(imSrc, FAKEFLAG=False):
    '''
    转灰度图
    输入三通道，转单通道真灰度图
    输入单通道，转三通道假灰度图
    '''
    if imSrc is not None and imSrc.data is not None:
        if FAKEFLAG:
            return merge([imSrc, imSrc, imSrc])
        else:
            return cvtColor(imSrc, COLOR_BGR2GRAY)


def contrastbright(imSrc, c=0, b=0):
    '''
    调用addWeighted方法调整亮度及对比度
    '''
    if imSrc is not None and imSrc.data is not None:
        if c == 0:
            blank = zeros([imSrc.shape[0], imSrc.shape[1], 3], imSrc.dtype)
        elif b == 0:
            blank = 114 * ones([imSrc.shape[0], imSrc.shape[1], 3], imSrc.dtype)
        else:
            blank = ones([imSrc.shape[0], imSrc.shape[1], 3], imSrc.dtype)
        imDst = addWeighted(imSrc, 1-c, blank, c, b)

        return imDst


def saturation(imSrc, s=0):
    '''
    转换成HSV色彩空间调节饱和度
    '''
    if imSrc is not None and imSrc.data is not None:
        imHSV = cvtColor(imSrc, COLOR_BGR2HSV)
        imHSV = imHSV.astype(float32)
        imHSV[:, :, 1] = (1.0 + s) * imHSV[:, :, 1]
        imHSV[:, :, 1][imHSV[:, :, 1] > 255] = 255
        imHSV[:, :, 1][imHSV[:, :, 1] < 0] = 0
        imDst = cvtColor(imHSV.astype(uint8), COLOR_HSV2BGR)

        return imDst


def zonebrightdark(imSrc, b=0, d=0):
    '''
    根据统计特性区分亮/暗部
    再调节对应区域的亮度
    '''
    if imSrc is not None and imSrc.data is not None:
        h, w, ch = imSrc.shape
        imDst = zeros((h, w, ch))
        imSrc = imSrc.astype(float32)
        maskBool = (imSrc[:, :, 0] + imSrc[:, :, 1] + imSrc[:, :, 2]) / 3 > mean(imSrc)
        for ch in range(3):
            if d == 0:
                imDst[:, :, ch] = where(maskBool, imSrc[:, :, ch] + b, imSrc[:, :, ch])
            elif b == 0:
                imDst[:, :, ch] = where(maskBool, imSrc[:, :, ch], imSrc[:, :, ch] + d)
            else:
                imDst[:, :, ch] = where(maskBool, imSrc[:, :, ch] + b, imSrc[:, :, ch] + d)
            imDst[:, :, ch][imDst[:, :, ch] > 255] = 255
            imDst[:, :, ch][imDst[:, :, ch] < 0] = 0
        imDst = imDst.astype(uint8)

        return imDst


def zoom_scale(imSrc, scale):
    '''
    根据系数放缩
    输出放缩后的图片
    注意：输入是面积系数
    '''
    if imSrc is not None and imSrc.data is not None:
        if scale > 1:
            INPO = INTER_LINEAR
        else:
            INPO = INTER_AREA
        imResize = resize(imSrc, None, fx=sqrt(scale), fy=sqrt(scale), interpolation=INPO)

        return imResize


def crop_ar(imSrc, ratioDst):
    '''
    根据固定的Aspect Ratio（宽高比）裁剪
    输出裁剪后的图片
    '''
    if imSrc is not None and imSrc.data is not None:
        hSrc, wSrc, _ = imSrc.shape
        ratioSrc = wSrc / hSrc
        if ratioDst > ratioSrc:
            wDst = wSrc
            hDst = wDst / ratioDst
        else:
            hDst = hSrc
            wDst = hDst * ratioDst
        h_s = hSrc/2 - hDst/2
        w_s = wSrc/2 - wDst/2
        h_s, hDst, w_s, wDst = map(int, (h_s, hDst, w_s, wDst))
        imCrop = imSrc[h_s:h_s+hDst+1, w_s:w_s+wDst+1]

        return imCrop


def sym_flip(imSrc, flipCode):
    '''
    根据flipCode翻转
    flipCode=0(Vertical) or 1(Horizontal)
    '''
    if imSrc is not None and imSrc.data is not None:
        imSym = flip(imSrc, flipCode)

        return imSym


def rotate_cwra(imSrc, rotateCode):
    '''
    ClockWise Right Angle Rotate, 顺时针直角旋转
    rotateCode = 0, 1, 2分别代表 90°, 180°, 270°
    '''
    if imSrc is not None and imSrc.data is not None:
        imRotate = rotate(imSrc, rotateCode)

        return imRotate


def rotate_deg(imSrc, degree):
    '''
    旋转degree角度
    根据角度计算外接矩形
    输出不裁剪旋转后的图片
    '''
    if imSrc is not None and imSrc.data is not None:
        h, w, _ = imSrc.shape
        cX, cY = w//2, h//2

        M = getRotationMatrix2D((cX, cY), degree, 1.0)
        cos = abs(M[0, 0])
        sin = abs(M[0, 1])

        # 计算旋转后外接矩形的宽和高
        w_new = int((h * sin) + (w * cos))
        h_new = int((h * cos) + (w * sin))

        # 同时考虑平移
        M[0, 2] += w_new / 2 - cX
        M[1, 2] += h_new / 2 - cY

        imRotate = warpAffine(imSrc, M, (w_new, h_new))
        return imRotate


def mosaic_rect(imSrc, point_tl: QPoint, point_br: QPoint, kss):
    '''
    矩形区域打马赛克
    输入图片、左上和右下角点以及核边长(kernel side size)
    例：kss=10表示马赛克单位是10*10的像素格
    '''
    if imSrc is not None and imSrc.data is not None:
        imDst = imSrc.copy()
        for y in range(point_tl.y(), point_br.y()):
            for x in range(point_tl.x(), point_br.x()):
                if y % kss == 0 and x % kss == 0:
                    for j in range(kss):
                        for i in range(kss):
                            b, g, r = imSrc[y, x]
                            # 边界判断，防止超出
                            if y+j < imSrc.shape[0] and x+i < imSrc.shape[1]:
                                imDst[y+j, x+i] = (b, g, r)

        return imDst


def blur_rect(imSrc, point_tl: QPoint, point_br: QPoint, kss):
    '''
    矩形区域平滑模糊
    输入图片、左上和右下角点以及核边长(kernel side size)
    例：kss=9表示马赛克单位是9*9的卷积核
    '''
    if imSrc is not None and imSrc.data is not None:
        imBlur = blur_gauss(imSrc, (kss, kss))
        mask = 255 * ones(imSrc.shape, dtype=uint8)
        if point_tl.isNull() and point_br == QPoint(imSrc.shape[1], imSrc.shape[0]):
            con = 0
        else:
            con = 255
        mask[point_tl.y():point_br.y(), point_tl.x():point_br.x()] = 0
        imDst = where(mask == con, imBlur, imSrc)

        return imDst


def reserve_color(imSrc, color: QColor, width, transFlag=False):
    '''
    保留色彩/透明化
    输入选择的颜色和色相邻域宽度
    例：huewidth=5表示保留选中色的色相±5范围内的颜色
    '''
    if imSrc is not None and imSrc.data is not None:
        imSrc = imSrc.astype(float32)  # 如果uint8，则转换出来每个通道最大255
        imHSV = cvtColor(imSrc, COLOR_BGR2HSV_FULL)
        imHSV = trunc(imHSV).astype(int)  # 转换出hue通道满足0~359整型的数据
        hue = color.hue()

        if hue != -1:  # 有色差颜色，用hue通道区别
            hueleft = hue - width
            hueright = hue + width
            imSrc = imSrc.astype(uint8)
            if not transFlag:
                imGray = cvtColor(imSrc, COLOR_BGR2GRAY)
                imDst = zeros(imSrc.shape, dtype=uint8)
                if hueleft < 0 or hueright > 359:
                    hueleft = hueleft + 360 if hueleft < 0 else hueleft
                    hueright = hueright - 360 if hueright > 359 else hueright
                    for ch in range(3):
                        imDst[:, :, ch] = where(
                            (hueleft <= imHSV[:, :, 0]) | (imHSV[:, :, 0] <= hueright),
                            imSrc[:, :, ch], imGray)
                else:
                    for ch in range(3):
                        imDst[:, :, ch] = where(
                            (hueleft <= imHSV[:, :, 0]) & (imHSV[:, :, 0] <= hueright),
                            imSrc[:, :, ch], imGray)
            else:
                imSrc = cvtColor(imSrc, COLOR_BGR2BGRA)
                imDst = imSrc.copy()
                if hueleft < 0 or hueright > 359:
                    hueleft = hueleft + 360 if hueleft < 0 else hueleft
                    hueright = hueright - 360 if hueright > 359 else hueright
                    imDst[:, :, 3] = where(
                        (hueleft <= imHSV[:, :, 0]) | (imHSV[:, :, 0] <= hueright), 0, 255)
                else:
                    imDst[:, :, 3] = where(
                        (hueleft <= imHSV[:, :, 0]) & (imHSV[:, :, 0] <= hueright), 0, 255)
        else:  # 无色差(灰阶)颜色，用hue和value通道区别
            value = color.value()
            valueleft = value - width
            valueright = value + width
            imSrc = imSrc.astype(uint8)
            if not transFlag:
                imGray = cvtColor(imSrc, COLOR_BGR2GRAY)
                imDst = zeros(imSrc.shape, dtype=uint8)
                if valueleft < 0 or valueright > 255:
                    valueleft = valueleft + 256 if valueleft < 0 else valueleft
                    valueright = valueright - 256 if valueright > 255 else valueright
                    for ch in range(3):
                        imDst[:, :, ch] = where(
                            ((valueleft <= imHSV[:, :, 2]) | (imHSV[:, :, 2] <= valueright))
                            & (imHSV[:, :, 0] == 0), imSrc[:, :, ch], imGray)
                else:
                    for ch in range(3):
                        imDst[:, :, ch] = where(
                            ((valueleft <= imHSV[:, :, 2]) & (imHSV[:, :, 2] <= valueright))
                            & (imHSV[:, :, 0] == 0), imSrc[:, :, ch], imGray)
            else:
                imSrc = cvtColor(imSrc, COLOR_BGR2BGRA)
                imDst = imSrc.copy()
                if valueleft < 0 or valueright > 255:
                    valueleft = valueleft + 256 if valueleft < 0 else valueleft
                    valueright = valueright - 256 if valueright > 255 else valueright
                    imDst[:, :, 3] = where(
                        ((valueleft <= imHSV[:, :, 2]) | (imHSV[:, :, 2] <= valueright))
                        & (imHSV[:, :, 0] == 0), 0, 255)
                else:
                    imDst[:, :, 3] = where(
                        ((valueleft <= imHSV[:, :, 2]) & (imHSV[:, :, 2] <= valueright))
                        & (imHSV[:, :, 0] == 0), 0, 255)

        imDst = medianBlur(imDst, 3)
        return imDst


def cvt2BGR(imSrc):
    '''
    转三通道BGR图
    主要针对imSrc为四通道PNG图片的情况
    '''
    if imSrc is not None and imSrc.data is not None:
        imDst = cvtColor(imSrc, COLOR_BGRA2BGR)

        return imDst


def trans_perspective(imSrc, PointSrc: list[QPointF], switch=False):
    '''
    透视变换
    PointsSrc是原图上四个点的列表(顺时针排序)
    PointsTar由PointsSrc计算的宽、高自动确定
    '''
    p1 = []
    for p in PointSrc:
        p1.append([p.x(), p.y()])
    w, h = perspectiveWH(PointSrc, switch)
    if switch:
        p2 = [[w, 0], [w, h], [0, h], [0, 0]]
    else:
        p2 = [[0, 0], [w, 0], [w, h], [0, h]]
    p1, p2 = float32(p1), float32(p2)

    M = getPerspectiveTransform(p1, p2)
    imDst = warpPerspective(imSrc, M, (int(round(w)), int(round(h))))

    return imDst


def perspectiveWH(pointfs: list[QPointF], switch=False):
    '''
    计算透视变换后目标的宽高
    输入原图四个排序好(顺/逆时针)角点的坐标
    取对应边的最大值作宽、高
    '''
    lens = []
    for i in range(4):
        beg = i
        end = (i + 1) % 4
        line = QLineF(pointfs[beg], pointfs[end])
        lens.append(line.length())
    if switch:
        w = max(lens[1], lens[3])
        h = max(lens[0], lens[2])
    else:
        w = max(lens[0], lens[2])
        h = max(lens[1], lens[3])

    return w, h

