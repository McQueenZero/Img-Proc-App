import datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from numpy import sqrt
from plugins import AppImg


class ImgFrame(QtWidgets.QFrame):
    '''
    自编继承自QtWidgets.QFrame的新子类
    用于MainWindow图片的显示
    '''
    def __init__(self, parent):
        super(ImgFrame, self).__init__(parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setStyleSheet("border-width: 1px;border-style: solid;border-color: rgb(114, 114, 114);")

        self.CV = AppImg()  # AppImg的CV格式图片
        self.dir_img = None  # 路径及文件名，用于删除或保存功能
        self.AdaptedFlag = True  # 图窗自适应标识符，默认缩略图自适应图窗大小
        self.imQT = None  # QImage格式图片
        self.tn = None  # 放入frame图窗显示的经过缩放的图（thumbnail）
        self.x_d, self.y_d = 0, 0  # 绘图起始左上角点
        self.pos_s = None  # 鼠标点击的坐标
        self.MoveFlag = False  # 鼠标移动拖拽图片标识符
        self.scale4tn = 1  # 面积缩放系数，操作QImage结果呈缩略图显示

    def paintEvent(self, event: QtGui.QPaintEvent):  # 绘图事件
        '''
        重载paintEvent函数
        当检测到ImgFrame子类读入图片时，显示到Frame视图上
        '''
        if self.imQT:
            self.scaleImage()
        else:
            self.tn = QtGui.QImage(None)  # 必须是QImage(None)，否则drawImage报错
            self.x_d, self.y_d = 0, 0

        painter = QtGui.QPainter(self)
        painter.begin(self)
        painter.drawImage(self.x_d, self.y_d, self.tn)
        painter.end()

    def wheelEvent(self, event: QtGui.QWheelEvent):  # 鼠标滚轮事件
        '''
        重载wheelEvent函数
        当检测到鼠标滚轮转动时，放缩系数改变并repaint
        '''
        if not self.AdaptedFlag:
            angle_whell = event.angleDelta().y() / 8
            pos_mouse = event.pos()

            if angle_whell > 0 and self.scale4tn <= 7:
                self.scale4tn *= 1.1
                self.x_d -= pos_mouse.x() * self.scale4tn * 0.01
                self.y_d -= pos_mouse.y() * self.scale4tn * 0.01
                # 使图片缩放的效果看起来像是以鼠标所在点为中心进行缩放的
            elif angle_whell < 0 and self.scale4tn >= 0.14:
                self.scale4tn *= 0.9
                self.x_d += pos_mouse.x() * self.scale4tn * 0.01
                self.y_d += pos_mouse.y() * self.scale4tn * 0.01

            self.repaint()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        '''
        重载mousePressEvent函数
        当鼠标点击时记录位置，更新拖动标识符
        '''
        if not self.AdaptedFlag:
            self.pos_s = event.pos()
            self.MoveFlag = True

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
        '''
        重载mouseReleaseEvent函数
        当鼠标释放时更新拖动标识符
        '''
        if not self.AdaptedFlag:
            self.MoveFlag = False

    def mouseMoveEvent(self, event: QtGui.QMouseEvent):
        '''
        重载mouseMoveEvent函数
        当鼠标移动时记录位置变化并repaint
        '''
        if not self.AdaptedFlag and self.MoveFlag:
            # 0.05是比例系数，用于解决拖拽灵敏度过大的问题

            point: QtCore.QPoint = (event.pos() - self.pos_s) * 0.03
            self.x_d += point.x()
            self.y_d += point.y()

            self.repaint()

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent):
        '''
        重载mouseDoubleClickEvent函数
        当鼠标双击时重置绘图起始左上角点和边缩放系数
        '''
        if not self.AdaptedFlag:
            self.x_d, self.y_d = 0, 0
            self.scale4tn = 1

        self.repaint()  # 此语句使得重开AdaptedFlag后，双击即可适应图窗

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent):
        '''
        重载dragEnterEvent函数，从外部拖入图片时触发事件
        注意：hasImage针对从Word中拖入判断，而hasUrls针对从本地资源浏览器中拖入判断
        '''
        if event.mimeData().hasImage() or event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QtGui.QDropEvent):
        '''
        重载dropEvent函数
        从Word中拖入的图片直接QImage转换
        从本地资源浏览器拖入的图片需要先转出LocalFile路径然后打开
        '''
        now = datetime.datetime.now()
        filename = "./InputImages/" + "Drop " + now.strftime("%Y-%m-%d %H-%M-%S") + ".png"

        if event.mimeData().hasImage():
            self.imQT = QtGui.QImage(event.mimeData().imageData())
            self.imQT.save(filename)
        elif event.mimeData().hasUrls():
            self.dir_img = event.mimeData().urls()[0].toLocalFile()
            self.imQT = QtGui.QImage(self.dir_img)
            self.imQT.save(filename)
        self.CV.Q2CVimg(self.imQT)
        self.repaint()

    def scaleImage(self):
        '''
        自编放缩Image方法，根据self.AdaptedFlag的不同分两种情况
        注意：此处的放缩处理的只是显示的缩略图，即为 不可保存的 放缩操作
        '''
        # .scaled()语句确保了图片铺满，并自适应窗口缩放
        # self.size()返回frame或frame_2的大小是QtCore.QSize格式
        # event.rect()返回是绘图事件的目标框大小
        # painter.drawImage第一个参数为角点坐标，或者是方框QtCore.QRect(0, 0, 348, 395)
        # 但这样做会填满，不希望，原比例显示只希望填充一部分，修改起始点x_start和y_start
        if self.AdaptedFlag:
            self.tn = self.imQT.scaled(
                self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.x_d = self.width() / 2 - self.tn.width() / 2
            self.y_d = self.height() / 2 - self.tn.height() / 2
        else:
            self.tn = self.imQT.scaled(
                self.imQT.width() * sqrt(self.scale4tn), self.imQT.height() * sqrt(self.scale4tn),
                QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)




