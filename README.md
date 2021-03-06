# AIDA64监控小屏

Inspired by FlyAkari https://github.com/flyAkari/AIDA64Reader

## 目前使用的硬件
1. ESP8266模块(NodeMCU D1 Mini开发板)
2. SSD1306模块(0.96寸128*64黑白显示器)
3. USB-microUSB数据线、面包板、杜邦线等

## Arduino IDE 环境配置
1. 安装并打开Arduino IDE
2. 在文件-首选项-附加开发板管理器地址中填入https://arduino.esp8266.com/stable/package_esp8266com_index.json
3. 点击工具-开发板-开发板管理器，搜索8266，点击安装下载开发板定义
4. 开发板定义下载完成后，选择LOLIN(WEMOS) D1 R2 & Mini
5. 点击项目-加载库-管理库，搜索并安装u8g2库 (注：u8g2库是黑白显示器专用，彩色屏需改用其它库)
6. 安装USB转串口芯片CH340G/CH341G驱动CH341SER.EXE

## 连接开发板并上传程序
1. 用一根USB-microUSB线连接开发板和电脑，在电脑的设备管理器中查看"端口(COM和LPT)"中新增的设备，记住开发板的端口号，以COM3为例。一般来说，COM1是电脑主板自带的端口，不是开发板。如果还不确定是哪个端口，可以拔下连接开发板的线，看看哪个端口消失了。如果插上线之后开发板电源灯闪亮一下(说明USB线是通电的)，但电脑上没有新增的端口，甚至设备管理器中没有端口这一项，应高度怀疑连接线没有数据功能，多换几条线试试。验证方法：打开声音，注意听插拔时是否有提示音，如无提示音，说明此线没有数据传输功能。
2. 在Arduino IDE中打开准备好的ino文件，点击项目-上传，或界面上打勾右边的向右的箭头。项目会自动编译并上传到开发板Flash区中。上传完成后，按Reset键重置开发板。

## 配置AIDA64并运行上位机程序
1. 启动AIDA64，在设置-外部程序中勾选"允许共享内存"
2. 安装Python依赖：pip install pyserial
3. 运行Python上位机程序：python aida64upper.py
4. Enjoy!
