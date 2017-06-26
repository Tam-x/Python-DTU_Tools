#!/usr/bin/python3.5

import sys
import os
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

from PyQt5.QtWidgets import QApplication
from UiControl.Main import MainControl
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainControl()
    sys.exit(app.exec_())
    pass