# -*- coding: utf-8 -*-

import os
from PyQt5 import QtCore, QtGui, QtWidgets
from widgets import ImgFrame
from gui import Ui_SubWindow, Ui_About
from plugins import ipc


class CntFcn:
    '''
    记录某一函数的调用次数
    '''
    def __init__(self, fcn):
        self.calls = 0
        self.fcn = fcn

    def __call__(self, *args, **kwargs):
        self.calls += 1
        self.fcn(*args, **kwargs)
        print("函数{}被调用了{}次".format(self.fcn.__name__, self.calls))


class Ui_MainWindow(QtWidgets.QMainWindow):
    '''
    在designer自动生成的代码
    基础上修改编写
    '''
    def __init__(self, platform):
        super(Ui_MainWindow, self).__init__()
        self.Platform = platform  # 运行平台
        self.InputDir = './InputImages'  # 图像输入路径
        self.OutputDir = './OutputImages'  # 图像输出路径
        self.Clipboard = QtWidgets.QApplication.clipboard()  # 图像剪贴板
        self.scale4CV = 1  # 面积缩放系数，操作CVImage结果可保存
        self.RefreshFlag = True  # 刷新标识符，打开新图片默认结果图窗刷新
        self.ChannelFlag = -1  # 方便红通道开始循环，Channel标识符初始化为-1
        self.RotateFlag = -1  # 方便第一次旋转90°，Rotate标识符初始化为-1
        self.setupUi(self)  # 括号里必须有self

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1600, 900)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout.addWidget(self.pushButton_3, 0, 2, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout.addWidget(self.pushButton_4, 0, 3, 1, 1)

        self.frame = ImgFrame(self.centralwidget)
        self.frame.setObjectName("frame")
        self.gridLayout.addWidget(self.frame, 1, 0, 1, 2)

        self.frame_2 = ImgFrame(self.centralwidget)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout.addWidget(self.frame_2, 1, 2, 1, 2)

        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label_Info")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 2)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 2, 1, 2)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 720, 22))
        self.menubar.setObjectName("menubar")

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")

        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")

        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")

        self.menu_4 = QtWidgets.QMenu(self.menubar)
        self.menu_4.setObjectName("menu_4")

        self.menu_6 = QtWidgets.QMenu(self.menu_4)
        self.menu_6.setObjectName("menu_6")
        self.menu_7 = QtWidgets.QMenu(self.menu_4)
        self.menu_7.setObjectName("menu_7")
        self.menu_8 = QtWidgets.QMenu(self.menu_4)
        self.menu_8.setObjectName("menu_8")

        self.menu_5 = QtWidgets.QMenu(self.menubar)
        self.menu_5.setObjectName("menu_5")

        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")

        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")

        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")

        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")

        self.actionCopy = QtWidgets.QAction(MainWindow)
        self.actionCopy.setObjectName("actionCopy")

        self.actionPaste = QtWidgets.QAction(MainWindow)
        self.actionPaste.setObjectName("actionPaste")

        self.actionBlur = QtWidgets.QAction(MainWindow)
        self.actionBlur.setObjectName("actionBlur")

        self.actionEdge = QtWidgets.QAction(MainWindow)
        self.actionEdge.setObjectName("actionEdge")

        self.actionChannel = QtWidgets.QAction(MainWindow)
        self.actionChannel.setObjectName("actionChannel")

        self.actionSharpen = QtWidgets.QAction(MainWindow)
        self.actionSharpen.setObjectName("actionSharpen")

        self.actionInvert = QtWidgets.QAction(MainWindow)
        self.actionInvert.setObjectName("actionInvert")

        self.actionHisteq = QtWidgets.QAction(MainWindow)
        self.actionHisteq.setObjectName("actionHisteq")

        self.action0_25 = QtWidgets.QAction(MainWindow)
        self.action0_25.setObjectName("action0_5")
        self.action0_5 = QtWidgets.QAction(MainWindow)
        self.action0_5.setObjectName("action0_5")
        self.action0_8 = QtWidgets.QAction(MainWindow)
        self.action0_8.setObjectName("action0_8")
        self.action1_2 = QtWidgets.QAction(MainWindow)
        self.action1_2.setObjectName("action1_2")
        self.action1_5 = QtWidgets.QAction(MainWindow)
        self.action1_5.setObjectName("action1_5")
        self.action2_0 = QtWidgets.QAction(MainWindow)
        self.action2_0.setObjectName("action2_0")

        self.action9_16 = QtWidgets.QAction(MainWindow)
        self.action9_16.setObjectName("action9_16")
        self.action2_3 = QtWidgets.QAction(MainWindow)
        self.action2_3.setObjectName("action2_3")
        self.action3_4 = QtWidgets.QAction(MainWindow)
        self.action3_4.setObjectName("action3_4")
        self.action4_5 = QtWidgets.QAction(MainWindow)
        self.action4_5.setObjectName("action4_5")
        self.action1_1 = QtWidgets.QAction(MainWindow)
        self.action1_1.setObjectName("action1_1")
        self.action5_4 = QtWidgets.QAction(MainWindow)
        self.action5_4.setObjectName("action5_4")
        self.action4_3 = QtWidgets.QAction(MainWindow)
        self.action4_3.setObjectName("action4_3")
        self.action3_2 = QtWidgets.QAction(MainWindow)
        self.action3_2.setObjectName("action3_2")
        self.action16_9 = QtWidgets.QAction(MainWindow)
        self.action16_9.setObjectName("action16_9")

        self.actionHSym = QtWidgets.QAction(MainWindow)
        self.actionHSym.setObjectName("actionHSym")
        self.actionVSym = QtWidgets.QAction(MainWindow)
        self.actionVSym.setObjectName("actionVSym")

        self.actionInterface = QtWidgets.QAction(MainWindow)
        self.actionInterface.setObjectName("actionInterface")

        self.actionRefresh = QtWidgets.QAction(MainWindow)
        self.actionRefresh.setObjectName("actionRefresh")
        self.actionAdapted = QtWidgets.QAction(MainWindow)
        self.actionAdapted.setObjectName("actionAdapted")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")

        self.menu.addAction(self.actionNew)
        self.menu.addAction(self.actionOpen)
        self.menu.addAction(self.actionSave)
        self.menu.addAction(self.actionSave_as)

        self.menu_2.addAction(self.actionPaste)
        self.menu_2.addAction(self.actionCopy)

        self.menu_3.addAction(self.actionBlur)
        self.menu_3.addAction(self.actionEdge)
        self.menu_3.addAction(self.actionChannel)
        self.menu_3.addAction(self.actionSharpen)
        self.menu_3.addAction(self.actionInvert)
        self.menu_3.addAction(self.actionHisteq)

        self.menu_6.addAction(self.action0_25)
        self.menu_6.addAction(self.action0_5)
        self.menu_6.addAction(self.action0_8)
        self.menu_6.addSeparator()
        self.menu_6.addAction(self.action1_2)
        self.menu_6.addAction(self.action1_5)
        self.menu_6.addAction(self.action2_0)

        self.menu_7.addAction(self.action9_16)
        self.menu_7.addAction(self.action2_3)
        self.menu_7.addAction(self.action3_4)
        self.menu_7.addAction(self.action4_5)
        self.menu_7.addSeparator()
        self.menu_7.addAction(self.action1_1)
        self.menu_7.addSeparator()
        self.menu_7.addAction(self.action5_4)
        self.menu_7.addAction(self.action4_3)
        self.menu_7.addAction(self.action3_2)
        self.menu_7.addAction(self.action16_9)

        self.menu_8.addAction(self.actionHSym)
        self.menu_8.addAction(self.actionVSym)

        self.menu_4.addAction(self.menu_6.menuAction())
        self.menu_4.addAction(self.menu_7.menuAction())
        self.menu_4.addAction(self.menu_8.menuAction())
        self.menu_4.addAction(self.actionInterface)

        self.menu_5.addAction(self.actionRefresh)
        self.menu_5.addAction(self.actionAdapted)
        self.menu_5.addAction(self.actionAbout)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menubar.addAction(self.menu_5.menuAction())

        self.connectUi(MainWindow)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "图像处理小工具"))

        self.pushButton.setText(_translate("MainWindow", "放大"))
        self.pushButton.setShortcut(_translate("MainWindow", "Ctrl++"))
        self.pushButton_2.setText(_translate("MainWindow", "缩小"))
        self.pushButton_2.setShortcut(_translate("MainWindow", "Ctrl+-"))
        self.pushButton_3.setText(_translate("MainWindow", "旋转"))
        self.pushButton_3.setShortcut(_translate("MainWindow", "Ctrl+R"))
        self.pushButton_4.setText(_translate("MainWindow", "删除"))
        self.pushButton_4.setShortcut(_translate("MainWindow", "Del"))

        self.label.setText(_translate("MainWindow", "原始图像"))
        self.label_2.setText(_translate("MainWindow", "处理结果"))

        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "编辑"))
        self.menu_3.setTitle(_translate("MainWindow", "图处理"))
        self.menu_4.setTitle(_translate("MainWindow", "域处理"))
        self.menu_6.setTitle(_translate("MainWindow", "放缩"))
        self.menu_7.setTitle(_translate("MainWindow", "裁剪"))
        self.menu_8.setTitle(_translate("MainWindow", "翻转"))
        self.menu_5.setTitle(_translate("MainWindow", "选项"))

        self.actionOpen.setText(_translate("MainWindow", "打开"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))

        self.actionNew.setText(_translate("MainWindow", "新建"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))

        self.actionSave.setText(_translate("MainWindow", "保存"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))

        self.actionSave_as.setText(_translate("MainWindow", "另存为"))
        self.actionSave_as.setShortcut(_translate("MainWindow", "Ctrl+A"))

        self.actionCopy.setText(_translate("MainWindow", "复制图像"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))

        self.actionPaste.setText(_translate("MainWindow", "粘贴图像"))
        self.actionPaste.setShortcut(_translate("MainWindow", "Ctrl+V"))

        self.actionBlur.setText(_translate("MainWindow", "平滑"))
        self.actionEdge.setText(_translate("MainWindow", "边缘提取"))
        self.actionChannel.setText(_translate("MainWindow", "通道提取"))
        self.actionSharpen.setText(_translate("MainWindow", "锐化"))
        self.actionInvert.setText(_translate("MainWindow", "反色"))
        self.actionHisteq.setText(_translate("MainWindow", "直方图均衡化"))

        self.action0_25.setText(_translate("MainWindow", "0.25"))
        self.action0_5.setText(_translate("MainWindow", "0.5"))
        self.action0_8.setText(_translate("MainWindow", "0.8"))
        self.action1_2.setText(_translate("MainWindow", "1.2"))
        self.action1_5.setText(_translate("MainWindow", "1.5"))
        self.action2_0.setText(_translate("MainWindow", "2.0"))

        self.action9_16.setText(_translate("MainWindow", "9:16"))
        self.action2_3.setText(_translate("MainWindow", "2:3"))
        self.action3_4.setText(_translate("MainWindow", "3:4"))
        self.action4_5.setText(_translate("MainWindow", "4:5"))
        self.action1_1.setText(_translate("MainWindow", "1:1"))
        self.action5_4.setText(_translate("MainWindow", "5:4"))
        self.action4_3.setText(_translate("MainWindow", "4:3"))
        self.action3_2.setText(_translate("MainWindow", "3:2"))
        self.action16_9.setText(_translate("MainWindow", "16:9"))

        self.actionHSym.setText(_translate("MainWindow", "水平镜像"))
        self.actionVSym.setText(_translate("MainWindow", "垂直镜像"))

        self.actionInterface.setText(_translate("MainWindow", "交互"))
        self.actionInterface.setShortcut(_translate("MainWindow", "`"))

        self.actionRefresh.setText(_translate("MainWindow", "读入刷新"))
        self.actionRefresh.setShortcut(_translate("MainWindow", "Ctrl+F"))
        self.actionAdapted.setText(_translate("MainWindow", "自适应显示"))
        self.actionAdapted.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionAbout.setText(_translate("MainWindow", "关于"))
        self.actionAbout.setShortcut(_translate("MainWindow", "F12"))

    def connectUi(self, MainWindow):
        '''
        子函数：用于槽函数连接及额外设定
        '''
        self.pushButton.clicked.connect(lambda: self.dzoom(True))
        self.pushButton_2.clicked.connect(lambda: self.dzoom(False))
        self.pushButton_3.clicked.connect(self.rotate)
        self.pushButton_4.clicked.connect(self.delete)

        self.frame.setAcceptDrops(True)  # 原始图窗接收外部拖拽图片
        self.frame_2.setAcceptDrops(False)  # 结果图窗不接收外部拖拽图片

        self.actionOpen.triggered.connect(self.open)
        self.actionNew.triggered.connect(self.new)
        self.actionSave.triggered.connect(self.save)
        self.actionSave_as.triggered.connect(self.save_as)

        self.actionCopy.triggered.connect(self.copy)
        self.actionPaste.triggered.connect(self.paste)

        self.actionBlur.triggered.connect(self.blur)
        self.actionEdge.triggered.connect(self.edge)
        self.actionChannel.triggered.connect(self.channel)
        self.actionSharpen.triggered.connect(self.sharpen)
        self.actionInvert.triggered.connect(self.invert)
        self.actionHisteq.triggered.connect(self.histeq)

        self.action0_25.triggered.connect(lambda: self.zoom(0.25))
        self.action0_5.triggered.connect(lambda: self.zoom(0.5))
        self.action0_8.triggered.connect(lambda: self.zoom(0.8))
        self.action1_2.triggered.connect(lambda: self.zoom(1.2))
        self.action1_5.triggered.connect(lambda: self.zoom(1.5))
        self.action2_0.triggered.connect(lambda: self.zoom(2.0))

        self.action9_16.triggered.connect(lambda: self.crop(9 / 16))
        self.action2_3.triggered.connect(lambda: self.crop(2 / 3))
        self.action3_4.triggered.connect(lambda: self.crop(3 / 4))
        self.action4_5.triggered.connect(lambda: self.crop(4 / 5))
        self.action1_1.triggered.connect(lambda: self.crop(1 / 1))
        self.action5_4.triggered.connect(lambda: self.crop(5 / 4))
        self.action4_3.triggered.connect(lambda: self.crop(4 / 3))
        self.action3_2.triggered.connect(lambda: self.crop(3 / 2))
        self.action16_9.triggered.connect(lambda: self.crop(16 / 9))

        self.actionHSym.triggered.connect(lambda: self.sym(1))
        self.actionVSym.triggered.connect(lambda: self.sym(0))

        self.actionInterface.triggered.connect(lambda: self.iaedit(MainWindow))

        self.actionRefresh.setCheckable(True)
        self.actionRefresh.setChecked(True)
        self.actionRefresh.triggered.connect(self.refresh)

        self.actionAdapted.setCheckable(True)
        self.actionAdapted.setChecked(True)
        self.actionAdapted.triggered.connect(lambda: self.adapted(self.frame))
        self.actionAdapted.triggered.connect(lambda: self.adapted(self.frame_2))

        self.actionAbout.triggered.connect(self.about)

    def open(self):
        '''
        打开文件资源浏览器(Open File Browser)，选择文件；
        以QImage格式打开图片并显示
        '''
        self.frame.dir_img, _filter = \
            QtWidgets.QFileDialog.getOpenFileName(self, '打开', self.InputDir,
                                                  'PNG 文件(*.png);; JPG 文件(*.jpg);; JPEG 文件(*.jpeg);; 所有 文件(*.*)',
                                                  '所有 文件(*.*)')
        self.frame_2.dir_img = None  # 每次打开文件，初始化保存路径及文件名
        if self.frame.dir_img:
            # ext_index = self.frame.dir_img.rfind('.')
            # ext = self.frame.dir_img[ext_index+1:]
            # if ext == 'png':
            #     pass
            self.frame.CV.loadimg(self.frame.dir_img)
            # 发现QtGui.QImage可以直接根据文件名读取图片
            self.frame.imQT = QtGui.QImage(self.frame.dir_img)  # 省去用OPENCV读再转换的一步
            self.frame.repaint()  # 触发绘图事件显示
            if self.RefreshFlag:
                self.frame_2.imQT = None
                self.frame_2.repaint()
        # else:
        #     QtWidgets.QMessageBox.warning(self.centralwidget, 'Error')

    def save(self):
        '''
        保存槽函数，保存路径为空时打开资源浏览器，初始化保存路径
        保存过一次后，再次保存默认覆盖原文件
        '''
        if self.frame_2.CV.img is not None:
            if self.frame_2.dir_img is None or self.frame_2.dir_img == '':
                self.frame_2.dir_img, _filter = \
                    QtWidgets.QFileDialog.getSaveFileName(self, '保存', self.OutputDir,
                                                          'PNG 文件(*.png);; JPG 文件(*.jpg);; JPEG 文件(*.jpeg)',
                                                          'JPG 文件(*.jpg)')
            self.frame_2.CV.saveimg(self.frame_2.dir_img)

    def save_as(self):
        '''
        另存为槽函数
        每次点击都会跳出资源浏览器重新保存
        '''
        if self.frame_2.CV.img is not None:
            filepath, _filter = \
                QtWidgets.QFileDialog.getSaveFileName(self, '保存', self.OutputDir,
                                                      'PNG 文件(*.png);; JPG 文件(*.jpg);; JPEG 文件(*.jpeg)',
                                                      'JPG 文件(*.jpg)')
            self.frame_2.CV.saveimg(filepath)

    def copy(self):
        '''
        复制图像槽函数
        '''
        if self.frame_2.imQT is not None:
            self.Clipboard.setImage(self.frame_2.imQT)

    def paste(self):
        '''
        粘贴图像槽函数
        '''
        self.frame.imQT = self.Clipboard.image()
        self.frame.CV.Q2CVimg(self.frame.imQT)
        self.frame.repaint()

    def new(self):
        '''
        新建MainWindow 图像处理小工具窗口
        '''
        self.NewWindow = Ui_MainWindow(self.Platform)
        self.NewWindow.show()

    def blur(self):
        '''
        平滑滤波槽函数
        '''
        self.frame_2.CV.img = ipc.blur_gauss(self.frame.CV.img)
        self.disp(self.frame_2)

    def edge(self):
        '''
        边缘提取槽函数
        注意要先用高斯滤波平滑去噪，再进行边缘提取效果好
        '''
        self.frame_2.CV.img = ipc.blur_gauss(self.frame.CV.img, (3, 3))
        self.frame_2.CV.img = ipc.edge_sobel(self.frame_2.CV.img)
        self.disp(self.frame_2, GRAYFLAG=True)

    def channel(self):
        '''
        通道提取槽函数
        '''
        if self.ChannelFlag < 2:
            self.ChannelFlag += 1
        else:
            self.ChannelFlag = 0

        if ipc.channel_extract(self.frame.CV.img):
            if self.ChannelFlag % 3 == 0:
                self.frame_2.CV.img, _, _ = ipc.channel_extract(self.frame.CV.img)
            elif self.ChannelFlag % 3 == 1:
                _, self.frame_2.CV.img, _ = ipc.channel_extract(self.frame.CV.img)
            else:
                _, _, self.frame_2.CV.img = ipc.channel_extract(self.frame.CV.img)

        self.disp(self.frame_2)

    def sharpen(self):
        '''
        锐化槽函数
        '''
        self.frame_2.CV.img = ipc.sharpen_laplace(self.frame.CV.img, 0.5)
        self.disp(self.frame_2)

    def invert(self):
        '''
        反色槽函数
        '''
        self.frame_2.CV.img = ipc.invert_color(self.frame.CV.img)
        self.disp(self.frame_2)

    def histeq(self):
        '''
        直方图均衡化槽函数
        '''
        self.frame_2.CV.img = ipc.hist_eq(self.frame.CV.img)
        self.disp(self.frame_2)

    def zoom(self, scale):
        '''
        缩放槽函数，输入缩放系数
        注意：此处的放缩会处理OPENCV源图像，即为 可保存的 放缩操作
        '''
        self.frame_2.CV.img = ipc.zoom_scale(self.frame.CV.img, scale)
        self.disp(self.frame_2)

    def dzoom(self, IFlag=True):
        '''
        按钮缩放槽函数
        用于递增/减缩放系数，调用缩放槽函数
        '''
        if IFlag and self.scale4CV <= 5:
            self.scale4CV *= 1.1
        elif not IFlag and self.scale4CV >= 0.2:
            self.scale4CV *= 0.9

        self.zoom(self.scale4CV)

    def crop(self, ratio):
        '''
        裁剪槽函数
        输入裁剪比例
        '''
        self.frame_2.CV.img = ipc.crop_ar(self.frame.CV.img, ratio)
        self.disp(self.frame_2)

    def sym(self, flipCode):
        '''
        翻转（对称）槽函数
        输入水平还是垂直镜像的标志位
        '''
        self.frame_2.CV.img = ipc.sym_flip(self.frame.CV.img, flipCode)
        self.disp(self.frame_2)

    def rotate(self):
        '''
        旋转槽函数
        '''
        if self.RotateFlag < 3:
            self.RotateFlag += 1
        else:
            self.RotateFlag = 0

        if self.RotateFlag == 3:
            self.frame_2.CV.img = self.frame.CV.img
        else:
            self.frame_2.CV.img = ipc.rotate_cwra(self.frame.CV.img, self.RotateFlag)
        self.disp(self.frame_2)

    def delete(self):
        '''
        删除槽函数
        '''
        if self.frame.dir_img:
            os.remove(self.frame.dir_img)
            self.frame.dir_img = None
        self.frame.imQT, self.frame.CV = None, None
        self.frame.repaint()
        self.frame_2.dir_img, self.frame_2.imQT, self.frame_2.CV = None, None, None
        self.frame_2.repaint()

    def iaedit(self, MainWindow):
        '''
        新建 InterActive Edit 窗口
        '''
        if self.frame.CV.img is not None:
            self.hide()  # 隐藏主窗口
            self.SubWindow = Ui_SubWindow(MainWindow)
            self.SubWindow.show()

    @staticmethod
    def disp(Frame, GRAYFLAG=False):
        '''
        显示刷新静态方法，接收ImgFrame类和灰度转换选项输入
        完成将CV类图片转换成QImage并在输入ImgFrame上显示
        '''
        Frame.imQT = Frame.CV.CV2Qimg(GRAYFLAG)
        Frame.repaint()

    def refresh(self):
        '''
        读入刷新槽函数
        点一下RefreshFlag变一次
        '''
        self.RefreshFlag = False if self.RefreshFlag is True else True

    def adapted(self, Frame):
        '''
        缩略图窗口自适应槽函数
        点一下AdaptedFlag变一次
        '''
        Frame.AdaptedFlag = False if Frame.AdaptedFlag is True else True

    def about(self):
        '''
        关于槽函数
        '''
        self.AboutDialog = Ui_About()
        self.AboutDialog.exec_()

