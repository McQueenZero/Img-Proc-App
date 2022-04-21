import os
import sys
from PyQt5.QtWidgets import QApplication
import cgitb

from gui import Ui_MainWindow

if __name__ == '__main__':
    log_dir = os.path.join(os.getcwd(), 'log')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    cgitb.enable(display=0, format='txt', logdir=log_dir)

    app = QApplication(sys.argv)

    MainGUI = Ui_MainWindow()
    MainGUI.show()

    sys.exit(app.exec_())
