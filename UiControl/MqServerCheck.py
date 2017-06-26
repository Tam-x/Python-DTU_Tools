from Ui.MQServer import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5 import QtCore
from Config.Config import Config
import time, threading
import paho.mqtt.client as mqtt
from binascii import hexlify

TIME_OUT_LIST = ['1', '2', '3', '4', '5', '10']

class MQServerControl(Ui_MainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.ui = QMainWindow()
        self.setupUi(self.ui)
        self.mCheckDeviceClient = mqtt.Client(client_id='dtu-server-check-tool-tanxing-debug')
        self.comboBox.addItems(TIME_OUT_LIST)
        self.action.triggered.connect(self.click_menu)
        self.cleanLog.clicked.connect(self.cleanLogs)
        self.pushButton.clicked.connect(self.check_dtus_online)
        self.isStartCheckDevice = False
        self.isover = False
        self.startTime = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.run_loop)
        self.checkTimer = QtCore.QTimer()
        self.checkTimer.timeout.connect(self.check_device_finished)
        self.timer.start(1)

    def click_menu(self):
        configFile = QFileDialog.getOpenFileName(caption="选择文件")
        print (configFile)
        if configFile:
            self.ips = []
            self.textBrowser.append('导入设备地址：')
            self.importFile(configFile[0])

    def importFile(self, configFile):
        try:
            for line in open(configFile):
                if '#' not in line:
                    self.textBrowser.append(line)
                    self.ips.append(line.strip())


        except:
            print ("except")

    def cleanLogs(self):
        self.textBrowser.setText('')


    def on_connect_check(self, client, userdata, flag, rc):
        print("Connected with result code " + str(rc))
        if len(self.ips) > 0:
            for ip in self.ips:
                ip = ip.strip()
                client.subscribe('dtu/up/edian/'+ip+'/maintenance')

    def on_message_check(self, client, userdata, msg):
        data = hexlify(msg.payload).decode().upper()
        if len(data) < 14:
            return
        ip = data[6:14]
        ip =(self.hex2ip(ip[:2],ip[2:4], ip[4:6],ip[6:]))
        print ('recive:'+ip)
        if ip not in self.recvIps:
            self.recvIps.append(ip)
            print ('adddpend')
            self.mCheckDeviceClient.unsubscribe('dtu/up/edian/'+ip+'/maintenance')
        try:
            self.ips.remove(ip)
        except:
            print ('revmoodddd')
            pass
        if (len(self.ips) < 1):
            self.isStartCheckDevice = False
            self.check_device_finished()

    def query_device(self):
        isConnect = False
        try:
            self.mCheckDeviceClient.connect(Config.MQ_ONLINE_BROKER, Config.MQ_ONLINE_PORT, 60)
            isConnect = True
            self.mCheckDeviceClient.loop_forever()
        except:
            if isConnect:
                print("except")
                self.mCheckDeviceClient.disconnect()
                self.isStartCheckDevice = False
                self.pushButton.setText("开始检测")
                self.pushButton.setEnabled(True)

    def check_dtus_online(self):
        if  len(self.ips) < 1:
            self.textBrowser.append('已经订阅完成或者没有导入设备的地址')
            return
        if not self.isStartCheckDevice:
            self.textBrowser.append('开始检测...')
            self.isover = False
            self.startCheckDeviceTime = time.time()
            self.isStartCheckDevice = True
            self.pushButton.setText("查询中...")
            self.pushButton.setEnabled(False)
            self.mCheckDeviceClient.on_connect = self.on_connect_check
            self.mCheckDeviceClient.on_message = self.on_message_check
            thread = threading.Thread(target=self.query_device)
            thread.start()

    def check_device_finished(self):
        self.pushButton.setText("开始检测")
        self.pushButton.setEnabled(True)
        self.isStartCheckDevice = False
        self.mCheckDeviceClient.loop_stop()
        self.mCheckDeviceClient.disconnect()
        self.isover = True


    def run_loop(self):
        if self.isStartCheckDevice:
            if time.time() - self.startCheckDeviceTime > int(self.comboBox.currentText()) * 60:
                self.check_device_finished()

        if self.isover:
            if len(self.recvIps) > 0:
                self.textBrowser.append('-'*25)
                for ip in self.recvIps:
                    self.textBrowser.append(ip + '订阅到数据')
                    self.textBrowser.append('-' * 25)
                self.textBrowser.append('检测结束\n')
            else:
                self.textBrowser.append('全部设备都没有订阅到数据')
            self.recvIps = []
            print ('----------------------')
            self.isover = False

    def hex2ip(self, data1, data2, data3, data4):
        return str(int(data4,16))+'.'+str(int(data3,16))+'.'+str(int(data2,16))+'.'+str(int(data1,16))