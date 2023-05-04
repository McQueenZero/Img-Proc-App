# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_About(QtWidgets.QDialog):
    '''
    在designer自动生成的代码
    基础上修改编写
    '''
    def __init__(self):
        super(Ui_About, self).__init__()
        self.k = 2
        self.fontsize = "font-size:"+str(int(round(15*self.k)))+"px;"
        self.setupUi(self)  # 括号里必须有self

    def setupUi(self, About_Dialog):
        About_Dialog.setObjectName("About_Dialog")
        About_Dialog.resize(400*self.k, 300*self.k)

        self.label_Icon = QtWidgets.QLabel(About_Dialog)
        self.label_Icon.setGeometry(QtCore.QRect(0, 0, 400*self.k, 100*self.k))
        self.label_Icon.setPixmap(QtGui.QPixmap("./Icons/西工大校徽标缩小.png"))
        self.label_Icon.setAlignment(QtCore.Qt.AlignCenter)
        self.label_Icon.setObjectName("label_Icon")

        self.label_Info = QtWidgets.QLabel(About_Dialog)
        self.label_Info.setGeometry(QtCore.QRect(10*self.k, 110*self.k, 391*self.k, 181*self.k))
        self.label_Info.setStyleSheet(self.fontsize)
        self.label_Info.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_Info.setObjectName("label_Info")

        self.retranslateUi(About_Dialog)
        QtCore.QMetaObject.connectSlotsByName(About_Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "软件信息"))
        self.label_Info.setText(_translate("Dialog", "图像处理小工具 Version 1.0.9 \n"
        "\n"
        "\n"
        "\n"
        "作者：赵敏琨 学号 2022202443 自动化学院\n"
        "\n"
        "\n"
        "\n"
        "Copyright (C) 2023 Minkun Zhao. All Rights Reserved."))
