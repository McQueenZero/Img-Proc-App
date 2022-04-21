import sys
from PyQt5 import QtGui, QtWidgets, QtCore
import cv2


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    # 尝试把图像平滑等功能的菜单初始化写成函数形式
    def initUI(self):
        # 菜单栏
        exitAction1 = QtWidgets.QAction('图像平滑', self)
        exitAction1.setShortcut('1')
        exitAction1.setStatusTip('可选：空域中值/高斯，频域中值/高斯/巴特沃斯低通滤波')
        # exitAction1.triggered.connect(self.run_rf)

        exitAction2 = QtWidgets.QAction('图像平滑', self)
        exitAction2.setShortcut('2')
        exitAction2.setStatusTip('可选：空域中值/高斯，频域中值/高斯/巴特沃斯低通滤波')
        # exitAction1.triggered.connect(self.run_rf)

        # 工具栏
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('图像平滑')
        fileMenu.addAction(exitAction1)
        fileMenu.addAction(exitAction2)
        # 以上部分尝试写成函数形式

        # 状态栏
        self.statusBar()
        # 主界面
        self.hbox = QtWidgets.QHBoxLayout()
        self.lbl_left = QtWidgets.QLabel()
        self.lbl_left.setStyleSheet(
            "font:20pt '楷体';border-width: 3px;border-style: solid;border-color: rgb(0, 0, 0);")
        self.lbl_left.setAutoFillBackground(True)
        # self.lbl_left.setFixedSize(1000, 1000)
        self.lbl_right = QtWidgets.QLabel()
        self.lbl_right.setStyleSheet(
            "font:20pt '楷体';border-width: 3px;border-style: solid;border-color: rgb(0, 0, 0);")
        self.lbl_right.setAutoFillBackground(True)
        # self.lbl_right.setFixedSize(1000, 1000)
        self.hbox.addWidget(self.lbl_left)
        self.hbox.addWidget(self.lbl_right)
        self.setLayout(self.hbox)
        # 布局
        widget = QtWidgets.QWidget()
        widget.setLayout(self.hbox)
        self.setCentralWidget(widget)
        # 设置主窗口大小、位置、标题
        self.setGeometry(10, 10, 2000, 1000)
        self.setWindowTitle('Image Processor')
        self.showMaximized()
        self.show()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())