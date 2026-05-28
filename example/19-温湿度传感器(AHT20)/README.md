# 温湿度传感器

## **一、** **模块介绍**

温湿度传感器作为常见的传感器之一，是一种装有湿敏和热敏元件，能够用来测量温度和湿度的传感器装置。其工作原理主要基于热敏电阻和湿敏电阻的特性，通过测量电阻值并转换成电压信号输出，实现对环境温湿度的准确监测。

**发光原理：**

模块通过内部热敏元件与湿敏元件采集环境数据，经芯片校准后以**I2C 数字信号**输出，开发板通过 I2C 总线读取温度和湿度数值。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设         | 开发板       |
| ------------ | ------------ |
| AHT20（+）   | 3.3V         |
| AHT20（-）   | GND          |
| AHT20（SCL） | PIN17（SCL） |
| AHT20（SDA） | PIN16（SDA） |

 

![](../media/aht20.png)

## 三、 操作步骤

请参考目录中的开发指导手册

![](../media/test1.png)

## 四、 驱动代码

```python
from machine import I2C 

from utime import sleep_ms

 

class aht20(object):

  def __init__(self):

     self.i2c = I2C(I2C.I2C0,I2C.STANDARD_MODE)

     self.slave_addr = 0x38# AHT20 slave address

     self.RESET_CMD = b'/xBA'# reset command

     self.INIT_CMD = b'/xE1'# initialize command

     self.MEASURE_CMD = b'/xAC/x33/x00'# measure command

 

 

  def reset(self):

     self.i2c.write(self.slave_addr,b'/x00',0,self.RESET_CMD,len(self.RESET_CMD))

     sleep_ms(20)# wait 20ms

 

  def init(self):

     self.i2c.write(self.slave_addr,b'/x00',0,self.INIT_CMD,len(self.INIT_CMD))

 

  def read(self):

     /# Send measurement cmd to trigger data acquirement.

     self.i2c.write(self.slave_addr,b'/x00',0,self.MEASURE_CMD,len(self.MEASURE_CMD))

 

     /#read data

     /#wait for data ready (at least 80ms)

     sleep_ms(80)

     r_data = bytearray([0x00]*6)

     self.i2c.read(self.slave_addr,b'/x00',0,r_data,6,80)

     busy = 0#r_data[0]>>7

     if not busy:

       RH_reg_data = (r_data[1]<<12) | (r_data[2]<<4) | (r_data[3]>>4)

       RH = RH_reg_data/(1<<20) * 100

 

       temp_reg_data = ((r_data[3]&0x0F)<<16) | (r_data[4]<<8) | r_data[5]

       temp = temp_reg_data/(1<<20) * 200 - 50

 

 

       return RH,temp

     else:

       return ()

     

if __name__ == '__main__':

  aht20_obj = aht20()

  aht20_obj.init()

  sleep_ms(1000)

  while True:

     res = aht20_obj.read()

     if res:

       print("RH: %.2f%%" % res[0])

       print("Temp: %.2f" % res[1])

       print("------------")

     else:

       print("read error")

     sleep_ms(1000)
```



 