import os
import sys
from PyQt5.QtWidgets import QApplication
import cgitb

from gui import Ui_MainWindow


def check_folder_dir(path):
    folder_dir = os.path.join(os.getcwd(), path)
    if not os.path.exists(folder_dir):
        os.mkdir(folder_dir)

    return folder_dir


if __name__ == '__main__':
    log_dir = check_folder_dir('log')
    check_folder_dir('InputImages')
    check_folder_dir('OutputImages')
    cgitb.enable(display=0, format='txt', logdir=log_dir)

    app = QApplication(sys.argv)

    MainGUI = Ui_MainWindow(sys.platform)
    MainGUI.show()

    sys.exit(app.exec_())
