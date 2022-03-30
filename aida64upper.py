# -*- coding: utf-8 -*-
"""
Created on 2020-07-23 23:36:03

@author: Walnut

"""

import mmap
import xml.dom.minidom
import serial #pip install pyserial
import time
import os, platform

def kiB2bps(kiB):
    t = float(kiB) * 8
    if t > 1000:
        return ("%.1f"%(t/1024)).rjust(5," ") + " Mbps"
    else:
        return ("%.1f"%(t)).rjust(5," ") + " kbps"

if platform.system() == "Windows":
    os.system("chcp 65001")
print("AIDA64 Python上位机")

while True:
    # 读取AIDA64共享内存数据，参见文档https://www.aida64.co.uk/user-manual/external-applications
    # 10000是读取的长度值，并不知道实际数据的长度，如果实际数据超出此区域需要增加长度.
    # 请求的长度多于实际长度时自动填0. 实际数据中\x00后面还有一些内容，原因不明，需在\x00出现时提前截断.
    # consider using multiprocessing.shared_memory for python 3.8+
    mm = mmap.mmap(-1, 12000, "AIDA64_SensorValues", mmap.ACCESS_READ)
    # 原生数据只有"一行"，直接readline获得b""二进制串，转码为普通ascii字符串，x00空白字符截止
    raw = ""
    for i in range(mm.size()):
        c = mm.read(1)
        if c == b'\x00':
            break
        raw = raw + c.decode('cp1252')
    mm.close()
    if len(raw)==0:
        print("无数据, 请开启AIDA64共享内存.")
        time.sleep(1)
        continue
    # 原生数据没有根元素，其实不符合XML格式规范，套上根元素方便解析
    xmlstr = "<AIDA64>" + raw + "</AIDA64>"
    # with open("aida64.xml", mode="w", encoding='cp1252') as f:
    #     print(xmlstr, file=f)
    # XML转DOM树，参考资料https://www.runoob.com/python/python-xml.html
    try:
        DOMTree = xml.dom.minidom.parseString(xmlstr)
    except:
        print("XML转DOM失败.")
        continue
    root = DOMTree.documentElement
    # 共6类数据，生成相应的list，拼接到aidalist
    groups = ["sys", "fan", "temp", "duty", "volt", "pwr"]
    xmllist = []
    for g in groups:
        xmllist.extend(root.getElementsByTagName(g))
    datadict = {}
    for element in xmllist:
        eid = element.getElementsByTagName('id')[0].childNodes[0].data
        edata = element.getElementsByTagName('value')[0].childNodes[0].data
        datadict[eid] = edata  
    try:
        # ESP8266使用的波特率为1500000
        scom = serial.Serial("COM3", 1500000)
        scomlist = []
        scomlist.append("CPU: %s%% @ %.2f GHz"
                        %(datadict["SCPUUTI"].rjust(2," "), float(datadict["SCPUCLK"])/1000))
        scomlist.append("%s°C, %.0f W, %srpm"
                        %(datadict["TCPU"], float(datadict["PCPUPKG"]), datadict["FCPU"]))
        scomlist.append("RAM: %.2f GB (%s%%)"
                        %(float(datadict["SUSEDMEM"])/1024, datadict["SMEMUTI"]))
        TDP_GPU = 175 # RTX2060Super
        scomlist.append("GPU: %s%%, %.0f MB"
                        %(datadict["SGPU1UTI"].rjust(2," "), float(datadict["SUSEDVMEM"])))
        scomlist.append("%s°C, %s W, %.0frpm "
                        %(datadict["TGPU1DIO"],
                          str(int(175*float(datadict["PGPU1TDPP"])/100)),
                          float(datadict["FGPU1"])))
        # scomlist.append("Network: (DL/UL)")
        # scomlist.append("%s/%s"%(kiB2bps(datadict["SNIC1DLRATE"]),kiB2bps(datadict["SNIC1ULRATE"])))
        for i in range(len(scomlist)):
            msg = "{" + str(i) + "@" + scomlist[i] + "}"
            scom.write(msg.encode())
            # print(msg)
        scom.close()
        time.sleep(1)
    except serial.SerialException:
        print("串口通信失败")
        time.sleep(1)
        continue
    except KeyboardInterrupt:
        print("KeyboardInterrupt Detected")
        break
    