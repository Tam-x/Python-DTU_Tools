from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5 import QtWidgets, QtCore
from Ui.OnlineCheck import MY_UI
from Ui.OnlineCheckBase import OnlineMainWindow
import sys, re

reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')

def open_file():
    fileName = QFileDialog.getOpenFileName(caption='选择文件')
    if fileName:
        try:
            IPs = []
            for line in open(fileName[0]):
                if '#' not in line:
                    for ip in reip.findall(line):
                        IPs.append(ip)
            if IPs:
                form.refreshUI(IPs)
        except:
            print('except')

if __name__ == "__main__":
    IPs = []
    app = QApplication(sys.argv)
    mainWindow = OnlineMainWindow()
    menubar = QtWidgets.QMenuBar(mainWindow)
    menu = QtWidgets.QMenu(menubar)
    mainWindow.setMenuBar(menubar)
    statusbar = QtWidgets.QStatusBar(mainWindow)
    mainWindow.setStatusBar(statusbar)
    actionOpen = QtWidgets.QAction(mainWindow)
    menu.addAction(actionOpen)
    menubar.addAction(menu.menuAction())
    _translate = QtCore.QCoreApplication.translate
    mainWindow.setWindowTitle(_translate("MainWindow", "DTU在线监测"))
    menu.setTitle(_translate("MainWindow", "文件"))
    actionOpen.setText(_translate("MainWindow", "导入设备地址文件"))
    actionOpen.triggered.connect(open_file)
    form = MY_UI()
    mainWindow.setCentralWidget(form)
    mainWindow.resize(350,550)
    mainWindow.show()
    sys.exit(app.exec_())