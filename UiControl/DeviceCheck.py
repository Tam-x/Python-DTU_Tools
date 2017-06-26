#/usr/bin/python3
# _*_ coding: utf_8 _*_

from Ui.DeviceCheck import Ui_MainWindow
from Util.DeviceCommand import DeviceCommand as Command
from Config.Config import Config
from Util.Crc16 import CRC16
import serial, serial.tools.list_ports
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow,QFileDialog
from Util.Util import Util
import sys, time, threading, re

class DeviceControl(Ui_MainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.ui = QMainWindow()
        self.setupUi(self.ui)
        self.initDatas()
        self.connect_fun()
        self.Tool = Util()
        # widge.show()

    def initDatas(self):
        self._serial = serial.Serial()
        self.is_find_comm = True
        self.is_port_open = False
        self.is_debug = False
        self.is_debug_feedback = True
        self.is_send_debug_data = False
        self.debug_send_time = time.time()
        self.debug_recive_data = ""
        self.debug_send_data = ""
        self.debug_buffer= None
        self.current_address = []
        self.current_device = ""
        self.address_num = ""
        self.is_send_hex = True
        self.is_recive_hex = True
        self.radbtnRcvHex.setChecked(True)
        self.radbtnSenHex.setChecked(True)
        self.recstr = ''  # 串口接收字符串
        self.rec_data_cnt = 0  # 数据接收计数
        self.send_data_cnt = 0  # 数据发送是计数
        self.timer = QtCore.QTimer()
        self.comms_add_data()
        # self.is_cancel_debug = False

    def comms_add_data(self):
        self.comSerialPort.addItems(self.set_port_list())
        self.comBaudRate.addItems(Config.BAUDRATES)
        self.comCheckBit.addItems(Config.SERIAL_CHECKBIT_ARRAY)
        self.comDataBit.addItems(Config.SERIAL_DATABIT_ARRAY)
        self.comStopBit.addItems(Config.SERIAL_STOPBIT_ARRAY)
        self.comChooseDevice.addItems(Command.DEVICES)
        self.comBaudRate.setCurrentText("9600")

    def set_port_list(self):
        comms=[]
        port_list = list(serial.tools.list_ports.comports())
        for port in port_list:
            comms.append(port[0])
        if not comms:
            self.is_find_comm = False
            comms = ['none']
        return comms

    def connect_fun(self):
        self.btnOpenSerialPort.clicked.connect(self.open_port)
        self.btnSend.clicked.connect(self.open_send)
        self.btnInputAdr.clicked.connect(self.click_input_adr)
        self.checkBoxDebug.clicked.connect(self.click_debug_device)
        self.radbtnRcvHex.clicked.connect(self.click_recive_hex)
        self.radbtnRcvASCII.clicked.connect(self.click_recive_str)
        self.timer.timeout.connect(self.recive_data)

    def open_port(self):
        if not self.is_port_open:
            if not self.is_find_comm:
                self.textBrowser.setText("串口没插入或重启软件！")
                return
            com_num = self.comSerialPort.currentText()
            baud_rate = self.comBaudRate.currentText()
            data_bit = Config.SERIAL_DATABIT_ARRAY[self.comDataBit.currentIndex()]
            stop_bit = Config.SERIAL_STOPBIT_ARRAY[self.comStopBit.currentIndex()]
            check_bit = Config.SERIAL_CHECKBIT_ARRAY[self.comCheckBit.currentIndex()]
            try:
                self._serial = serial.Serial()
                self._serial.port = com_num
                self._serial.baudrate = int(baud_rate)
                self._serial.stopbits = int(stop_bit)
                self._serial.bytesize = float(data_bit)
                self._serial.parity = check_bit
                self._serial.open()
            except (OSError, serial.SerialException):
                self._serial.close()
                self.timer.stop()
                self.is_port_open = False
                self.show_warning("端口警告！","端口被占用或者不存在")
            if self._serial.is_open:
                self.open_comm_status()
                print("open!")
        else:
            self.close_comm_status()
            self._serial.close()

    def open_comm_status(self):
        self.comCheckBit.setEnabled(False)
        self.comSerialPort.setEnabled(False)
        self.comBaudRate.setEnabled(False)
        self.comStopBit.setEnabled(False)
        self.comDataBit.setEnabled(False)
        self.is_port_open = True
        self.btnOpenSerialPort.setText("关闭")
        self.timer.start(20)
        if self.is_debug or self.checkBoxDebug.isChecked():
            self.is_debug = True
            self.radbtnRcvHex.setChecked(True)
            self.radbtnSenASCII.setChecked(True)
            self.radbtnRcvASCII.setEnabled(False)
            self.radbtnSenHex.setEnabled(False)
            self.checkBoxRcvTime.setChecked(False)
            self.checkBoxRcvTime.setEnabled(False)
            self.checkBoxSenAT.setChecked(False)
            self.checkBoxSenAT.setEnabled(False)
            self.checkBoxSenTime.setChecked(False)
            self.checkBoxSenTime.setEnabled(False)
            self.textEdit.setEnabled(False)

    def close_comm_status(self):
        self.comCheckBit.setEnabled(True)
        self.comSerialPort.setEnabled(True)
        self.comBaudRate.setEnabled(True)
        self.comStopBit.setEnabled(True)
        self.comDataBit.setEnabled(True)
        self.is_port_open = False
        self.timer.stop()
        self.btnOpenSerialPort.setText("打开")
        if self.is_debug:
            self.is_debug = False
            self.radbtnRcvASCII.setEnabled(True)
            self.radbtnSenASCII.setEnabled(True)
            self.checkBoxRcvTime.setEnabled(True)
            self.checkBoxSenAT.setEnabled(True)
            self.radbtnSenHex.setEnabled(True)
            self.checkBoxSenTime.setEnabled(True)
            self.textEdit.setEnabled(True)


    def open_send(self):
        if self.is_port_open:
            if self.is_debug:
                print("debug modle")
                if self.debug_send_data.strip():
                    self.textBrowserDebug.append(self.debug_send_data)
                self.textEdit.setText("")
                send = threading.Thread(target=self.get_debug_data)
                send.start()
            else:
                self.textBrowser.setText("点击发送！")
        else:
            self.show_warning("提示","当前串口没有打开")

    def recive_data(self):
        if self.cleanDatas.is_clean:
            self.textBrowser.clear()
            self.cleanDatas.is_clean = False
        if self.saveDatas.is_save:
            self.saveDatas.is_save = False
            try:
                self.SaveDatas()
            except:
                print("close")
        if self.is_port_open:
            try:
                bytesToRead = self._serial.inWaiting()
            except:
                print("read serial port wrong")
                time.sleep(1)
                return
            if bytesToRead > 0:
                self.recstr = self._serial.read(bytesToRead)
                if self.current_device and self.is_debug:
                    origin = Command.CMD_DIR[self.current_device]
                    len_origin = ((origin[4] & 0xFF) << 8) | (origin[5] & 0xFF)
                    if self.debug_buffer:
                        bytesToRead = bytesToRead + len(self.debug_buffer)
                    if bytesToRead < 2*len_origin+5:
                        self.debug_buffer = self.recstr
                        print("mistake...")
                        return
                # self.recdatacnt += bytesToRead
                if self.is_debug and self.debug_buffer:
                    self.recstr = self.debug_buffer+self.recstr
                    self.debug_buffer = None
                print(self.recstr)
                # self.recstr = self.debug_buffer
                print("window_refresh")
                self.window_refresh()
            else:
                if self.is_debug and bytesToRead == 0 and self.current_address and self.is_debug_feedback == False and self.is_send_debug_data:
                    if time.time() - self.debug_send_time > 3:
                        print("=========chaoshi=======")
                        print(time.time())
                        print(time.time() - self.debug_send_time)
                        print(self.current_address)
                        self.is_debug_feedback = True
                        self.is_send_debug_data = False
                        self.address_num = self.current_address[0]
                        self.debug_send_time = time.time()
                        self.current_address.remove(self.current_address[0])
                        self.debug_recive_data = "【接收】" + self.current_device + " " + str(self.address_num) + "设置超时"
                        self.textBrowserDebug.append(self.debug_recive_data)
                        self.debug_recive_data = ""
                        print("chao shi")

    def window_refresh(self):
        if self.is_recive_hex:
            print("refresh-text")
            print(self.recstr)
            print(self.Tool.hex_show(self.recstr))
            array = self.Tool.hex_show(self.recstr)
            self.address_num = self.recstr[0]
            self.textBrowser.append(array)
            print("show text")
            try:
                if self.is_debug:
                    crc16 = CRC16()
                    array = self.Tool.byte_to_hexarray(self.recstr)
                    origin = Command.CMD_DIR[self.current_device]
                    print(origin)
                    print(array)
                    len_origin = ((origin[4] & 0xFF)<< 8)|(origin[5] & 0xFF)
                    print(len_origin)
                    self.is_set_success = True
                    if len(array) < 5:
                        print("if1")
                        self.is_set_success = False
                    elif len(array) != len_origin*2+5:
                        print("if2")
                        self.is_set_success = False
                    elif (array[0]&0xFF) != int(self.current_address[0]):
                        print(array[0])
                        print(self.current_address[0])
                        print("if3")
                        self.is_set_success = False
                    elif array[1] != origin[1]:
                        print("if4")
                        self.is_set_success = False
                    elif not crc16.check_crc16(array):
                        print("if5")
                        self.is_set_success = False

                    if self.is_set_success:
                        print("chenggong")
                        self.debug_recive_data = "【接收】"+self.current_device+"-"+str(self.current_address[0])+" 设置成功"
                        self.textBrowserDebug.append(self.debug_recive_data)
                        self.current_address.remove(self.current_address[0])
                        self.debug_recive_data = ""
                        time.sleep(1)
                    else:
                        print("shibai--mei chao shi")
                        if self.current_address and self.is_send_debug_data:
                            print("in")
                            print(self.current_address[0])
                            self.debug_recive_data = "【接收】" + self.current_device + str(self.current_address[0]) + " 设置失败"
                            print(self.debug_recive_data)
                            self.textBrowserDebug.append(self.debug_recive_data)
                            print("chenggong--mei chao shi3")
                            self.current_address.remove(self.current_address[0])
                            self.debug_recive_data = ""
                            print("chenggong--mei chao shi5")
                    time.sleep(1)
                    self.is_send_debug_data = False
                    self.is_debug_feedback = True
                    self.recstr=None

            except:
                print("except")

            if self.textBrowser.toPlainText().__len__() > 100000:
                self.textBrowser.clear()
        else:
            try:
                print("no hex recive")
                print(self.recstr)
                print("sss")
                print(self.recstr.decode("utf-8"))
                print("bbb")
                self.textBrowser.append(self.recstr.decode("utf-8"))
                if self.textBrowser.toPlainText().__len__() > 200000:
                    self.textBrowser.clear()
            except :
                print("ex")

    def SaveDatas(self):
        print('save-press')
        filename = QFileDialog.getSaveFileName(None, 'Save File', '.',"Text file(*.txt);;All file(*.*)")
        fname = open(filename[0], 'w')
        print('save-press1:'+str(filename))
        try:
            fname.write(self.textBrowser.toPlainText())
        except:
            print('exception press')
        fname.close()
    def click_recive_hex(self):
        self.is_recive_hex = True

    def click_recive_str(self):
        self.is_recive_hex = False

    def click_input_adr(self):
        if not self.is_port_open:
            self.show_warning("提示","当前串口没有打开")
            return
        if not self.is_debug:
            if self.checkBoxDebug.isChecked():
                self.click_debug_device()
        if self.is_debug:
            str= Tool.parse_address(self.textEditDeviceIp.text())
            if str:
                print(str)
                self.current_address = str.split(",")
                self.current_device = self.comChooseDevice.currentText()
                print(self.current_device)
                print(self.current_address)
                self.debug_send_data = "【发送】设备类型：" + self.current_device + ",调试地址：" + str
                self.textEdit.setText("设备类型：" + self.current_device + ",调试地址：" + str)
        else:
            self.show_warning("提示", "请先选中'调试'选框")

    def click_debug_device(self):
        if self.is_port_open:
            if self.checkBoxDebug.isChecked():
                self.is_debug = True
                self.radbtnRcvHex.setChecked(True)
                self.radbtnSenASCII.setChecked(True)
                self.radbtnRcvASCII.setEnabled(False)
                self.radbtnSenHex.setEnabled(False)
                self.checkBoxRcvTime.setChecked(False)
                self.checkBoxRcvTime.setEnabled(False)
                self.checkBoxSenAT.setChecked(False)
                self.checkBoxSenAT.setEnabled(False)
                self.checkBoxSenTime.setChecked(False)
                self.checkBoxSenTime.setEnabled(False)
                self.textEdit.setEnabled(False)
            else:
                self.is_debug = False
                self.radbtnRcvASCII.setEnabled(True)
                self.radbtnSenASCII.setEnabled(True)
                self.checkBoxRcvTime.setEnabled(True)
                self.checkBoxSenAT.setEnabled(True)
                self.radbtnSenHex.setEnabled(True)
                self.checkBoxSenTime.setEnabled(True)
                self.textEdit.setEnabled(True)

    def get_debug_data(self):
        print("get_debug_data")
        print(self.debug_send_data)
        self.debug_send_data = ""
        if not self.current_address:
            print("no address")
            print(self.current_address)
            return
        while self.current_address:
            if self.is_debug_feedback:
                try:
                    print(self.current_address)
                    data = Command.get_device_cmd(self.current_address[0],Command.CMD_DIR[self.current_device])
                    print("x2")
                    print(data)
                    self.is_send_debug_data = True
                    self.is_debug_feedback = False
                    self.send_data(bytes(data))
                    print("send success")
                except:
                    print("except  bu zhi chi")
                    self.is_debug_feedback = False
                    self.is_send_debug_data = True
                    self.debug_send_time = time.time()
            # else:
            #

    def send_data(self,sdata):
        try:
            print("send data - write")
            if self.is_debug:
                self.debug_send_time = time.time()+1
                print(self.debug_send_time)
            self._serial.write(sdata)
            time.sleep(1)
        except:
            self.show_warning('出错',"写入出错")

    def parse_address(self, address):
        adr = address.strip()
        print("ddddddd33")
        print(adr)
        is_adr = True
        if not adr:
            is_adr = False
            QMessageBox.warning(None, '错误', "请输入地址", QMessageBox.Ok)
        else:
            res = adr.replace(" ", "").split(',')
            print(res)
            p1 = re.compile('^[0-9]*$')
            for num in res:
                number = p1.match(num)
                if not number:
                    self.show_warning('错误', "非法地址参数："+num)
                    is_adr = False
                    break
                if num and int(num) > 254:
                    self.show_warning('错误', "非法地址参数："+num+",仅支持0-254")
                    is_adr = False
                    break
        if is_adr:
            while '' in res:
                res.remove('')
            strr = ""
            i = 0
            print("ddddddddd3")
            res = list(set(res))
            for m in res:
                if (i == 0):
                    strr = strr + m
                    i = 2
                else:
                    strr = strr + "," + m
            result = strr.strip()
            if result:
                return result
            else:
                # QMessageBox.warning(None, '错误', "请输入正确地址", QMessageBox.Ok)
                self.show_warning('错误', "请输入正确地址")

    def show_warning(self, title, message):
        QMessageBox.warning(None, title, message+"。    ", QMessageBox.Ok)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mainWindow = QMainWindow()
#     ui = CommControl(mainWindow)
#     # mainWindow.show()
#     sys.exit(app.exec_())
#     pass