# LED模块

## **一、** **模块介绍**

LED原理及产业分类LED是发光二极体( Light EmitTIng Diode, LED)的简称，也被称作发光二极管，这种半导体组件发展以来一般是作为指示灯、显示板，但目前随着技术增加，已经能作为光源使用，它不但能够高效率地直接将电能转化为光能，而且拥有最长达数万小时～10 万小时的使用寿命，同时具备不若传统灯泡易碎，并能省电，同时拥有环保无汞、体积小、可应用在低温环境、光源具方向性、造成光害少与色域丰富等优点。

**LED组成：**

![](../../media/led1.png)

**发光原理：**

![](../../media/led2.png)

左为正极，右为负极。当正负极形成电压差时，LED点亮。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设     | 开发板       |
| -------- | ------------ |
| LED（+） | 3.3V         |
| LED（-） | GND          |
| LED（S） | PIN4(GPIO31) |

 

![](../../media/led3.png)

## 三、 驱动代码

```python
from machine import Pin
import utime

class LED():
    def __init__(self,pin):
        self.pin=Pin(pin,Pin.OUT,Pin.PULL_DISABLE,0)
    def write(self,value):
        self.pin.write(value)
        
    def read(self):
        return self.pin.read()
    
    def open_LED(self):
        self.pin.write(1)
        
    def close_LED(self):
        self.pin.write(0)

    def test_led(self):
        while True:
            self.open_LED()
            utime.sleep(1)
            self.close_LED()
            utime.sleep(1)


if __name__=='__main__':
    laser=LED(Pin.GPIO31)
    laser.test_led()
        
        
```

 