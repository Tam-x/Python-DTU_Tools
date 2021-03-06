from Util.Crc16 import CRC16

class DeviceCommand:

    DEVICES = ("电表DTM830", "电表DTM833", "电表GRT603","电表FM100", "测温-YADO", "测温-XMT-2888FC", "测温-BWD3K130C","测温-BWD3K320C",  "仁科-水浸",
               "仁科-烟感","仁科-温湿度","贝斯特-IO模块","贝斯特-温湿度","贝斯特-水浸模块","CSW11温湿度","Phorp计","ZL-528转换模块"
              )
    CMD_DTM830 = [0x00, 0x03, 0x00, 0xC9, 0x00, 0x03, 0x00, 0x00]
    CMD_DTM833 = [0x00, 0x03, 0x00, 0xC9, 0x00, 0x03, 0x00, 0x00]
    CMD_DTM603 = [0x00, 0x03, 0x00, 0x65, 0x00, 0x02, 0x00, 0x00]
    CMD_TEMP_YADO = [0x00, 0x03, 0x00, 0x01, 0x00, 0x0D, 0x00, 0x00]
    CMD_TEMP_XMT2888FC = [0x00, 0x03, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00]
    CMD_TEMP_BWD3K320C = [0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00]
    CMD_TEMP_BWD3K130C = [0x00, 0x04, 0x00, 0x00, 0x00, 0x04, 0x00, 0x00]
    CMD_KEREN_WATER = [0x00, 0x03, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00]
    CMD_KEREN_SMOKE = [0x00, 0x03, 0x00, 0x03, 0x00, 0x01, 0x00, 0x00]
    CMD_KEREN_TEMPHUMI = [0x00, 0x03, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00]
    CMD_BEST_IO =[0x00, 0x03, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00]
    CMD_BEST_TEMPHUMI = [0x00, 0x03, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00]
    CMD_BEST_WATER = [0x00, 0x03, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00]
    CMD_CSW11_TEMPHUMI = [0x00, 0x03, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00]
    CMD_PHORP = [0x00, 0x03, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00]
    CMD_ZL528 = [0x00, 0x03, 0x00, 0x00, 0x00, 0x08, 0x00, 0x00]
    CMD_FM100 = [0x00, 0x03, 0x00, 0x00, 0x00, 0x03, 0x00, 0x00]

    CMD_DIR = {
        DEVICES[DEVICES.index("电表DTM830")]: CMD_DTM830,
        DEVICES[DEVICES.index("电表DTM833")]: CMD_DTM833,
        DEVICES[DEVICES.index("电表GRT603")]: CMD_DTM603,
        DEVICES[DEVICES.index("电表FM100")]: CMD_FM100,
        DEVICES[DEVICES.index("测温-YADO")]: CMD_TEMP_YADO,
        DEVICES[DEVICES.index("测温-XMT-2888FC")]: CMD_TEMP_XMT2888FC,
        DEVICES[DEVICES.index("测温-BWD3K130C")]: CMD_TEMP_BWD3K130C,
        DEVICES[DEVICES.index("测温-BWD3K320C")]: CMD_TEMP_BWD3K320C,
        DEVICES[DEVICES.index("仁科-水浸")]: CMD_KEREN_WATER,
        DEVICES[DEVICES.index("仁科-烟感")]: CMD_KEREN_SMOKE,
        DEVICES[DEVICES.index("仁科-温湿度")]: CMD_KEREN_TEMPHUMI,
        DEVICES[DEVICES.index("贝斯特-IO模块")]: CMD_BEST_IO,
        DEVICES[DEVICES.index("贝斯特-温湿度")]: CMD_BEST_TEMPHUMI,
        DEVICES[DEVICES.index("贝斯特-水浸模块")]: CMD_BEST_WATER,
        DEVICES[DEVICES.index("CSW11温湿度")]: CMD_CSW11_TEMPHUMI,
        DEVICES[DEVICES.index("Phorp计")]: CMD_PHORP,
        DEVICES[DEVICES.index("ZL-528转换模块")]: CMD_ZL528,
               }

    def get_device_cmd(addr, command):
        crc16 = CRC16()
        command[0] = int(addr)
        return crc16.get_crc16_cmd(command)