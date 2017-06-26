from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5 import QtWidgets, QtCore
from Ui.OnlineCheck import MY_UI
import re

reip = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')

class OnlineMainWindow(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        IPs = []
        self.menubar = QtWidgets.QMenuBar(self)
        menu = QtWidgets.QMenu(self.menubar)
        self.setMenuBar(self.menubar)
        statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(statusbar)
        actionOpen = QtWidgets.QAction(self)
        menu.addAction(actionOpen)
        self.menubar.addAction(menu.menuAction())
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "DTU在线监测"))
        menu.setTitle(_translate("MainWindow", "文件"))
        actionOpen.setText(_translate("MainWindow", "导入设备地址文件"))
        actionOpen.triggered.connect(self.open_file)
        self.form = MY_UI()
        self.setCentralWidget(self.form)
        self.resize(350, 550)



    def open_file(self):
        fileName = QFileDialog.getOpenFileName(caption='选择文件')
        if fileName:
            try:
                IPs = []
                for line in open(fileName[0]):
                    if '#' not in line:
                        for ip in reip.findall(line):
                            IPs.append(ip)
                if IPs:
                    self.form.refreshUI(IPs)
            except:
                print('except')

    def closeEvent(self, event):
        self.centralWidget().closeMQTT()
        print('close------------------------------------------------------')
        super(OnlineMainWindow, self).closeEvent(event)