# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mqtt.ui'
#
# Created: Fri May 19 12:06:35 2017
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QGridLayout
# from PyQt5.Qt import SIGNAL
from PyQt5 import QtCore, QtGui, QtWidgets
import threading, time
from binascii import hexlify
import paho.mqtt.client as mqtt
from Config.Config import Config

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(540, 362)
        self.ips = []
        self.recvIps = []
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.horizontalLayout.addWidget(self.comboBox)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.cleanLog = QtWidgets.QPushButton(self.centralwidget)
        self.cleanLog.setObjectName(_fromUtf8("pushButton"))
        self.horizontalLayout_2.addWidget(self.pushButton)
        self.horizontalLayout_2.addWidget(self.cleanLog)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 540, 17))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_DTU = QtWidgets.QMenu(self.menubar)
        self.menu_DTU.setObjectName(_fromUtf8("menu_DTU"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setObjectName(_fromUtf8("action"))
        self.menu_DTU.addAction(self.action)
        self.menubar.addAction(self.menu_DTU.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "DTU-Server通讯检测v1.0测试版", None))
        self.label.setText(_translate("MainWindow", "超时设置", None))
        self.label_2.setText(_translate("MainWindow", "分", None))
        self.pushButton.setText(_translate("MainWindow", "开始检测", None))
        self.cleanLog.setText(_translate("MainWindow", "清除日志", None))
        self.menu_DTU.setTitle(_translate("MainWindow", "文件", None))
        self.action.setText(_translate("MainWindow", "导入地址", None))


    # def click_menu(self):
    #     configFile = QFileDialog.getOpenFileName(caption="选择文件")
    #     print (configFile)
    #     if configFile:
    #         self.ips = []
    #         self.textBrowser.append(u'导入设备地址：')
    #         self.importFile(configFile)
    #
    # def importFile(self, configFile):
    #     try:
    #         for line in open(configFile):
    #             if '#' not in line:
    #                 self.textBrowser.append(line)
    #                 self.ips.append(line.strip())
    #
    #
    #     except:
    #         print ("except")
    #
    # def cleanLogs(self):
    #     self.textBrowser.setText('')
    #
    #
    # def on_connect_check(self, client, userdata, flag, rc):
    #     print("Connected with result code " + str(rc))
    #     if len(self.ips) > 0:
    #         for ip in self.ips:
    #             ip = ip.strip()
    #             client.subscribe('dtu/up/edian/'+ip+'/maintenance')
    #
    # def on_message_check(self, client, userdata, msg):
    #     data = hexlify(msg.payload).decode().upper()
    #     if len(data) < 14:
    #         return
    #     ip = data[6:14]
    #     ip =(self.hex2ip(ip[:2],ip[2:4], ip[4:6],ip[6:]))
    #     print ('recive:'+ip)
    #     if ip not in self.recvIps:
    #         self.recvIps.append(ip)
    #         print ('adddpend')
    #         self.mCheckDeviceClient.unsubscribe('dtu/up/edian/'+ip+'/maintenance')
    #     try:
    #         self.ips.remove(ip)
    #     except:
    #         print ('revmoodddd')
    #         pass
    #     if (len(self.ips) < 1):
    #         self.isStartCheckDevice = False
    #         self.check_device_finished()
    #
    # def query_device(self):
    #     isConnect = False
    #     try:
    #         self.mCheckDeviceClient.connect(Config.MQ_ONLINE_BROKER, Config.MQ_ONLINE_PORT, 60)
    #         isConnect = True
    #         self.mCheckDeviceClient.loop_forever()
    #     except:
    #         if isConnect:
    #             print("except")
    #             self.mCheckDeviceClient.disconnect()
    #             self.isStartCheckDevice = False
    #             self.pushButton.setText(u"开始检测")
    #             self.pushButton.setEnabled(True)
    #
    # def check_dtus_online(self):
    #     if  len(self.ips) < 1:
    #         self.textBrowser.append(u'已经订阅完成或者没有导入设备的地址')
    #         return
    #     if not self.isStartCheckDevice:
    #         self.textBrowser.append(u'开始检测...')
    #         self.isover = False
    #         self.startCheckDeviceTime = time.time()
    #         self.isStartCheckDevice = True
    #         self.pushButton.setText(u"查询中...")
    #         self.pushButton.setEnabled(False)
    #         self.mCheckDeviceClient.on_connect = self.on_connect_check
    #         self.mCheckDeviceClient.on_message = self.on_message_check
    #         thread = threading.Thread(target=self.query_device)
    #         thread.start()
    #
    # def check_device_finished(self):
    #     self.pushButton.setText(u"开始检测")
    #     self.pushButton.setEnabled(True)
    #     self.isStartCheckDevice = False
    #     self.mCheckDeviceClient.loop_stop()
    #     self.mCheckDeviceClient.disconnect()
    #     self.isover = True
    #
    #
    # def run_loop(self):
    #     if self.isStartCheckDevice:
    #         if time.time() - self.startCheckDeviceTime > int(self.comboBox.currentText()) * 60:
    #             self.check_device_finished()
    #
    #     if self.isover:
    #         if len(self.recvIps) > 0:
    #             self.textBrowser.append('-'*25)
    #             for ip in self.recvIps:
    #                 self.textBrowser.append(ip + u'订阅到数据')
    #                 self.textBrowser.append('-' * 25)
    #             self.textBrowser.append(u'检测结束\n')
    #         else:
    #             self.textBrowser.append(u'全部设备都没有订阅到数据')
    #         self.recvIps = []
    #         print ('----------------------')
    #         self.isover = False
    #
    # def hex2ip(self, data1, data2, data3, data4):
    #     return str(int(data4,16))+'.'+str(int(data3,16))+'.'+str(int(data2,16))+'.'+str(int(data1,16))


import sys
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w =Ui_MainWindow()
    ui = QMainWindow()
    w.setupUi(ui)
    ui.show()
    sys.exit(app.exec_())
