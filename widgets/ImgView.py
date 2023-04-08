from numpy import sqrt, abs, cos, sin, arctan, pi, array, rad2deg
from PyQt5 import QtCore, QtGui, QtWidgets
from plugins import AppImg


class ImgView(QtWidgets.QGraphicsView):
    '''
    自编继承自QtWidgets.QGraphicsView的新子类
    用于SubWindow图片的显示
    '''
    def __init__(self, parent, appimgsrc):
        super(ImgView, self).__init__(parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        # 设置背景色
        self.setBackgroundBrush(QtGui.QColor(34, 34, 34))

        # 设置放大缩小时跟随鼠标
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

        self.CVsrc = appimgsrc  # AppImg的CV格式源图片, 初始化SubWindow时传入
        self.CVtemp = appimgsrc  # AppImg的CV格式临时图片, 主要用于dRotate
        self.CVdst = AppImg()  # AppImg的CV格式处理结果图片
        self.imQT = self.CVsrc.CV2Qimg()  # QImage格式图片

        self.scene = QtWidgets.QGraphicsScene()  # 画布
        self.setScene(self.scene)

        self.imItem = ImgPixmapItem(QtGui.QPixmap(self.imQT))  # 画
        self.s_old = QtCore.QSize(self.imItem.pixmap().width(),
                                  self.imItem.pixmap().height())  # ImgView的前一步Size
        self.k_rec = 1  # 记录滚轮放缩系数，用于旋转适应放缩及重置

        self.imItem.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.scene.addItem(self.imItem)

    def resizeEvent(self, event: QtGui.QResizeEvent):
        '''
        重载resizeEvent函数
        调用自编scaleView方法，不记录放缩系数k
        实现图片自适应QGraphicsView窗口大小变化
        '''
        self.scaleView()

    def wheelEvent(self, event: QtGui.QWheelEvent):
        '''
        重载wheelEvent函数
        当检测到鼠标滚轮转动时，放缩画布
        '''
        angle_whell = event.angleDelta().y() / 8

        if angle_whell > 0:
            k = sqrt(1.1)
            self.k_rec *= k
        else:
            k = sqrt(0.9)
            self.k_rec *= k
        self.scale(k, k)

    def resetPixmap(self):
        '''
        自编重设Pixmap函数
        子窗口调用disp后，重新填充图片
        '''
        self.imItem.renderFlag = False
        self.imItem.setPixmap(QtGui.QPixmap(self.imQT))

    def coverPixmap(self):
        '''
        自编覆盖Pixmap函数
        用于画图后覆盖到原图上
        '''
        self.imItem.renderFlag = True
        rectSrc = self.scene.itemsBoundingRect()
        self.imQT = QtGui.QImage(rectSrc.width(), rectSrc.height(), QtGui.QImage.Format_RGB888)
        painter = QtGui.QPainter(self.imQT)
        rectTge = QtCore.QRectF(self.imQT.rect())
        self.scene.render(painter, rectTge, rectSrc)
        self.resetPixmap()

    def scaleView(self):
        '''
        自编放缩View方法/函数
        返回放缩系数k
        '''
        s_new = self.size()  # ImgView的本步Size
        s_new = self.s_old.scaled(s_new, QtCore.Qt.KeepAspectRatio)  # 保持原始图像长宽比不变，本步Size修正
        k_w, k_h = s_new.width() / self.s_old.width(), s_new.height() / self.s_old.height()
        # 理论上放缩系数k在本步Size修正后满足k_w = k_h，但实际有10^-3量级误差
        # 因此选择较大的放缩系数
        k = max(k_w, k_h)
        # print("新:{},旧:{}".format(s_new, self.s_old))
        self.scale(k, k)

        self.s_old = s_new  # 本步Size赋值给上一步

        return k


class ImgPixmapItem(QtWidgets.QGraphicsPixmapItem):
    def __init__(self, pm, parent=None):
        # parent=None语句使得此类仅继承父类，而不继承父类的父类
        # 所以此类不能emit信号，只能在ImgView类中进行
        super(ImgPixmapItem, self).__init__(parent)

        self.setPixmap(pm)
        self.pointf_s = QtCore.QPointF(0.0, 0.0)  # 裁剪框起始点
        self.pointf_e = QtCore.QPointF(
            self.pixmap().width(), self.pixmap().height())  # 裁剪框终止点

        self.AspectRatio = None  # 固定宽高比

        self.pointf_tl = None  # 方框左上(Top Left)角点
        self.pointf_br = None  # 方框右下(Bottom Right)角点

        self.CropBFlag = False  # 裁剪开始(Begin)标识符
        self.CropEFlag = False  # 裁剪完成(End)标识符
        self.MidPressFlag = False  # 中键按下标识符
        self.RightPressFlag = False  # 右键按下标识符

        # 绘图模式标识符
        # 0~裁剪框, 1~标注框, 2~涂鸦, 3~马赛克
        # 4~虚化选择, 5~保留色彩(无绘制操作), 6形变校正, 7~无操作保留
        self.drawMode = 0
        self.renderFlag = False  # 渲染标识符，True表示正在渲染到图片上
        self.text = None
        self.Color = QtGui.QColor('black')
        self.textFont = QtGui.QFont('黑体', 32)
        self.penWidthF = 5
        self.drawShape = 0
        self.map_dir = None  # 贴图文件路径
        self.mosaicSize = 5
        self.blurKSize = 9
        self.pngFlag = False
        self.pointfs = []  # 鼠标按下四个点的点集
        self.pointfSorted = []  # 逆时针排序好的四个点的点集
        self.pspTransformed = False

    def mousePressEvent(self, event: 'QGraphicsSceneMouseEvent'):
        '''
        重载mousePressEvent函数
        记录起始坐标、结束坐标设空，置裁剪结束标识符为假
        判断中键、右键按下，分别置按下标识符
        同时右键按下切换裁剪开始标识符并切换光标
        '''
        super(ImgPixmapItem, self).mousePressEvent(event)
        self.pointf_s = event.pos()
        self.pointf_e = None
        self.pointf_tl, self.pointf_br = None, None
        self.CropEFlag = False

        if event.button() == QtCore.Qt.MouseButton.MidButton:
            self.MidPressFlag = True
            self.update()
        else:
            self.MidPressFlag = False
            self.update()
        
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            if self.CropBFlag:
                self.CropBFlag = False
                self.setCursor(QtCore.Qt.CursorShape.ArrowCursor)  # 箭头光标
            else:
                self.CropBFlag = True
                self.setCursor(QtCore.Qt.CursorShape.CrossCursor)  # 十字光标
            self.RightPressFlag = True
            self.update()
        else:
            self.RightPressFlag = False
            self.update()

    def mouseMoveEvent(self, event: 'QGraphicsSceneMouseEvent'):
        '''
        重载mouseMoveEvent函数
        当右键没按下时：(←该判断始终Deactivate了右键的拖动功能，达到仅将其作开关的目的)
        裁剪没开始可照常拖动，
        或者中键按下始终照常拖动
        '''
        self.pointf_e = event.pos()

        if self.AspectRatio is not None:
            self.keepAspectRatio(self.AspectRatio)

        self.pointf_tl = QtCore.QPointF(min(self.pointf_s.x(), self.pointf_e.x()),
                                        min(self.pointf_s.y(), self.pointf_e.y()))
        self.pointf_br = QtCore.QPointF(max(self.pointf_s.x(), self.pointf_e.x()),
                                        max(self.pointf_s.y(), self.pointf_e.y()))

        if not self.RightPressFlag and (not self.CropBFlag or self.MidPressFlag):
            dx = self.pointf_e.x() - self.pointf_s.x()
            dy = self.pointf_e.y() - self.pointf_s.y()
            self.moveBy(dx, dy)
            self.CropEFlag = False
        self.update()

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent'):
        '''
        重载mouseReleaseEvent函数
        右键/中间抬起时、没有进入绘图模式(十字光标)时清空点集
        反之点集每次增加选中的点，超过4个后清空
        '''
        # print("起点:{},终点:{}".format(self.pointf_s, self.pointf_e))
        # print("左上:{},右下:{}".format(self.pointf_tl, self.pointf_br))
        if self.drawMode == 6:
            if event.button() == QtCore.Qt.MouseButton.LeftButton and self.CropBFlag:
                if len(self.pointfs) >= 4:
                    self.pointfs.clear()
                self.pointfs.append(event.pos())
            else:
                self.pointfs.clear()
                self.pointfSorted.clear()
                self.CropEFlag = False
            self.update()
            # print(self.pointfs)

    def keepAspectRatio(self, AspectRatio):
        '''
        方框终止点限位器函数
        '''
        dx = self.pointf_e.x() - self.pointf_s.x()
        dy = self.pointf_e.y() - self.pointf_s.y()
        if AspectRatio < 1:
            if dx * dy > 0:
                dx = dy * AspectRatio
            else:
                dx = -dy * AspectRatio
            self.pointf_e = QtCore.QPointF(self.pointf_s.x() + dx, self.pointf_e.y())
        else:
            if dx * dy > 0:
                dy = dx / AspectRatio
            else:
                dy = -dx / AspectRatio
            self.pointf_e = QtCore.QPointF(self.pointf_e.x(), self.pointf_s.y() + dy)

    def paint(self, painter, option, widget):
        '''
        重载paint函数
        中键没按、且右键按下一次、且裁剪开始后 画各种图形
        renderFlag的判断使得辅助线/框在渲染后消失
        '''
        super(ImgPixmapItem, self).paint(painter, option, widget)
        if self.CropBFlag and not self.MidPressFlag and not self.RightPressFlag:
            painter.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)

            if self.drawMode == 0:
                pen = QtGui.QPen(QtCore.Qt.PenStyle.DashDotLine)
                pen.setColor(QtGui.QColor(0, 255, 0))  # 绿色点线边框
                self.autoPenWidth()
                pen.setWidthF(self.penWidthF)
                painter.setPen(pen)

                if self.pointf_e:
                    rect_crop = QtCore.QRectF(self.pointf_s, self.pointf_e)
                    painter.drawRect(rect_crop)
                    self.CropEFlag = True

            elif self.drawMode == 1:
                if not self.renderFlag:
                    pen = QtGui.QPen(QtCore.Qt.PenStyle.SolidLine)
                    pen.setColor(QtGui.QColor(0, 255, 0))  # 绿色边框
                    self.autoPenWidth()
                    pen.setWidthF(self.penWidthF)
                    painter.setPen(pen)
                    if self.pointf_e:
                        rect_text = QtCore.QRectF(self.pointf_tl, self.pointf_br)
                        painter.drawRect(rect_text)
                else:
                    self.MidPressFlag = True

                painter.setPen(self.Color)
                painter.setFont(self.textFont)
                if self.pointf_e:
                    rect_text = QtCore.QRectF(self.pointf_tl, self.pointf_br)
                    painter.drawText(rect_text, QtCore.Qt.TextFlag.TextWordWrap, self.text)
                    self.CropEFlag = True

            elif self.drawMode == 2:
                pen = QtGui.QPen(QtCore.Qt.PenStyle.SolidLine)
                pen.setColor(self.Color)
                pen.setWidthF(self.penWidthF)
                pen.setJoinStyle(QtCore.Qt.PenJoinStyle.MiterJoin)
                painter.setPen(pen)

                if self.pointf_e:
                    if self.drawShape == 0:
                        painter.drawLine(self.pointf_s, self.pointf_e)
                    elif self.drawShape == 1:
                        self.drawArrow(painter)
                    elif self.drawShape == 2:
                        self.drawRect(painter)
                    elif self.drawShape == 3:
                        self.drawEllipse(painter)
                    elif self.drawShape == 4:
                        self.drawTriangle(painter)
                    elif self.drawShape == 5:
                        self.drawStar(painter)
                    elif self.drawShape == 6:
                        self.drawRect(painter, fillFlag=True)
                    elif self.drawShape == 7:
                        self.drawEllipse(painter, fillFlag=True)
                    elif self.drawShape == 8:
                        self.drawTriangle(painter, fillFlag=True)
                    elif self.drawShape == 9:
                        self.drawStar(painter, fillFlag=True)
                    elif self.drawShape == 10:
                        self.drawPixmap(painter, ratioFlag=True)
                    elif self.drawShape == 11:
                        self.drawPixmap(painter)
                    self.CropEFlag = True

            elif self.drawMode == 3 or self.drawMode == 4:
                if not self.renderFlag:
                    pen = QtGui.QPen(QtCore.Qt.PenStyle.DashDotLine)
                    pen.setColor(QtGui.QColor(0, 255, 0))  # 绿色点线边框
                    self.autoPenWidth()
                    pen.setWidthF(self.penWidthF)
                    painter.setPen(pen)

                    if self.pointf_e:
                        rect_moblur = QtCore.QRect(self.pointf_tl.toPoint(), self.pointf_br.toPoint())
                        painter.drawRect(rect_moblur)
                        self.CropEFlag = True

            elif self.drawMode == 6:
                pen = QtGui.QPen(QtCore.Qt.PenStyle.SolidLine)
                pen.setColor(QtGui.QColor(0, 255, 0))  # 绿色边框
                self.autoPenWidth()
                pen.setWidthF(self.penWidthF)
                painter.setPen(pen)

                if self.pointfs and not self.pspTransformed:
                    for pointf in self.pointfs:
                        painter.drawEllipse(pointf.x(), pointf.y(),
                                            self.penWidthF, self.penWidthF)
                    if len(self.pointfs) == 4:
                        self.pointfSorted.clear()
                        p1, p2, p3, p4 = self.sort4PointFs(self.pointfs)
                        self.pointfSorted = [p1, p2, p3, p4]
                        painter.drawPolygon(p1, p2, p3, p4)
                        self.CropEFlag = True

            else:
                pass

    def autoPenWidth(self):
        '''
        自动笔刷宽度子函数
        根据图幅自动调整笔刷宽度
        '''
        if self.pixmap().width() > 2560 or self.pixmap().height() > 2560:
            self.penWidthF = 12.8
        elif self.pixmap().width() > 1080 or self.pixmap().height() > 1080:
            self.penWidthF = 5.4
        elif self.pixmap().width() > 480 or self.pixmap().height() > 480:
            self.penWidthF = 2.4
        else:
            self.penWidthF = 0.7

    def drawArrow(self, painter: QtGui.QPainter):
        '''
        画箭头线子函数
        根据直线的单位、法向量得到箭头
        '''
        if self.pointf_e:
            linef = QtCore.QLineF(self.pointf_s, self.pointf_e)
            linef.setLength(linef.length() - self.penWidthF * 1.7)  # 减去箭头长
            vecu = linef.unitVector()  # 该直线单位向量
            vecu.setLength(self.penWidthF * 1.7)
            vecu.translate(linef.dx(), linef.dy())  # 平移到直线终点
            vecn = vecu.normalVector()  # 该平移后单位向量的法向量
            vecn.setLength(self.penWidthF)
            vecnr = vecn.normalVector().normalVector()  # 得到反向法向量
            painter.drawLine(linef)
            painter.setBrush(self.Color)
            painter.drawPolygon(vecu.p2(), vecn.p2(), vecnr.p2())

    def drawRect(self, painter: QtGui.QPainter, fillFlag=False):
        '''
        画矩形子函数
        额外接受填充标识符输入
        '''
        if self.pointf_e:
            if fillFlag:
                painter.setBrush(self.Color)
            rect = QtCore.QRectF(self.pointf_s, self.pointf_e)
            painter.drawRect(rect)

    def drawEllipse(self, painter: QtGui.QPainter, fillFlag=False):
        '''
        画椭圆子函数
        额外接受填充标识符输入
        '''
        if self.pointf_e:
            if fillFlag:
                painter.setBrush(self.Color)
            rect = QtCore.QRectF(self.pointf_s, self.pointf_e)
            painter.drawEllipse(rect)

    def drawTriangle(self, painter: QtGui.QPainter, fillFlag=False):
        '''
        画三角形子函数
        三角形朝向随拖动方向改变
        额外接受填充标识符输入
        '''
        if self.pointf_e:
            if fillFlag:
                painter.setBrush(self.Color)
            dpsex = self.pointf_e.x() - self.pointf_s.x()
            dpsey = self.pointf_e.y() - self.pointf_s.y()
            p3 = self.pointf_e
            if dpsex * dpsey > 0:
                p1 = QtCore.QPointF(self.pointf_s.x(), self.pointf_e.y())
                p2 = QtCore.QPointF((self.pointf_s.x() + self.pointf_e.x()) / 2,
                                    self.pointf_s.y())
            else:
                p1 = QtCore.QPointF(self.pointf_e.x(), self.pointf_s.y())
                p2 = QtCore.QPointF(self.pointf_s.x(),
                                    (self.pointf_s.y() + self.pointf_e.y()) / 2)
            painter.drawPolygon(p1, p2, p3)

    def drawStar(self, painter: QtGui.QPainter, fillFlag=False):
        '''
        画正五角星子函数
        两自由度：半径及方向
        五角星朝向随拖动方向改变
        额外接受填充标识符输入
        '''
        if self.pointf_e:
            if fillFlag:
                painter.setBrush(self.Color)
            linef = QtCore.QLineF(self.pointf_s, self.pointf_e)
            if linef.dx() > 0:
                deg = arctan(linef.dy() / linef.dx()) * 180 / pi
            elif linef.dx() < 0 < linef.dy():
                deg = arctan(linef.dy() / linef.dx()) * 180 / pi + 180
            elif linef.dx() < 0 and linef.dy() < 0:
                deg = arctan(linef.dy() / linef.dx()) * 180 / pi - 180
            elif linef.dx() == 0 and linef.dy() < 0:
                deg = -90
            else:
                deg = 180
            deg = round(deg, 3)
            # print(-deg)  # 形状实际转的角度

            path = QtGui.QPainterPath()
            path.moveTo(self.pointf_s.x() + linef.length(), self.pointf_s.y())
            for i in range(1, 5):
                path.lineTo(self.pointf_s.x() + linef.length() * cos(0.8 * i * pi),
                            self.pointf_s.y() + linef.length() * sin(0.8 * i * pi))
            path.closeSubpath()
            path.setFillRule(QtCore.Qt.FillRule.WindingFill)
            painter.translate(self.pointf_s.x(), self.pointf_s.y())
            painter.rotate(deg)
            painter.translate(-self.pointf_s.x(), -self.pointf_s.y())
            painter.drawPath(path)

    def drawPixmap(self, painter: QtGui.QPainter, ratioFlag=False):
        '''
        贴图子函数
        额外接受贴图宽高比限制标识符输入
        '''
        imQTSrc = QtGui.QImage(self.map_dir)
        rect_I = imQTSrc.rect()
        if self.map_dir:
            if self.pointf_e:
                if ratioFlag:
                    aspectratio = imQTSrc.width() / imQTSrc.height()
                    self.keepAspectRatio(aspectratio)
                    self.pointf_tl = QtCore.QPointF(min(self.pointf_s.x(), self.pointf_e.x()),
                                                    min(self.pointf_s.y(), self.pointf_e.y()))
                    self.pointf_br = QtCore.QPointF(max(self.pointf_s.x(), self.pointf_e.x()),
                                                    max(self.pointf_s.y(), self.pointf_e.y()))
                rect_P = QtCore.QRectF(self.pointf_tl, self.pointf_br)
                rect_P = rect_P.toRect()
                if not self.renderFlag:
                    painter.drawRect(rect_P)
                painter.drawPixmap(rect_P, QtGui.QPixmap(imQTSrc), rect_I)

    def sort4PointFs(self, pointfs: list[QtCore.QPointF]):
        '''
        四边形角点集排序
        输入元素为QPointF类型的list
        输出排序好的顺时针四个QPointF点
        '''
        xfs, yfs = [], []
        for pointf in pointfs:
            xfs.append(pointf.x())
            yfs.append(pointf.y())

        pt_index = yfs.index(min(yfs))  # 最上角点的索引
        pt = pointfs[pt_index]  # 最上角点作原点
        xfs_moved = [x - pt.x() for x in xfs]  # 平移后的x坐标
        yfs_moved = [y - pt.y() for y in yfs]  # 平移后的y坐标
        for x in xfs_moved:
            if x == 0:  # 防止除0
                xfs_moved[xfs_moved.index(x)] += 0.001
        xfs_moved = array(xfs_moved)
        yfs_moved = array(yfs_moved)  # 反正切求辐角
        degs = rad2deg(arctan(yfs_moved/xfs_moved)).tolist()
        for deg in degs:
            if deg < 0:
                degs[degs.index(deg)] = 180 + deg

        degs_tuplelist = list(enumerate(degs))  # 生成[(index, value), (), ...]格式
        degs_tuplelist.sort(key=lambda x: x[1])  # 按角度由小到大排序
        pr = pointfs[degs_tuplelist[1][0]]
        pb = pointfs[degs_tuplelist[2][0]]
        pl = pointfs[degs_tuplelist[3][0]]
        # print(degs_tuplelist)
        # print(pt, pr, pb, pl)
        colineFlag = self.isCoLine(pointfs)
        concaveFlag = self.isConcave([pt, pr, pb, pl])
        if colineFlag or concaveFlag:
            pt = QtCore.QPointF(0, 0)
            pr = QtCore.QPointF(self.pixmap().width(), 0)
            pb = QtCore.QPointF(self.pixmap().width(), self.pixmap().height())
            pl = QtCore.QPointF(0, self.pixmap().height())

        return pt, pr, pb, pl

    def isCoLine(self, pointfs: list[QtCore.QPointF]):
        '''
        三点共线判断
        '''
        flag = False
        # 0,1,2 0,1,3 0,2,3 1,2,3  平面四个点取三点判断共线
        for i in range(len(pointfs)):
            for j in range(i + 1, len(pointfs)):
                for k in range(j + 1, len(pointfs)):
                    x1, y1 = pointfs[i].x(), pointfs[i].y()
                    x2, y2 = pointfs[j].x(), pointfs[j].y()
                    x3, y3 = pointfs[k].x(), pointfs[k].y()
                    area = 0.5 * abs(x1 * y2 + x2 * y3 + x3 * y1
                                     - x1 * y3 - x2 * y1 - x3 * y2)
                    # print(area)
                    if area < 50:
                        flag = True
                        break
                if flag:
                    break
            if flag:
                break

        return flag

    def isConcave(self, pointfs: list[QtCore.QPointF]):
        '''
        凹多边形判断
        注意输入的必须是排序好(顺/逆时针)的点集
        '''
        flag = False
        nums = len(pointfs)
        if nums < 3:  # 多边形至少包含三个顶点
            raise ValueError("多边形至少包含三个顶点！")
        for i in range(nums):
            pre = i
            thi = (i + 1) % nums
            nex = (i + 2) % nums
            line1 = QtCore.QLineF(pointfs[thi], pointfs[pre])
            line2 = QtCore.QLineF(pointfs[thi], pointfs[nex])
            interior_angle = line1.angleTo(line2)
            # print(interior_angle)
            if interior_angle > 180:
                flag = True
                break
        else:
            flag = False

        return flag

