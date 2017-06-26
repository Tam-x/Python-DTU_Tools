import sys, os
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap
import paho.mqtt.client as mqtt
from binascii import hexlify
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout,\
    QComboBox, QFrame, QScrollArea, QPushButton
from PyQt5.QtCore import QTimer
from Config.Config import Config
import threading, time

isShowTime = True
timeSpanList = ["1","5", "10", "15", "20", "25", "30", "45","60"]

class MY_UI(QWidget):
    def __init__(self, ips = None):
        super(MY_UI, self).__init__()
        self.initWidget(ips)

    def closeMQTT(self):
        if self.mMQClient:
            if self.isMQConnected:
                self.mMQClient.disconnect()
                self.isStartWatch = False
                self.checkBtn.setText('开始监测')

    def initWidget(self, ips):
        self.statusInfo = {}
        self.isStartWatch = False
        self.currentIP = None
        self.isMQConnected = False
        self.mMQClient = mqtt.Client(client_id='dtu-online-check-tool-tanxing-debug')
        self.timer = QTimer()
        vbox = QVBoxLayout()
        self.remind = QLabel("提示：从文件中导入DTU地址！")
        self.isImportData = False
        vbox.addWidget(self.remind)
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 388, 313))
        h1box = QHBoxLayout()
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setGeometry(QRect(40, 180, 400, 3))
        addrLabel = QLabel("设备地址")
        h1box.addWidget(addrLabel)
        addrLabel.setAlignment(Qt.AlignCenter)
        onLineLabel = QLabel("在线状态   ")
        h1box.addWidget(onLineLabel)
        onLineLabel.setAlignment(Qt.AlignCenter)
        if isShowTime:
            timeLabel = QLabel("时间")
            timeLabel.setAlignment(Qt.AlignCenter)
            h1box.addWidget(timeLabel)
        h1box.setGeometry(QRect(0, 0, 100, 313))
        vbox.addLayout(h1box)

        self.svbox = QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        vbox.addWidget(self.scrollArea)
        bootmbox = QHBoxLayout()
        bootmbox.addWidget(QLabel("离线间隔"))
        self.comBox = QComboBox()
        bootmbox.addWidget(self.comBox)
        self.comBox.addItems(timeSpanList)
        bootmbox.addWidget(QLabel("分"))
        bootombox = QHBoxLayout()
        bootombox.addLayout(bootmbox)
        bootombox.addWidget(QLabel(""))
        self.checkBtn = QPushButton("开始监测")
        bootombox.addWidget(self.checkBtn)
        vbox.addLayout(bootombox)
        self.setLayout(vbox)
        self.checkBtn.clicked.connect(self.watch)
        self.timer.timeout.connect(self.refresh)

    def refresh(self):
        if self.isStartWatch and self.statusInfo:
            span = int(self.comBox.currentText()) * 60
            for ip in self.statusInfo.keys():
                print(self.statusInfo.get(ip)[4])
                if time.time() - span > self.statusInfo.get(ip)[4] and self.statusInfo.get(ip)[3]:
                    self.statusInfo.get(ip)[3] = False
                    self.statusInfo.get(ip)[1].setText("OFF")
                    self.statusInfo.get(ip)[1].setPixmap(QPixmap(self.resource_path(".\\Res\\off.png")))
                if self.statusInfo.get(ip)[3]:
                    print("6666")
                    self.statusInfo.get(ip)[1].setText("ON")
                    time_local = time.localtime(self.statusInfo.get(ip)[4])
                    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                    self.statusInfo.get(ip)[2].setText(dt)
                    self.statusInfo.get(ip)[1].setPixmap(QPixmap(self.resource_path(".\\Res\\on.png")))

    def produce(self, ip, pos):
        vbox = QVBoxLayout()
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        if pos != 0:
            vbox.addWidget(line, 1)
        hbox = QHBoxLayout()
        ipLable = QLabel(ip)
        isOnline = QLabel("--")
        ipLable.setAlignment(Qt.AlignCenter)
        isOnline.setAlignment(Qt.AlignCenter)
        # self.isOnline.setPixmap(QPixmap("redv.png"))
        hbox.addWidget(ipLable, 1)
        hbox.addWidget(isOnline, 1)
        timeLable = QLabel("-")
        timeLable.setAlignment(Qt.AlignCenter)
        print(ip)
        self.statusInfo.update({ip:[ipLable, isOnline, timeLable, False, time.time()]})
        if isShowTime:
            hbox.addWidget(timeLable, 1)
        vbox.addLayout(hbox, 1)
        return vbox

    def refreshUI(self, IPs):
        self.remind.hide()
        self.isImportData = True
        if self.isStartWatch:
            if self.isMQConnected and self.statusInfo:
                for ip in self.statusInfo.keys():
                    topic1 = 'dtu/up/edian/' + str(ip) + '/devices'
                    topic2 = 'dtu/up/edian/' + str(ip) + '/mantances'
                    self.mMQClient.unsubscribe(topic1)
                    self.mMQClient.unsubscribe(topic2)
        self.statusInfo = {}
        self.unfill()
        for i in range(len(IPs)):
            layout = self.produce(IPs[i],i)
            self.svbox.addLayout(layout, 1)
        self.svbox.setContentsMargins(0,0,0,0)
        if self.isMQConnected and self.statusInfo:
            for ip in self.statusInfo.keys():
                topic1 = 'dtu/up/edian/' + str(ip) + '/devices'
                topic2 = 'dtu/up/edian/' + str(ip) + '/mantances'
                self.mMQClient.subscribe(topic1)
                self.mMQClient.subscribe(topic2)

    def unfill(self):
        def deleteItems(layout):
            if layout is not None:
                while layout.count():
                    item = layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        deleteItems(item.layout())

        deleteItems(self.svbox)

    def watch(self):
        print(self.isStartWatch)
        if self.isStartWatch:
            self.over_watch()
        else:
            self.start_watch()

    def start_watch(self):
        if not self.isImportData:
            self.remind.setText("提示：还没有导入监测设备地址!")
            return
        self.isStartWatch = True
        self.checkBtn.setText("结束监测")
        self.timer.start(5)
        self.mMQClient.on_connect = self.on_connect_check
        self.mMQClient.on_message = self.on_message_check
        thread = threading.Thread(target=self.query_data)
        thread.start()


    def over_watch(self):
        self.isStartWatch = False
        self.checkBtn.setText("开始监测")
        self.timer.stop()
        for ip in self.statusInfo.keys():
            topic1 = 'dtu/up/edian/'+str(ip)+'/devices'
            topic2 = 'dtu/up/edian/' + str(ip) + '/mantances'
            if self.isMQConnected:
                self.mMQClient.unsubscribe(topic1)
                self.mMQClient.unsubscribe(topic2)
        if self.isMQConnected:
            self.mMQClient.loop_stop()
            self.mMQClient.disconnect()
        self.isMQConnected = False


    def on_connect_check(self, client, userdata, flag, rc):
        print("Connected with result code " + str(rc))
        if rc == 0:
            self.isMQConnected = True
            for ip in self.statusInfo.keys():
                topic1 = 'dtu/up/edian/'+str(ip)+'/devices'
                topic2 = 'dtu/up/edian/' + str(ip) + '/mantances'
                client.subscribe(topic1)
                client.subscribe(topic2)
        else:
            self.isMQConnected = False

    def on_message_check(self, client, userdata, msg):
        data = hexlify(msg.payload)
        if len(data) < 14:
            return
        ip = data[6:14]
        self.currentIP =(self.hex2ip(ip[:2],ip[2:4], ip[4:6],ip[6:]))
        if self.currentIP in self.statusInfo.keys():
            self.statusInfo.get(self.currentIP)[3] = True
            self.statusInfo.get(self.currentIP)[4] = time.time()

    def hex2ip(self, data1, data2, data3, data4):
        return str(int(data4,16))+'.'+str(int(data3,16))+'.'+str(int(data2,16))+'.'+str(int(data1,16))

    def query_data(self):
        isConnect = False
        try:
            self.mMQClient.connect(Config.MQ_ONLINE_BROKER, Config.MQ_ONLINE_PORT, 60)
            isConnect = True
            self.mMQClient.loop_forever()
        except:
            if isConnect:
                self.mMQClient.disconnect()
                self.isStartWatch = False
                self.checkBtn.setText("开始监测")

    def resource_path(self, relative_path):
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath('.')
        return os.path.join(base_path, relative_path)
