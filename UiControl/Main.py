#!/usr/bin/python3.5
# -*- coding: utf-8 -*-
# author: tx
# time: 2017-06-13

from Ui.Main import Ui_mainWindow
from PyQt5.QtWidgets import QMainWindow
from Ui.OnlineCheckBase import OnlineMainWindow
from UiControl.DeviceCheck import DeviceControl
from UiControl.MqServerCheck import MQServerControl

class MainControl(Ui_mainWindow):
    def __init__(self, parent=None):
        self.main = QMainWindow()
        self.setupUi(self.main)
        self.windowOnline = OnlineMainWindow()
        self.deviceCheck = DeviceControl()
        self.mqServerCheck = MQServerControl()
        self.btnOnlineCheck.clicked.connect(self.click_btn_online)
        self.btnDeviceCheck.clicked.connect(self.click_btn_device)
        self.btnMqcheck.clicked.connect(self.click_btn_mq)

    def click_btn_online(self):
        print('online')
        self.windowOnline.show()

    def click_btn_device(self):
        print('device')
        self.deviceCheck.ui.show()

    def click_btn_mq(self):
        print('mqtt')
        self.mqServerCheck.ui.show()