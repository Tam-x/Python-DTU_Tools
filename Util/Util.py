# _*_ coding: utf-8 _*_
from PyQt5.QtWidgets import QMessageBox
import re
import time

class Util:
    def parse_address(self, address):
        adr = address.strip()
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
                    Util.show_warning('错误', "非法地址参数："+num)
                    is_adr = False
                    break
                if num and int(num) > 254:
                    Util.show_warning('错误', "非法地址参数："+num+",仅支持0-254")
                    is_adr = False
                    break
        print("ddddddddd1")
        if is_adr:
            while '' in res:
                print("ddddddddd2")
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
                Util.show_warning('错误', "请输入正确地址")

    def get_now_time(self, oh):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def show_warning(self, title, message):
        QMessageBox.warning(None, title, message+"。    ", QMessageBox.Ok)

    def hex_show(self, strargv):
        restr = ''
        slen = len(strargv)
        for i in range(slen):
            restr += hex(strargv[i])+' '
        return restr

    def byte_to_hexarray(self, bytes):
        array = []
        for b in bytes:
            array.append(int(b))
        return array

    def myLog(self, is_log, mes):
        if is_log:
            print(mes)

if __name__ == '__main__':
    # m = Tool.get_now_time(1)
    # Tool.show_warning('nime', m)
    str = "1,2,    4, , , 6, 6,,,"
    # print(str)
    # str1 = str.replace(" ",'')
    #
    # print(str1)
    # str2 = str1.split(',')
    # print(str2)
    # while '' in str2:
    #     str2.remove('')
    m = b'd\x03\x02\x00\x02u\x8d'
    n = b'd\x03\x02\x00\x02u\x8d'
    print(Util.hex_show(m+n))
    ids = ["x","x","m"]
    print(m+n)
