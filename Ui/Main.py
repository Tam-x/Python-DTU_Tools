# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os


class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName("mainWindow")
        mainWindow.resize(494, 366)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap((self.resource_path("..\\Res\\icon.png"))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(mainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(350, 100))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.setScaledContents(True)
        image = QtGui.QImage()
        image.load(self.resource_path("..\\Res\\title.png"))
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 3)
        self.btnDeviceCheck = QtWidgets.QToolButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnDeviceCheck.sizePolicy().hasHeightForWidth())
        self.btnDeviceCheck.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(self.resource_path("..\\Res\\icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(self.resource_path("..\\Res\\deviceIcon.png")), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(self.resource_path("..\\Res\\servericon.png")), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(self.resource_path("..\\Res\\nouseicon.png")), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.btnDeviceCheck.setIcon(icon2)
        self.btnDeviceCheck.setIconSize(QtCore.QSize(100, 100))
        self.btnDeviceCheck.setObjectName("btnDeviceCheck")
        self.gridLayout.addWidget(self.btnDeviceCheck, 1, 0, 1, 1)
        self.btnOnlineCheck = QtWidgets.QToolButton(self.centralwidget)
        self.btnOnlineCheck.setIcon(icon1)
        self.btnOnlineCheck.setIconSize(QtCore.QSize(100, 100))
        self.btnOnlineCheck.setObjectName("btnOnlineCheck")
        self.gridLayout.addWidget(self.btnOnlineCheck, 1, 1, 1, 1)
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridLayout.addWidget(self.calendarWidget, 1, 2, 2, 1)
        self.btnMqcheck = QtWidgets.QToolButton(self.centralwidget)
        self.btnMqcheck.setIcon(icon3)
        self.btnMqcheck.setIconSize(QtCore.QSize(100, 100))
        self.btnMqcheck.setObjectName("btnMqcheck")
        self.gridLayout.addWidget(self.btnMqcheck, 2, 0, 1, 1)
        self.toolButton_3 = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton_3.setIcon(icon4)
        self.toolButton_3.setIconSize(QtCore.QSize(100, 100))
        self.toolButton_3.setObjectName("toolButton_3")
        self.gridLayout.addWidget(self.toolButton_3, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        mainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(mainWindow)
        self.statusbar.setObjectName("statusbar")
        mainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(mainWindow)
        mainWindow.show()
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        _translate = QtCore.QCoreApplication.translate
        mainWindow.setWindowTitle(_translate("mainWindow", "DTU工具"))
        self.btnDeviceCheck.setText(_translate("mainWindow", "..."))
        self.btnOnlineCheck.setText(_translate("mainWindow", "..."))
        self.btnMqcheck.setText(_translate("mainWindow", "..."))
        self.toolButton_3.setText(_translate("mainWindow", "..."))

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath('.')
        return os.path.join(base_path, relative_path)