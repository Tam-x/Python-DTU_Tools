import serial

class Config:
    MQ_ONLINE_BROKER = '120.76.73.35'
    MQ_ONLINE_PORT = 1883

    # 是否调试
    IS_DEBUG = True
    # 数据位
    SERIAL_DATABIT_ARRAY = ("8", "7", "6", "5")
    # 停止位
    SERIAL_STOPBIT_ARRAY = ("1", "1.5", "2")
    # 校验位
    SERIAL_CHECKBIT_ARRAY = (
    serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD, serial.PARITY_MARK, serial.PARITY_SPACE)
    # 波特率
    BAUDRATES = ("50", "75", "110", "134", "150", "200", "300", "600", "1200", "1800", "2400", "4800",
                 "9600", "19200", "38400", "57600", "115200", "230400", "460800", "500000")