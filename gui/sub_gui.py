# -*- coding: utf-8 -*-

import os
import sys
from numpy import sin, cos, abs, deg2rad, round, uint8
from PyQt5 import QtCore, QtGui, QtWidgets
from widgets import ImgView
from plugins import AppImg, ipc, defogging, aceRGB
from copy import deepcopy


class Ui_SubWindow(QtWidgets.QWidget):
    '''
    在designer自动生成的代码
    基础上修改编写
    '''
    def __init__(self, MainWindow):
        super(Ui_SubWindow, self).__init__()
        self.MainWindow = MainWindow  # 传入主图窗并作为子图窗一个属性
        self.RotatedFlag = 0  # 旋转标识符，用于解决直角旋转缩放bug
        self.dRotatedFlag = False  # 滑条旋转标识符
        self.deg_old = 0  # 上一步的滑条旋转值，用于调试时计算旋转增量
        self.w_img4view, self.h_img4view = 512, 512  # 缩放到图窗中的图片宽和高，初值任意
        self.ModeFlag = 0  # 模式标识符
        self.AspectRatio = None  # 记录长宽比
        self.Color = QtGui.QColor('black')  # 记录颜色
        if sys.platform.startswith('win'):
            self.Font = QtGui.QFont('黑体', 32)  # 记录字体
        elif sys.platform.startswith('linux'):
            self.Font = QtGui.QFont('Noto Sans CJK SC', 32)  # 记录字体
        self.PenWidthTick = 5  # 记录笔刷粗细刻度
        self.Shape = 0  # 记录形状编号
        self.k_trans = 1  # 校正比例记录
        self.setupUi(self, MainWindow)

    def setupUi(self, SubWindow, MainWindow):
        SubWindow.setObjectName("SubWindow")
        SubWindow.resize(1600, 900)

        self.gridLayout = QtWidgets.QGridLayout(SubWindow)
        self.gridLayout.setObjectName("gridLayout")

        self.horizontalLayout_C1R1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_C1R1.setObjectName("horizontalLayout_C1R1")

        self.pushButton_Clip = QtWidgets.QPushButton(SubWindow)
        self.pushButton_Clip.setObjectName("pushButton_Clip")
        self.horizontalLayout_C1R1.addWidget(self.pushButton_Clip)

        self.pushButton_Filter = QtWidgets.QPushButton(SubWindow)
        self.pushButton_Filter.setObjectName("pushButton_Filter")
        self.horizontalLayout_C1R1.addWidget(self.pushButton_Filter)

        self.pushButton_Adjust = QtWidgets.QPushButton(SubWindow)
        self.pushButton_Adjust.setObjectName("pushButton_Adjust")
        self.horizontalLayout_C1R1.addWidget(self.pushButton_Adjust)

        self.pushButton_More = QtWidgets.QPushButton(SubWindow)
        self.pushButton_More.setObjectName("pushButton_More")
        self.horizontalLayout_C1R1.addWidget(self.pushButton_More)

        self.gridLayout.addLayout(self.horizontalLayout_C1R1, 0, 0, 1, 2)

        self.graphicsView = ImgView(SubWindow, MainWindow.frame.CV)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 1, 0, 1, 1)

        self.verticalLayout_C2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_C2.setObjectName("verticalLayout_C2")

        self.horizontalLayout_C2R1 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_C2R1.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_C2R1.setObjectName("horizontalLayout_C2R1")

        self.label_Function = QtWidgets.QLabel(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Function.sizePolicy().hasHeightForWidth())
        self.label_Function.setSizePolicy(sizePolicy)
        self.label_Function.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_Function.setObjectName("label_Function")
        self.horizontalLayout_C2R1.addWidget(self.label_Function)

        self.label_Num = QtWidgets.QLabel(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Num.sizePolicy().hasHeightForWidth())
        self.label_Num.setSizePolicy(sizePolicy)
        self.label_Num.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Num.setObjectName("label_Num")
        self.horizontalLayout_C2R1.addWidget(self.label_Num)

        self.label_Unit = QtWidgets.QLabel(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_Unit.sizePolicy().hasHeightForWidth())
        self.label_Unit.setSizePolicy(sizePolicy)
        self.label_Unit.setObjectName("label_Unit")
        self.horizontalLayout_C2R1.addWidget(self.label_Unit)

        self.verticalLayout_C2.addLayout(self.horizontalLayout_C2R1)

        self.horizontalSlider = QtWidgets.QSlider(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSlider.sizePolicy().hasHeightForWidth())
        self.horizontalSlider.setSizePolicy(sizePolicy)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout_C2.addWidget(self.horizontalSlider)

        self.horizontalLayout_C2R3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_C2R3.setObjectName("horizontalLayout_C2R3")

        self.pushButton_F1 = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_F1.sizePolicy().hasHeightForWidth())
        self.pushButton_F1.setSizePolicy(sizePolicy)
        self.pushButton_F1.setObjectName("pushButton_F1")
        self.horizontalLayout_C2R3.addWidget(self.pushButton_F1)

        self.pushButton_F2 = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_F2.sizePolicy().hasHeightForWidth())
        self.pushButton_F2.setSizePolicy(sizePolicy)
        self.pushButton_F2.setObjectName("pushButton_F2")
        self.horizontalLayout_C2R3.addWidget(self.pushButton_F2)

        self.verticalLayout_C2.addLayout(self.horizontalLayout_C2R3)

        self.textEdit = QtWidgets.QTextEdit(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.textEdit.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_C2.addWidget(self.textEdit)

        self.comboBox = QtWidgets.QComboBox(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        self.comboBox.setSizePolicy(sizePolicy)
        self.comboBox.setObjectName("comboBox")
        self.verticalLayout_C2.addWidget(self.comboBox)

        self.gridLayout_C2R6 = QtWidgets.QGridLayout()
        self.gridLayout_C2R6.setObjectName("gridLayout_C2R6")

        self.pushButton_1 = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_1.sizePolicy().hasHeightForWidth())
        self.pushButton_1.setSizePolicy(sizePolicy)
        self.pushButton_1.setObjectName("pushButton_1")
        self.gridLayout_C2R6.addWidget(self.pushButton_1, 0, 0, 1, 1)

        self.pushButton_2 = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_C2R6.addWidget(self.pushButton_2, 0, 1, 1, 1)

        self.pushButton_3 = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_C2R6.addWidget(self.pushButton_3, 1, 0, 1, 1)

        self.pushButton_4 = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_C2R6.addWidget(self.pushButton_4, 1, 1, 1, 1)

        self.pushButton_5 = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(sizePolicy)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_C2R6.addWidget(self.pushButton_5, 2, 0, 1, 1)

        self.pushButton_6 = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6.sizePolicy().hasHeightForWidth())
        self.pushButton_6.setSizePolicy(sizePolicy)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_C2R6.addWidget(self.pushButton_6, 2, 1, 1, 1)

        self.pushButton_Apply = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Apply.sizePolicy().hasHeightForWidth())
        self.pushButton_Apply.setSizePolicy(sizePolicy)
        self.pushButton_Apply.setObjectName("pushButton_Apply")
        self.gridLayout_C2R6.addWidget(self.pushButton_Apply, 3, 0, 1, 1)

        self.pushButton_Import = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Import.sizePolicy().hasHeightForWidth())
        self.pushButton_Import.setSizePolicy(sizePolicy)
        self.pushButton_Import.setObjectName("pushButton_Import")
        self.gridLayout_C2R6.addWidget(self.pushButton_Import, 3, 1, 1, 1)

        self.verticalLayout_C2.addLayout(self.gridLayout_C2R6)

        self.pushButton_Reset = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Reset.sizePolicy().hasHeightForWidth())
        self.pushButton_Reset.setSizePolicy(sizePolicy)
        self.pushButton_Reset.setObjectName("pushButton_Reset")
        self.verticalLayout_C2.addWidget(self.pushButton_Reset)

        self.pushButton_Compare = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Compare.sizePolicy().hasHeightForWidth())
        self.pushButton_Compare.setSizePolicy(sizePolicy)
        self.pushButton_Compare.setObjectName("pushButton_Compare")
        self.verticalLayout_C2.addWidget(self.pushButton_Compare)

        self.horizontalLayout_C2R9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_C2R9.setObjectName("horizontalLayout_C2R9")

        self.pushButton_Save = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Save.sizePolicy().hasHeightForWidth())
        self.pushButton_Save.setSizePolicy(sizePolicy)
        self.pushButton_Save.setObjectName("pushButton_Save")
        self.horizontalLayout_C2R9.addWidget(self.pushButton_Save)

        self.pushButton_Cancel = QtWidgets.QPushButton(SubWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Cancel.sizePolicy().hasHeightForWidth())
        self.pushButton_Cancel.setSizePolicy(sizePolicy)
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.horizontalLayout_C2R9.addWidget(self.pushButton_Cancel)

        self.verticalLayout_C2.addLayout(self.horizontalLayout_C2R9)
        self.gridLayout.addLayout(self.verticalLayout_C2, 1, 1, 1, 1)

        self.connectSubUi(SubWindow)
        self.connectClipUi()
        QtCore.QMetaObject.connectSlotsByName(SubWindow)

    def connectSubUi(self, SubWindow):
        self.pushButton_Clip.setEnabled(False)

        self.pushButton_Clip.clicked.connect(lambda: self.switch(self.pushButton_Clip.objectName()))
        self.pushButton_Filter.clicked.connect(lambda: self.switch(self.pushButton_Filter.objectName()))
        self.pushButton_Adjust.clicked.connect(lambda: self.switch(self.pushButton_Adjust.objectName()))
        self.pushButton_More.clicked.connect(lambda: self.switch(self.pushButton_More.objectName()))

        self.pushButton_1.setCheckable(True)
        self.pushButton_2.setCheckable(True)
        self.pushButton_3.setCheckable(True)
        self.pushButton_4.setCheckable(True)
        self.pushButton_5.setCheckable(True)
        self.pushButton_6.setCheckable(True)

        self.pushButton_Apply.clicked.connect(self.apply)
        self.pushButton_Import.clicked.connect(self.open)

        self.pushButton_Reset.clicked.connect(self.reset)
        self.pushButton_Compare.pressed.connect(lambda: self.compare(pressed=True))
        self.pushButton_Compare.released.connect(lambda: self.compare(pressed=False))

        self.pushButton_Save.clicked.connect(self.save)
        self.pushButton_Cancel.clicked.connect(self.cancel)

        self.retranslateSubUi(SubWindow)

    def retranslateSubUi(self, SubWindow):
        _translate = QtCore.QCoreApplication.translate
        SubWindow.setWindowTitle(_translate("SubWindow", "交互编辑"))

        self.pushButton_Clip.setText(_translate("SubWindow", "修剪"))
        self.pushButton_Clip.setShortcut(_translate("MainWindow", "F1"))
        self.pushButton_Filter.setText(_translate("SubWindow", "滤镜"))
        self.pushButton_Filter.setShortcut(_translate("MainWindow", "F2"))
        self.pushButton_Adjust.setText(_translate("SubWindow", "调节"))
        self.pushButton_Adjust.setShortcut(_translate("MainWindow", "F3"))
        self.pushButton_More.setText(_translate("SubWindow", "更多"))
        self.pushButton_More.setShortcut(_translate("MainWindow", "F4"))

        self.pushButton_Apply.setText(_translate("SubWindow", "应用"))
        self.pushButton_Apply.setShortcut(_translate("MainWindow", "A"))
        self.pushButton_Import.setText(_translate("SubWindow", "导入"))
        self.pushButton_Import.setShortcut(_translate("MainWindow", "Backspace"))

        self.pushButton_Reset.setText(_translate("SubWindow", "重置"))
        self.pushButton_Reset.setShortcut(_translate("MainWindow", "`"))
        self.pushButton_Compare.setText(_translate("SubWindow", "对比"))

        self.pushButton_Save.setText(_translate("SubWindow", "保存"))
        self.pushButton_Save.setShortcut(_translate("MainWindow", "S"))
        self.pushButton_Cancel.setText(_translate("SubWindow", "取消"))
        self.pushButton_Cancel.setShortcut(_translate("MainWindow", "Esc"))

    def connectClipUi(self):
        self.disconnectModeUi()
        self.ModeFlag = 0
        self.graphicsView.imItem.drawMode = 0
        self.label_Num.setPalette(self.palette())
        self.label_Unit.show()

        self.horizontalSlider.setMinimum(-45)
        self.horizontalSlider.setMaximum(45)
        self.horizontalSlider.setTickInterval(5)
        self.horizontalSlider.setValue(-self.deg_old)
        self.label_Num.setNum(self.deg_old)
        self.horizontalSlider.setEnabled(True)
        self.horizontalSlider.valueChanged.connect(
            lambda: self.label_Num.setNum(-self.horizontalSlider.value()))
        self.horizontalSlider.valueChanged.connect(
            lambda: self.drotate(-self.horizontalSlider.value()))

        self.pushButton_F1.show()
        self.pushButton_F1.setCheckable(False)
        self.pushButton_F1.setEnabled(True)
        self.pushButton_F1.clicked.connect(self.rotate)
        self.pushButton_F2.show()
        self.pushButton_F2.setCheckable(False)
        self.pushButton_F2.setEnabled(True)
        self.pushButton_F2.clicked.connect(lambda: self.sym(1))
        if self.horizontalSlider.value() == 0:
            self.pushButton_F1.setEnabled(True)
            self.pushButton_F2.setEnabled(True)

        self.textEdit.show()
        self.textEdit.setEnabled(True)
        self.textEdit.textChanged.connect(self.aspectratioset)
        self.comboBox.hide()

        FcnObjs = [self.pushButton_1, self.pushButton_2, self.pushButton_3,
                   self.pushButton_4, self.pushButton_5, self.pushButton_6]
        for FcnObj in FcnObjs:
            FcnObj.clicked.connect(self.switch6b)
            FcnObj.clicked.connect(self.clip)

        self.pushButton_Apply.setEnabled(False)
        self.pushButton_Import.setEnabled(True)
        self.pushButton_Compare.hide()

        self.retranslateClipUi()

    def retranslateClipUi(self):
        _translate = QtCore.QCoreApplication.translate

        self.label_Function.setText(_translate("SubWindow", "拉伸"))
        self.label_Unit.setText(_translate("SubWindow", "°"))

        self.pushButton_F1.setText(_translate("SubWindow", "旋转"))
        self.pushButton_F2.setText(_translate("SubWindow", "镜像"))

        self.pushButton_1.setText(_translate("SubWindow", "原始"))
        self.pushButton_2.setText(_translate("SubWindow", "1:1"))
        self.pushButton_3.setText(_translate("SubWindow", "16:9"))
        self.pushButton_4.setText(_translate("SubWindow", "9:16"))
        self.pushButton_5.setText(_translate("SubWindow", "4:3"))
        self.pushButton_6.setText(_translate("SubWindow", "3:4"))

    def connectFilterUi(self):
        self.disconnectModeUi()
        self.ModeFlag = 1
        self.graphicsView.imItem.drawMode = 0
        self.label_Num.setPalette(self.palette())
        self.label_Unit.hide()

        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setValue(5)
        self.label_Num.setNum(5)
        self.horizontalSlider.setEnabled(False)

        self.pushButton_F1.hide()
        self.pushButton_F2.hide()
        self.textEdit.hide()
        self.comboBox.hide()

        FcnObjs = [self.pushButton_1, self.pushButton_2, self.pushButton_3,
                   self.pushButton_4, self.pushButton_5, self.pushButton_6]
        for FcnObj in FcnObjs:
            FcnObj.clicked.connect(self.switch6b)
            FcnObj.clicked.connect(self.filter)

        self.pushButton_Apply.setEnabled(False)
        self.pushButton_Import.setEnabled(True)
        self.pushButton_Compare.show()

        self.retranslateFilterUi()

    def retranslateFilterUi(self):
        _translate = QtCore.QCoreApplication.translate

        self.label_Function.setText(_translate("SubWindow", "滤镜强度"))

        self.pushButton_1.setText(_translate("SubWindow", "反色"))
        self.pushButton_2.setText(_translate("SubWindow", "除雾"))
        self.pushButton_3.setText(_translate("SubWindow", "直方图均衡化"))
        self.pushButton_4.setText(_translate("SubWindow", "自动色彩均衡"))
        self.pushButton_5.setText(_translate("SubWindow", "灰度"))
        self.pushButton_6.setText(_translate("SubWindow", "增强锐化"))

    def connectAdjustUi(self):
        self.disconnectModeUi()
        self.ModeFlag = 2
        self.graphicsView.imItem.drawMode = 0
        self.label_Num.setPalette(self.palette())
        self.label_Unit.hide()

        self.horizontalSlider.setMinimum(-10)
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setValue(0)
        self.label_Num.setNum(0)
        self.horizontalSlider.setEnabled(False)

        self.pushButton_F1.hide()
        self.pushButton_F2.hide()
        self.textEdit.hide()
        self.comboBox.hide()

        FcnObjs = [self.pushButton_1, self.pushButton_2, self.pushButton_3,
                   self.pushButton_4, self.pushButton_5, self.pushButton_6]
        for FcnObj in FcnObjs:
            FcnObj.clicked.connect(self.switch6b)
            FcnObj.clicked.connect(self.adjust)

        self.pushButton_Apply.setEnabled(False)
        self.pushButton_Import.setEnabled(True)
        self.pushButton_Compare.show()

        self.retranslateAdjustUi()

    def retranslateAdjustUi(self):
        _translate = QtCore.QCoreApplication.translate

        self.label_Function.setText(_translate("SubWindow", "调节量"))

        self.pushButton_1.setText(_translate("SubWindow", "亮度"))
        self.pushButton_2.setText(_translate("SubWindow", "对比度"))
        self.pushButton_3.setText(_translate("SubWindow", "饱和度"))
        self.pushButton_4.setText(_translate("SubWindow", "锐度"))
        self.pushButton_5.setText(_translate("SubWindow", "亮部"))
        self.pushButton_6.setText(_translate("SubWindow", "暗部"))

    def connectMoreUi(self):
        self.disconnectModeUi()
        self.ModeFlag = 3
        self.graphicsView.imItem.drawMode = 7
        self.label_Num.setPalette(self.palette())
        self.label_Unit.show()

        self.horizontalSlider.setMinimum(0)
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setTickInterval(1)
        self.horizontalSlider.setValue(0)
        self.label_Num.setNum(0)
        self.horizontalSlider.setEnabled(False)

        self.pushButton_F1.show()
        self.pushButton_F1.setEnabled(False)
        self.pushButton_F1.setCheckable(False)
        self.pushButton_F2.show()
        self.pushButton_F2.setEnabled(False)
        self.pushButton_F2.setCheckable(False)
        self.textEdit.show()
        self.textEdit.setEnabled(False)
        self.comboBox.show()
        self.comboBox.setEnabled(False)

        FcnObjs = [self.pushButton_1, self.pushButton_2, self.pushButton_3,
                   self.pushButton_4, self.pushButton_5, self.pushButton_6]
        for FcnObj in FcnObjs:
            FcnObj.clicked.connect(self.switch6b)
            FcnObj.clicked.connect(self.more)

        self.pushButton_Apply.setEnabled(False)
        self.pushButton_Import.setEnabled(True)
        self.pushButton_Compare.show()

        self.retranslateMoreUi()

    def retranslateMoreUi(self):
        _translate = QtCore.QCoreApplication.translate

        self.label_Function.setText(_translate("SubWindow", "选择"))
        self.label_Num.setText(_translate("SubWindow", "        "))
        self.label_Unit.setText(_translate("SubWindow", "格式"))

        self.pushButton_F1.setText(_translate("SubWindow", "更多"))
        self.pushButton_F2.setText(_translate("SubWindow", "更多"))

        self.pushButton_1.setText(_translate("SubWindow", "标注"))
        self.pushButton_2.setText(_translate("SubWindow", "涂鸦"))
        self.pushButton_3.setText(_translate("SubWindow", "马赛克"))
        self.pushButton_4.setText(_translate("SubWindow", "虚化"))
        self.pushButton_5.setText(_translate("SubWindow", "保留色彩"))
        self.pushButton_6.setText(_translate("SubWindow", "形变校正"))

    def disconnectModeUi(self):
        UiObjects = [self.horizontalSlider, self.pushButton_F1, self.pushButton_F2,
                     self.textEdit, self.comboBox, self.pushButton_1, self.pushButton_2,
                     self.pushButton_3, self.pushButton_4, self.pushButton_5, self.pushButton_6]
        for UiObject in UiObjects:
            try:
                UiObject.disconnect()
            except TypeError:
                print('No {} Reused Signal Connect!'.format(UiObject.objectName()))
            else:
                print('{} Reused Signal Disconnected!'.format(UiObject.objectName()))

    def switch(self, ModeObjName):
        FcnObjs = [self.pushButton_1, self.pushButton_2, self.pushButton_3,
                   self.pushButton_4, self.pushButton_5, self.pushButton_6]
        for FcnObj in FcnObjs:
            FcnObj.setChecked(False)
            FcnObj.setEnabled(True)

        if ModeObjName == self.pushButton_Clip.objectName():
            self.pushButton_Clip.setEnabled(False)
            self.pushButton_Clip.setChecked(False)
            self.pushButton_Filter.setEnabled(True)
            self.pushButton_Adjust.setEnabled(True)
            self.pushButton_More.setEnabled(True)
            self.connectClipUi()
        elif ModeObjName == self.pushButton_Filter.objectName():
            self.pushButton_Filter.setEnabled(False)
            self.pushButton_Filter.setChecked(False)
            self.pushButton_Clip.setEnabled(True)
            self.pushButton_Adjust.setEnabled(True)
            self.pushButton_More.setEnabled(True)
            self.connectFilterUi()
        elif ModeObjName == self.pushButton_Adjust.objectName():
            self.pushButton_Adjust.setEnabled(False)
            self.pushButton_Adjust.setChecked(False)
            self.pushButton_Clip.setEnabled(True)
            self.pushButton_Filter.setEnabled(True)
            self.pushButton_More.setEnabled(True)
            self.connectAdjustUi()
        elif ModeObjName == self.pushButton_More.objectName():
            self.pushButton_More.setEnabled(False)
            self.pushButton_More.setChecked(False)
            self.pushButton_Clip.setEnabled(True)
            self.pushButton_Filter.setEnabled(True)
            self.pushButton_Adjust.setEnabled(True)
            self.connectMoreUi()

    def switch6b(self):
        FcnObjs = [self.pushButton_1, self.pushButton_2, self.pushButton_3,
                   self.pushButton_4, self.pushButton_5, self.pushButton_6]
        for FcnObj in FcnObjs:
            if FcnObj.isChecked():
                for i in range(len(FcnObjs)):
                    if i != FcnObjs.index(FcnObj):
                        FcnObjs[i].setEnabled(False)
                break
        else:
            for FcnObj in FcnObjs:
                FcnObj.setEnabled(True)

    def fcnlinkreset(self):
        '''
        重设与Fcn按键相关的
        滑条、F1/F2键、textEdit、comboBox的enabled等属性
        通过filter、adjust、more槽函数实现
        '''
        if self.ModeFlag == 0:
            self.horizontalSlider.setValue(0)
            self.clip()
        elif self.ModeFlag == 1:
            self.horizontalSlider.setValue(5)
            self.filter()
        elif self.ModeFlag == 2:
            self.horizontalSlider.setValue(0)
            self.adjust()
        else:
            # 此处不用再重设滑条值，否则会触发颜色信号
            self.more()

    def save(self):
        '''
        保存(另存为)槽函数
        每次点击都会跳出资源浏览器重新保存
        '''
        point_tl = self.graphicsView.imItem.pointf_tl
        point_br = self.graphicsView.imItem.pointf_br

        if point_tl is None or point_br is None or self.ModeFlag == 3:
            rect_crop = self.graphicsView.imItem.pixmap().rect()
        else:
            point_tl = point_tl.toPoint()
            point_br = point_br.toPoint()
            rect_crop = QtCore.QRect(point_tl, point_br)

        pixmap_crop = self.graphicsView.imItem.pixmap().copy(rect_crop)

        if self.graphicsView.imItem.pngFlag:
            filepath, _filter = \
                QtWidgets.QFileDialog.getSaveFileName(self, '保存', self.MainWindow.OutputDir, 'PNG 文件(*.png)')
            self.MainWindow.OutputDir = filepath
        else:
            if self.MainWindow.filename:
                _, ext = os.path.splitext(self.MainWindow.filename)
                if ext == ".jpeg":
                    ext_str = 'JPEG 文件(*.jpeg)'
                elif ext == ".png":
                    ext_str = 'PNG 文件(*.png)'
                else:
                    ext_str = 'JPG 文件(*.jpg)'
            else:
                ext_str = '所有 文件(*.*)'
            filepath, _filter = \
                QtWidgets.QFileDialog.getSaveFileName(self, '保存', self.MainWindow.OutputDir,
                                                      'PNG 文件(*.png);; JPG 文件(*.jpg);; JPEG 文件(*.jpeg)',
                                                      ext_str)
            self.MainWindow.OutputDir = filepath
        pixmap_crop.save(filepath)

    def cancel(self):
        '''
        取消槽函数
        点击后取消操作并关闭图窗
        '''
        self.close()
        self.MainWindow.show()

    def closeEvent(self, event: QtGui.QCloseEvent):
        '''
        重载closeEvent函数
        针对右上角×关闭，快捷键Alt+F4关闭子图窗的情况
        重新显示主图窗
        '''
        self.MainWindow.show()

    def reset(self):
        '''
        重置槽函数
        点击后重置滚轮/旋转/形变校正缩放并重置系数
        注意：当图片处于直角旋转状态1、3时，再调用一次drotate、rotate槽函数
        '''
        if self.RotatedFlag % 2 == 1:
            self.drotate(0)  # 针对按钮旋转→滑条旋转→重置 缩放失调bug
            self.rotate()  # 针对按钮旋转→重置→按钮旋转 缩放失调bug
        self.RotatedFlag = 0

        k_reciprocal = 1 / (self.graphicsView.k_rec * self.k_trans)  # 滚轮、校正缩放系数记录值的倒数
        self.graphicsView.scale(k_reciprocal, k_reciprocal)
        self.graphicsView.k_rec = 1
        self.k_trans = 1

        self.disp(DSTFLAG=0)

        self.graphicsView.imItem.setPos(0, 0)  # 重设场景位置及矩形范围
        self.graphicsView.scene.setSceneRect(self.graphicsView.imItem.boundingRect())

        self.graphicsView.CVdst.img = None
        self.graphicsView.imItem.MidPressFlag = True

        self.pushButton_1.setChecked(False)
        self.pushButton_2.setChecked(False)
        self.pushButton_3.setChecked(False)
        self.pushButton_4.setChecked(False)
        self.pushButton_5.setChecked(False)
        self.pushButton_6.setChecked(False)

        self.fcnlinkreset()
        self.switch6b()

    def clip(self):
        '''
        裁剪槽函数
        用于传送固定宽高比
        '''
        if self.pushButton_1.isChecked():
            self.textEdit.setEnabled(False)
            self.aspectratioset(self.graphicsView.imItem.pixmap().width() / self.graphicsView.imItem.pixmap().height())
        elif self.pushButton_2.isChecked():
            self.textEdit.setEnabled(False)
            self.aspectratioset(1)
        elif self.pushButton_3.isChecked():
            self.textEdit.setEnabled(False)
            self.aspectratioset(16 / 9)
        elif self.pushButton_4.isChecked():
            self.textEdit.setEnabled(False)
            self.aspectratioset(9 / 16)
        elif self.pushButton_5.isChecked():
            self.textEdit.setEnabled(False)
            self.aspectratioset(4 / 3)
        elif self.pushButton_6.isChecked():
            self.textEdit.setEnabled(False)
            self.aspectratioset(3 / 4)
        else:
            self.textEdit.setEnabled(True)
            self.aspectratioset()

    def rotate(self):
        '''
        顺时针90°旋转槽函数
        '''
        imTemp = self.graphicsView.CVtemp.img
        imDst = self.graphicsView.CVdst.img
        if imDst is None:
            self.graphicsView.CVdst.img = ipc.rotate_cwra(imTemp, 0)
        else:
            self.graphicsView.CVdst.img = ipc.rotate_cwra(imDst, 0)

        self.disp()

        # 直角旋转，宽高互换
        self.graphicsView.s_old = QtCore.QSize(
            self.graphicsView.s_old.height(), self.graphicsView.s_old.width())

        if self.RotatedFlag > 2:
            self.RotatedFlag = 0
        else:
            self.RotatedFlag += 1

        self.graphicsView.scaleView()

        # 重设场景矩形范围，否则旋转后的不在场景正中心
        self.graphicsView.scene.setSceneRect(self.graphicsView.imItem.boundingRect())

    def drotate(self, deg):
        '''
        滑条旋转槽函数
        '''
        imTemp = self.graphicsView.CVtemp.img
        self.graphicsView.CVdst.img = ipc.rotate_deg(imTemp, deg)

        self.disp(CACHEFLAG=False)

        # 旋转自适应放缩
        # ddeg = deg - self.deg_old
        if self.dRotatedFlag is False:
            self.w_img4view, self.h_img4view = self.graphicsView.s_old.width(), self.graphicsView.s_old.height()
            # w_old = self.h_img4view * abs(sin(deg2rad(deg - ddeg))) + self.w_img4view * cos(deg2rad(deg - ddeg))
            # h_old = self.h_img4view * cos(deg2rad(deg - ddeg)) + self.w_img4view * abs(sin(deg2rad(deg - ddeg)))
        else:
            # w_old, h_old = self.graphicsView.s_old.width(), self.graphicsView.s_old.height()
            pass
        w_new = self.h_img4view * abs(sin(deg2rad(deg))) + self.w_img4view * cos(deg2rad(deg))
        h_new = self.h_img4view * cos(deg2rad(deg)) + self.w_img4view * abs(sin(deg2rad(deg)))

        # print('NEW:', w_new, h_new, 'OLD:', w_old, h_old)
        self.graphicsView.s_old = QtCore.QSize(round(w_new * self.graphicsView.k_rec),
                                               round(h_new * self.graphicsView.k_rec))
        # print('k_rec:', self.graphicsView.k_rec)
        # 因为需要迭代，所以记录放缩系数k
        self.graphicsView.k_rec *= self.graphicsView.scaleView()

        # 重设场景矩形范围，否则旋转后的不在场景正中心
        self.graphicsView.scene.setSceneRect(self.graphicsView.imItem.boundingRect())

        self.deg_old = deg  # 本步角度赋给上一步

        if deg != 0:
            self.pushButton_F2.setEnabled(False)
            self.pushButton_F1.setEnabled(False)
            self.pushButton_Import.setEnabled(False)
            self.dRotatedFlag = True
        else:
            self.pushButton_F2.setEnabled(True)
            self.pushButton_F1.setEnabled(True)
            self.pushButton_Import.setEnabled(True)
            self.dRotatedFlag = False

    def sym(self, flipCode):
        '''
        翻转（对称）槽函数
        输入水平还是垂直镜像的标志位
        '''
        imTemp = self.graphicsView.CVtemp.img
        imDst = self.graphicsView.CVdst.img
        # 加入该判断实现每次点击都能镜像翻转
        if imDst is None:
            self.graphicsView.CVdst.img = ipc.sym_flip(imTemp, flipCode)
        else:
            self.graphicsView.CVdst.img = ipc.sym_flip(imDst, flipCode)

        self.disp()

    def aspectratioset(self, ar=None):
        '''
        设置长宽比率槽函数
        '''
        if ar is None:
            input_str = self.textEdit.toPlainText()
            if ':' in input_str:
                input_list = input_str.split(':')

                if len(input_list) != 2:
                    self.textEdit.setText("格式错误！提示：先输入全部数字，后输入冒号")
                    self.graphicsView.imItem.AspectRatio = ar
                    self.AspectRatio = ar
                    return

                try:
                    width = int(input_list[0])
                    height = int(input_list[1])
                except ValueError:
                    self.textEdit.setText("格式错误！提示：先输入全部数字，后输入冒号")
                    self.graphicsView.imItem.AspectRatio = ar
                    self.AspectRatio = ar
                    return

                if width < 0 or height <= 0:
                    self.textEdit.setText("格式错误！提示：先输入全部数字，后输入冒号")
                    self.graphicsView.imItem.AspectRatio = ar
                    self.AspectRatio = ar
                    return

                ar = width / height

        self.graphicsView.imItem.AspectRatio = ar
        self.AspectRatio = ar

    def filter(self):
        '''
        滤镜槽函数
        用于切换到特定的槽函数
        '''
        try:
            self.horizontalSlider.disconnect()
        except TypeError:
            print('No Slider Reused Signal Connect!')
        else:
            print('Slider Reused Signal Disconnected!')

        self.pushButton_Apply.setEnabled(True)

        if self.pushButton_1.isChecked():
            self.horizontalSlider.setEnabled(False)
            self.invert()

        elif self.pushButton_2.isChecked():
            w_list = [0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.96, 0.98, 1, 1.03, 1.05]
            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider.setValue(5)
            self.label_Num.setNum(5)
            self.horizontalSlider.valueChanged['int'].connect(self.label_Num.setNum)
            self.horizontalSlider.valueChanged.connect(
                lambda: self.defog(w_list[self.horizontalSlider.value()]))
            self.defog()

        elif self.pushButton_3.isChecked():
            self.horizontalSlider.setEnabled(False)
            self.histeq()

        elif self.pushButton_4.isChecked():
            rr_list = [(1, 1), (2, 1), (2, 2), (3, 2), (3, 3), (4, 3),
                       (5, 3), (5, 4), (6, 4), (6, 5), (7, 5)]
            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider.setValue(5)
            self.label_Num.setNum(5)
            self.horizontalSlider.valueChanged['int'].connect(self.label_Num.setNum)
            self.horizontalSlider.valueChanged.connect(
                lambda: self.coloreq(rr_list[self.horizontalSlider.value()]))
            self.coloreq()

        elif self.pushButton_5.isChecked():
            self.horizontalSlider.setEnabled(False)
            self.gray()

        elif self.pushButton_6.isChecked():
            bC_list = [(5, 15), (7, 15), (9, 10), (11, 10), (13, 5), (15, 5),
                       (17, 5), (19, 3), (21, 3), (23, 1), (25, 1)]
            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider.setValue(5)
            self.label_Num.setNum(5)
            self.horizontalSlider.valueChanged['int'].connect(self.label_Num.setNum)
            self.horizontalSlider.valueChanged.connect(
                lambda: self.enhshp(bC_list[self.horizontalSlider.value()]))
            self.enhshp()

        else:
            self.horizontalSlider.setEnabled(False)
            self.pushButton_Apply.setEnabled(False)
            self.disp(DSTFLAG=2)
            k_reciprocal = 1 / (self.graphicsView.k_rec * self.k_trans)  # 滚轮、校正缩放系数记录值的倒数
            self.graphicsView.scale(k_reciprocal, k_reciprocal)
            self.graphicsView.k_rec = 1
            self.k_trans = 1
            self.graphicsView.scene.setSceneRect(self.graphicsView.imItem.boundingRect())

    def invert(self):
        '''
        反色槽函数
        '''
        imTemp = self.graphicsView.CVtemp.img
        self.graphicsView.CVdst.img = ipc.invert_color(imTemp)

        self.disp(CACHEFLAG=False)

    def defog(self, w=0.95):
        '''
        去雾槽函数
        '''
        imTemp = self.graphicsView.CVtemp.img
        imDst = defogging(m=imTemp / 255.0, w=w) * 255
        self.graphicsView.CVdst.img = imDst.astype(uint8)

        self.disp(CACHEFLAG=False)

    def histeq(self):
        '''
        直方图均衡化槽函数
        '''
        imTemp = self.graphicsView.CVtemp.img
        self.graphicsView.CVdst.img = ipc.hist_eq(imTemp)

        self.disp(CACHEFLAG=False)

    def coloreq(self, rr=(4, 3)):
        '''
        自动色彩均衡槽函数
        '''
        imTemp = self.graphicsView.CVtemp.img
        imDst = aceRGB(I=imTemp / 255.0, ratio=rr[0], radius=rr[1]) * 255
        self.graphicsView.CVdst.img = imDst.astype(uint8)

        self.disp(CACHEFLAG=False)

    def gray(self):
        '''
        灰度滤镜槽函数
        '''
        imTemp = self.graphicsView.CVtemp.img
        self.graphicsView.CVdst.img = ipc.cvt2Gray(imTemp)

        self.disp(CACHEFLAG=False, GRAYFLAG=True)

    def enhshp(self, bC=(15, 5)):
        '''
        增强锐化槽函数
        '''
        imTemp = self.graphicsView.CVtemp.img
        self.graphicsView.CVdst.img = ipc.threshold_adaptive(imTemp, bC[0], bC[1])

        self.disp(CACHEFLAG=False, GRAYFLAG=True)

    def adjust(self):
        '''
        调节槽函数
        用于切换到特定的槽函数
        '''
        try:
            self.horizontalSlider.disconnect()
        except TypeError:
            print('No Slider Reused Signal Connect!')
        else:
            print('Slider Reused Signal Disconnected!')

        self.horizontalSlider.setEnabled(True)
        self.horizontalSlider.setMinimum(-10)
        self.horizontalSlider.setValue(0)
        self.label_Num.setNum(0)
        self.horizontalSlider.valueChanged['int'].connect(self.label_Num.setNum)
        self.pushButton_Apply.setEnabled(True)

        if self.pushButton_1.isChecked():
            self.horizontalSlider.valueChanged.connect(
                lambda: self.conbri(b_tick=self.horizontalSlider.value()))

        elif self.pushButton_2.isChecked():
            self.horizontalSlider.valueChanged.connect(
                lambda: self.conbri(c_tick=self.horizontalSlider.value()))

        elif self.pushButton_3.isChecked():
            self.horizontalSlider.valueChanged.connect(
                lambda: self.satura(s_tick=self.horizontalSlider.value()))

        elif self.pushButton_4.isChecked():
            self.horizontalSlider.setMinimum(0)
            self.horizontalSlider.valueChanged.connect(
                lambda: self.sharpen(k_tick=self.horizontalSlider.value()))

        elif self.pushButton_5.isChecked():
            self.horizontalSlider.valueChanged.connect(
                lambda: self.bridark(b_tick=self.horizontalSlider.value()))

        elif self.pushButton_6.isChecked():
            self.horizontalSlider.valueChanged.connect(
                lambda: self.bridark(d_tick=self.horizontalSlider.value()))

        else:
            self.horizontalSlider.setEnabled(False)
            self.pushButton_Apply.setEnabled(False)
            self.disp(DSTFLAG=2)
            k_reciprocal = 1 / (self.graphicsView.k_rec * self.k_trans)  # 滚轮、校正缩放系数记录值的倒数
            self.graphicsView.scale(k_reciprocal, k_reciprocal)
            self.graphicsView.k_rec = 1
            self.k_trans = 1
            self.graphicsView.scene.setSceneRect(self.graphicsView.imItem.boundingRect())

    def conbri(self, c_tick=0, b_tick=0):
        '''
        亮度、对比度调节槽函数
        '''
        imTemp = self.graphicsView.CVtemp.img
        self.graphicsView.CVdst.img = ipc.contrastbright(imTemp, -c_tick * 0.1, b_tick * 7)

        self.disp(CACHEFLAG=False)

    def satura(self, s_tick=0):
        '''
        饱和度调节槽函数
        '''
        imTemp = self.graphicsView.CVtemp.img
        self.graphicsView.CVdst.img = ipc.saturation(imTemp, s_tick / 20.0)

        self.disp(CACHEFLAG=False)

    def sharpen(self, k_tick=0):
        '''
        锐化调节槽函数
        '''
        imTemp = self.graphicsView.CVtemp.img
        self.graphicsView.CVdst.img = ipc.sharpen_laplace(imTemp, k_tick * 0.1)

        self.disp(CACHEFLAG=False)

    def bridark(self, b_tick=0, d_tick=0):
        '''
        亮部/暗部调节槽函数
        '''
        imTemp = self.graphicsView.CVtemp.img
        self.graphicsView.CVdst.img = ipc.zonebrightdark(imTemp, b_tick * 2, d_tick * 2)

        self.disp(CACHEFLAG=False)

    def more(self):
        '''
        更多模式槽函数
        用于切换到特定的槽函数
        '''
        FcnObjs = [self.horizontalSlider, self.pushButton_F1, self.pushButton_F2,
                     self.textEdit, self.comboBox]
        for FcnObject in FcnObjs:
            try:
                FcnObject.disconnect()
            except TypeError:
                print('No {} Reused Signal Connect!'.format(FcnObject.objectName()))
            else:
                print('{} Reused Signal Disconnected!'.format(FcnObject.objectName()))

        self.pushButton_Apply.setEnabled(True)
        self.pushButton_Import.setEnabled(True)
        self.pushButton_Compare.setEnabled(True)

        if self.pushButton_1.isChecked():
            self.graphicsView.imItem.drawMode = 1
            self.label_Function.setText('颜色')
            self.pushButton_F1.setText('更多颜色')
            self.pushButton_F2.setText('更多字体')
            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider.setValue(0)
            self.horizontalSlider.valueChanged.connect(
                lambda: self.colorpicker(tick=self.horizontalSlider.value()))
            self.colorset(self.Color)

            self.pushButton_F1.setEnabled(True)
            self.pushButton_F1.clicked.connect(self.colorother)
            self.pushButton_F2.setEnabled(True)
            self.pushButton_F2.setCheckable(False)
            self.pushButton_F2.clicked.connect(self.fontother)
            self.fontset(self.Font)

            self.textEdit.setEnabled(True)
            self.textEdit.textChanged.connect(self.textset)
            self.comboBox.setEnabled(False)

        elif self.pushButton_2.isChecked():
            self.graphicsView.imItem.drawMode = 2
            self.label_Function.setText('颜色')
            self.pushButton_F1.setText('更多颜色')
            self.pushButton_F2.setText('笔刷粗细')
            self.pushButton_Import.setText('导入贴图')
            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider.setValue(0)
            self.horizontalSlider.valueChanged.connect(
                lambda: self.colorpicker(tick=self.horizontalSlider.value()))
            self.colorset(self.Color)

            self.pushButton_F1.setEnabled(True)
            self.pushButton_F1.clicked.connect(self.colorother)
            self.pushButton_F2.setEnabled(True)
            self.pushButton_F2.setCheckable(True)
            self.pushButton_F2.clicked.connect(self.penwidthset)
            self.penwidthpicker(self.PenWidthTick)

            self.textEdit.setEnabled(False)
            shapes = dict(enumerate(
                ['直线', '箭头线', '矩形 轮廓', '椭圆 轮廓', '三角形 轮廓', '五角星 轮廓',
                 '矩形 填充', '椭圆 填充', '三角形 填充', '五角星 填充', '本地贴图 原始比例',
                 '本地贴图 任意比例']))
            self.comboBox.setEnabled(True)
            self.comboBox.clear()
            for k, v in shapes.items():
                self.comboBox.addItem(v, k)
            self.comboBox.setCurrentIndex(self.Shape)
            self.comboBox.activated['int'].connect(self.shapeset)

            self.pushButton_Import.setEnabled(False)

        elif self.pushButton_3.isChecked():
            self.graphicsView.imItem.drawMode = 3
            self.label_Function.setText('马赛克大小')
            self.label_Num.setPalette(self.palette())
            self.label_Unit.setText('^2')
            self.pushButton_F1.setText('添加马赛克')
            self.pushButton_F2.setText('撤销马赛克')
            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider.setValue(5)
            self.horizontalSlider.valueChanged.connect(
                lambda: self.mosaicset(tick=self.horizontalSlider.value()))
            self.mosaicset()

            self.pushButton_F1.setEnabled(True)
            self.pushButton_F1.clicked.connect(lambda: self.mosaic(DoFlag=True))
            self.pushButton_F2.setEnabled(True)
            self.pushButton_F2.clicked.connect(lambda: self.mosaic(DoFlag=False))

            self.textEdit.setEnabled(False)
            self.comboBox.setEnabled(False)

        elif self.pushButton_4.isChecked():
            self.graphicsView.imItem.drawMode = 4
            self.label_Function.setText('卷积核大小')
            self.label_Num.setPalette(self.palette())
            self.label_Unit.setText('^2')
            self.pushButton_F1.setText('添加模糊')
            self.pushButton_F2.setText('撤销模糊')
            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider.setValue(5)
            self.horizontalSlider.valueChanged.connect(
                lambda: self.blurset(tick=self.horizontalSlider.value()))
            self.blurset()

            self.pushButton_F1.setEnabled(True)
            self.pushButton_F1.clicked.connect(lambda: self.blur(DoFlag=True))
            self.pushButton_F2.setEnabled(True)
            self.pushButton_F2.clicked.connect(lambda: self.blur(DoFlag=False))

            self.textEdit.setEnabled(False)
            self.comboBox.setEnabled(False)

        elif self.pushButton_5.isChecked():
            self.graphicsView.imItem.drawMode = 5
            self.label_Function.setText('色相邻域宽度')
            self.pushButton_F1.setText('选择颜色')
            self.pushButton_F2.setText('透明化')
            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider.setValue(5)
            self.horizontalSlider.valueChanged.connect(
                lambda: self.colorReserve(tick=self.horizontalSlider.value()))
            self.label_Unit.setNum(5)
            self.horizontalSlider.valueChanged['int'].connect(self.label_Unit.setNum)
            self.colorset(self.Color)

            self.pushButton_F1.setEnabled(True)
            self.pushButton_F1.clicked.connect(lambda: self.disp(DSTFLAG=2))
            self.pushButton_F1.clicked.connect(self.colorother)
            self.pushButton_F2.setEnabled(True)
            self.pushButton_F2.setCheckable(True)

            self.textEdit.setEnabled(False)
            self.comboBox.setEnabled(False)

        elif self.pushButton_6.isChecked():
            self.graphicsView.imItem.drawMode = 6
            self.horizontalSlider.setEnabled(False)
            self.pushButton_F1.setText('透视变换')
            self.pushButton_F2.setText('切换顶点')

            self.pushButton_F1.setEnabled(True)
            self.pushButton_F1.setCheckable(True)
            self.pushButton_F1.clicked.connect(self.transform)
            self.pushButton_F2.setEnabled(True)
            self.pushButton_F2.setCheckable(True)
            self.pushButton_F2.clicked.connect(self.transform)

            self.textEdit.setEnabled(False)
            self.comboBox.setEnabled(False)
            self.pushButton_Compare.setEnabled(False)

        else:
            self.graphicsView.imItem.drawMode = 7
            self.label_Function.setText('选择')
            self.label_Num.setPalette(self.palette())
            self.label_Num.setText('        ')
            self.label_Unit.setText('格式')
            self.horizontalSlider.setEnabled(False)
            self.pushButton_F1.setCheckable(False)
            self.pushButton_F1.setEnabled(False)
            self.pushButton_F2.setCheckable(False)
            self.pushButton_F2.setEnabled(False)
            self.textEdit.setEnabled(False)
            self.comboBox.setEnabled(False)
            self.pushButton_Apply.setEnabled(False)
            self.pushButton_Import.setText('导入')

            if self.graphicsView.imItem.pngFlag:
                self.graphicsView.imItem.pngFlag = False
                self.graphicsView.CVtemp.img = ipc.cvt2BGR(self.graphicsView.CVtemp.img)
            if self.graphicsView.imItem.pspTransformed:
                self.graphicsView.imItem.pspTransformed = False

            pm_old = self.graphicsView.imItem.pixmap()
            self.disp(DSTFLAG=2)
            pm_new = self.graphicsView.imItem.pixmap()
            self.scalePixView(pm_new, pm_old, record=True)
            self.graphicsView.scene.setSceneRect(self.graphicsView.imItem.boundingRect())

    def colorpicker(self, tick=0):
        '''
        常用色选择槽函数
        返回QColor格式颜色并设置标签颜色
        '''
        basic = [QtGui.QColor('black'), QtGui.QColor('gray'), QtGui.QColor('white'),
                 QtGui.QColor('red'), QtGui.QColor('orange'), QtGui.QColor('yellow'),
                 QtGui.QColor('green'), QtGui.QColor('lime'), QtGui.QColor('cyan'),
                 QtGui.QColor('blue'), QtGui.QColor('magenta')]
        color = basic[tick]
        self.colorset(color)

    def colorother(self):
        '''
        更多颜色槽函数
        打开颜色对话框选择颜色
        '''
        if self.graphicsView.imItem.drawMode != 5:
            color = QtWidgets.QColorDialog.getColor(
                self.Color, self, '更多颜色', QtWidgets.QColorDialog.ShowAlphaChannel)
            self.colorset(color)
        else:
            color = QtWidgets.QColorDialog.getColor(self.Color, self, '更多颜色')
            self.colorset(color)
            self.colorReserve(self.horizontalSlider.value())

    def fontother(self):
        '''
        更多字体槽函数
        打开字体对话框选择字体
        '''
        font, confirm = QtWidgets.QFontDialog.getFont(self.Font, self, '更多字体')
        if confirm:
            self.fontset(font)

    def colorset(self, color):
        '''
        设置颜色槽函数
        设置label_Num的颜色
        同时设置字体/笔刷颜色
        '''
        p = QtGui.QPalette()
        p.setColor(QtGui.QPalette.Window, color)
        self.label_Num.setAutoFillBackground(True)
        self.label_Num.setPalette(p)
        self.graphicsView.imItem.Color = color
        self.Color = color

    def fontset(self, font):
        '''
        设置字体槽函数
        设置label_Unit的文字
        同时设置字体
        '''
        self.label_Unit.setText(
            QtGui.QFontInfo(font).family()+' '+str(QtGui.QFontInfo(font).pointSize())+'号')
        self.graphicsView.imItem.textFont = font
        self.Font = font

    def textset(self):
        '''
        设置文字槽函数
        '''
        self.graphicsView.imItem.text = self.textEdit.toPlainText()

    def penwidthset(self):
        '''
        设置笔刷粗细槽函数
        '''
        try:
            self.horizontalSlider.disconnect()
        except TypeError:
            print('No Slider Reused Signal Connect!')
        else:
            print('Slider Reused Signal Disconnected!')

        if self.pushButton_F2.isChecked():
            self.label_Function.setText('粗细')
            self.horizontalSlider.setValue(5)
            self.horizontalSlider.valueChanged.connect(
                lambda: self.penwidthpicker(tick=self.horizontalSlider.value()))
            self.penwidthpicker(self.PenWidthTick)
        else:
            self.label_Function.setText('颜色')
            self.horizontalSlider.setValue(0)
            self.horizontalSlider.valueChanged.connect(
                lambda: self.colorpicker(tick=self.horizontalSlider.value()))
            self.colorset(self.Color)

    def penwidthpicker(self, tick=5):
        '''
        根据刻度选择笔刷粗细槽函数
        '''
        self.graphicsView.imItem.autoPenWidth()
        autowidthf = self.graphicsView.imItem.penWidthF * 2 / self.graphicsView.k_rec
        d = autowidthf * 0.15
        widths = [autowidthf - 5 * d, autowidthf - 4 * d, autowidthf - 3 * d,
                  autowidthf - 2 * d, autowidthf - d, autowidthf,
                  autowidthf + d, autowidthf + 2 * d, autowidthf + 3 * d,
                  autowidthf + 4 * d, autowidthf + 5 * d]
        widths = [round(width, 2) for width in widths]
        self.graphicsView.imItem.penWidthF = widths[tick]
        self.label_Unit.setText(str(widths[tick]))
        self.PenWidthTick = tick

    def shapeset(self, value):
        '''
        设置形状槽函数
        '''
        self.graphicsView.imItem.drawShape = value
        self.Shape = value
        if value == 10 or value == 11:
            self.pushButton_Import.setEnabled(True)
        else:
            self.pushButton_Import.setEnabled(False)

    def mosaicset(self, tick=5):
        '''
        根据刻度选择马赛克大小槽函数
        '''
        self.graphicsView.imItem.autoPenWidth()
        autowidthf = self.graphicsView.imItem.penWidthF * 5 / self.graphicsView.k_rec
        d = autowidthf * 0.15
        widths = [autowidthf - 5 * d, autowidthf - 4 * d, autowidthf - 3 * d,
                  autowidthf - 2 * d, autowidthf - d, autowidthf,
                  autowidthf + d, autowidthf + 2 * d, autowidthf + 3 * d,
                  autowidthf + 4 * d, autowidthf + 5 * d]
        widths = [int(round(width, 0)) for width in widths]
        for width in widths:
            if width == 0:  # 防止传过去0
                widths[widths.index(width)] += 1
        self.graphicsView.imItem.mosaicSize = widths[tick]
        self.label_Num.setNum(widths[tick])

    def mosaic(self, DoFlag=True):
        '''
        图像选定区域添加/撤销马赛克槽函数
        '''
        if DoFlag:
            imTemp = self.graphicsView.CVtemp.img
            if self.graphicsView.imItem.pointf_e:
                self.graphicsView.CVdst.img = ipc.mosaic_rect(
                    imTemp, self.graphicsView.imItem.pointf_tl.toPoint(),
                    self.graphicsView.imItem.pointf_br.toPoint(),
                    self.graphicsView.imItem.mosaicSize)
            else:
                self.graphicsView.CVdst.img = ipc.mosaic_rect(
                    imTemp, QtCore.QPoint(0, 0),
                    QtCore.QPoint(self.graphicsView.imItem.pixmap().width(),
                                  self.graphicsView.imItem.pixmap().height()),
                    self.graphicsView.imItem.mosaicSize)

            self.disp(CACHEFLAG=False)
        else:
            self.disp(DSTFLAG=2)

    def blurset(self, tick=5):
        '''
        根据刻度选择高斯卷积核大小槽函数
        '''
        self.graphicsView.imItem.autoPenWidth()
        autowidthf = self.graphicsView.imItem.penWidthF * 7 / self.graphicsView.k_rec
        d = autowidthf * 0.15
        widths = [autowidthf - 5 * d, autowidthf - 4 * d, autowidthf - 3 * d,
                  autowidthf - 2 * d, autowidthf - d, autowidthf,
                  autowidthf + d, autowidthf + 2 * d, autowidthf + 3 * d,
                  autowidthf + 4 * d, autowidthf + 5 * d]
        widths = [int(round(width, 0)) for width in widths]
        for width in widths:
            if width == 0:  # 防止传过去0
                widths[widths.index(width)] += 3
            elif width % 2 == 0:
                widths[widths.index(width)] += 1
        self.graphicsView.imItem.blurKSize = widths[tick]
        self.label_Num.setNum(widths[tick])

    def blur(self, DoFlag=True):
        '''
        虚化槽函数
        图像选定区域外全部虚化/撤销虚化槽函数
        如果没有框终点值的话，虚化全图
        '''
        if DoFlag:
            imTemp = self.graphicsView.CVtemp.img
            if self.graphicsView.imItem.pointf_e:
                self.graphicsView.CVdst.img = ipc.blur_rect(
                    imTemp, self.graphicsView.imItem.pointf_tl.toPoint(),
                    self.graphicsView.imItem.pointf_br.toPoint(),
                    self.graphicsView.imItem.blurKSize)
            else:
                k = self.graphicsView.imItem.blurKSize
                self.graphicsView.CVdst.img = ipc.blur_gauss(imTemp, (k, k))

            self.disp(CACHEFLAG=False)
        else:
            self.disp(DSTFLAG=2)

    def colorReserve(self, tick=5):
        '''
        保留色彩槽函数
        '''
        imTemp = self.graphicsView.CVtemp.img
        if self.pushButton_F2.isChecked():
            self.graphicsView.CVdst.img = ipc.reserve_color(imTemp, self.graphicsView.imItem.Color, tick,
                                                            transFlag=True)
            self.disp(CACHEFLAG=False, PNGFLAG=True)
            self.graphicsView.imItem.pngFlag = True
        else:
            self.graphicsView.CVdst.img = ipc.reserve_color(imTemp, self.graphicsView.imItem.Color, tick)
            self.disp(CACHEFLAG=False)

    def transform(self):
        '''
        透视变换槽函数
        '''
        pm_old = self.graphicsView.imItem.pixmap()

        if self.graphicsView.imItem.CropEFlag:
            if self.pushButton_F1.isChecked():
                imTemp = self.graphicsView.CVtemp.img
                if self.pushButton_F2.isChecked():
                    self.graphicsView.CVdst.img = ipc.trans_perspective(
                        imTemp, self.graphicsView.imItem.pointfSorted, switch=True)
                    self.graphicsView.imItem.pspTransformed = True
                    self.disp(CACHEFLAG=False)
                else:
                    self.graphicsView.CVdst.img = ipc.trans_perspective(
                        imTemp, self.graphicsView.imItem.pointfSorted, switch=False)
                    self.graphicsView.imItem.pspTransformed = True
                    self.disp(CACHEFLAG=False)
            else:
                self.graphicsView.imItem.pspTransformed = False
                self.disp(DSTFLAG=2)
        else:
            self.pushButton_F1.setChecked(False)

        self.graphicsView.imItem.update()

        pm_new = self.graphicsView.imItem.pixmap()
        self.scalePixView(pm_new, pm_old, record=True)

    def apply(self):
        '''
        应用操作槽函数
        '''
        if self.ModeFlag == 3:
            drawMode = self.graphicsView.imItem.drawMode
            if drawMode == 5 or drawMode == 6:
                self.graphicsView.resetPixmap()
                if drawMode == 6 and self.graphicsView.imItem.pspTransformed:
                    self.graphicsView.imItem.pspTransformed = False
            else:
                self.graphicsView.coverPixmap()
                self.graphicsView.CVdst.Q2CVimg(self.graphicsView.imQT)

        if self.graphicsView.CVdst.img is not None:
            if len(self.graphicsView.CVdst.img.shape) == 3:
                self.graphicsView.CVtemp = deepcopy(self.graphicsView.CVdst)
            else:
                self.graphicsView.CVdst.img = ipc.cvt2Gray(
                    self.graphicsView.CVdst.img, FAKEFLAG=True)
                self.graphicsView.CVtemp = deepcopy(self.graphicsView.CVdst)

        FcnObjs = [self.pushButton_1, self.pushButton_2, self.pushButton_3,
                   self.pushButton_4, self.pushButton_5, self.pushButton_6]
        for FcnObj in FcnObjs:
            FcnObj.setChecked(False)
            FcnObj.setEnabled(True)
        self.pushButton_Apply.setEnabled(False)
        self.pushButton_Apply.setChecked(False)
        self.fcnlinkreset()

    def open(self):
        '''
        打开文件槽函数
        '''
        filepath, _filter = \
            QtWidgets.QFileDialog.getOpenFileName(self, '打开', self.MainWindow.InputDir,
                                                  'PNG 文件(*.png);; JPG 文件(*.jpg);; JPEG 文件(*.jpeg);; 所有 文件(*.*)',
                                                  '所有 文件(*.*)')
        shape = self.graphicsView.imItem.drawShape
        if filepath:
            self.MainWindow.InputDir = os.path.dirname(filepath)
            self.MainWindow.filename = os.path.basename(filepath)
            filename, ext = os.path.splitext(self.MainWindow.filename)
            new_filename = filename + "_edit" + ext
            self.MainWindow.OutputDir = os.path.dirname(filepath) + '/' + new_filename

            if self.ModeFlag == 3 and self.pushButton_2.isChecked() and (shape == 10 or shape == 11):
                self.graphicsView.imItem.map_dir = filepath
            else:
                pm_old = self.graphicsView.imItem.pixmap()

                self.graphicsView.CVsrc, self.graphicsView.CVdst = AppImg(), AppImg()
                self.graphicsView.CVsrc.loadimg(filepath)
                self.disp(DSTFLAG=0)

                pm_new = self.graphicsView.imItem.pixmap()
                self.scalePixView(pm_new, pm_old, record=False)

                # 联动主窗口
                self.MainWindow.frame_2.dir_img = None  # 每次打开文件，初始化保存路径及文件名
                self.MainWindow.frame.dir_img = filepath
                self.MainWindow.frame.CV.loadimg(self.MainWindow.frame.dir_img)
                # 发现QtGui.QImage可以直接根据文件名读取图片
                self.MainWindow.frame.imQT = QtGui.QImage(self.MainWindow.frame.dir_img)  # 省去用OPENCV读再转换的一步
                self.MainWindow.frame.repaint()  # 触发绘图事件显示
                if self.MainWindow.RefreshFlag:
                    self.MainWindow.frame_2.imQT = None
                    self.MainWindow.frame_2.repaint()

    def compare(self, pressed=True):
        '''
        对比槽函数
        '''
        if pressed:
            self.disp(DSTFLAG=0, CACHEFLAG=False)
        else:
            if self.graphicsView.CVdst.img is None:
                self.disp(DSTFLAG=2)
            else:
                try:
                    self.disp(CACHEFLAG=False, PNGFLAG=self.graphicsView.imItem.pngFlag)
                except ValueError:
                    self.disp(CACHEFLAG=False, GRAYFLAG=True, PNGFLAG=self.graphicsView.imItem.pngFlag)

    def disp(self, DSTFLAG=1, CACHEFLAG=True, GRAYFLAG=False, PNGFLAG=False):
        '''
        显示刷新方法，接受CVdst/src/temp标识码、缓存标识符、灰度转换选项、PNG转换选项输入
        将CV类图片转换成QImage并在ImgView上显示
        '''
        if DSTFLAG == 1:
            self.graphicsView.imQT = self.graphicsView.CVdst.CV2Qimg(GRAYFLAG, PNGFLAG)
            if CACHEFLAG:
                self.graphicsView.CVtemp = deepcopy(self.graphicsView.CVdst)
        elif DSTFLAG == 0:
            self.graphicsView.imQT = self.graphicsView.CVsrc.CV2Qimg(GRAYFLAG, PNGFLAG)
            if CACHEFLAG:
                self.graphicsView.CVtemp = deepcopy(self.graphicsView.CVsrc)
        else:
            self.graphicsView.imQT = self.graphicsView.CVtemp.CV2Qimg(GRAYFLAG, PNGFLAG)

        self.graphicsView.resetPixmap()

    def scalePixView(self, pm_new: QtGui.QPixmap, pm_old: QtGui.QPixmap, record=False):
        '''
        根据disp前后pixmap大小确定显示大小比例
        从而进行自适应放缩并居中
        '''
        k_w, k_h = pm_new.width() / pm_old.width(), pm_new.height() / pm_old.height()
        # print("新:{}x{},旧:{}x{}".format(pm_new.width(), pm_new.height(), pm_old.width(), pm_old.height()))
        self.w_img4view = self.graphicsView.s_old.width() * k_w
        self.h_img4view = self.graphicsView.s_old.height() * k_h
        self.graphicsView.s_old = QtCore.QSize(int(round(self.w_img4view)), int(round(self.h_img4view)))
        if record:
            self.k_trans *= self.graphicsView.scaleView()
        else:
            self.graphicsView.scaleView()
        self.graphicsView.scene.setSceneRect(self.graphicsView.imItem.boundingRect())
