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

![](../../media/aht20.png)

## 三、 驱动代码

```python
from machine import I2C
from utime import sleep_ms


class AHT20(object):
    """AHT20 温湿度传感器类，通过 I2C 读取温度和湿度数据。

    应用场景：环境监测、智能家居温控、仓储温湿度管理等。
    """

    def __init__(self):
        """初始化 AHT20 传感器实例，配置 I2C 通信。"""
        self.i2c = I2C(I2C.I2C0, I2C.STANDARD_MODE)
        self.slave_addr = 0x38  # AHT20 I2C 从机地址
        self.RESET_CMD = b'\xBA'       # 复位命令
        self.INIT_CMD = b'\xE1'       # 初始化命令
        self.MEASURE_CMD = b'\xAC\x33\x00'  # 测量命令

    def reset(self):
        """软复位传感器。"""
        self.i2c.write(self.slave_addr, b'\x00', 0, self.RESET_CMD, len(self.RESET_CMD))
        sleep_ms(20)  # 等待复位完成

    def init(self):
        """初始化传感器，配置校准参数。"""
        self.i2c.write(self.slave_addr, b'\x00', 0, self.INIT_CMD, len(self.INIT_CMD))

    def read(self):
        """读取温湿度数据。

        发送测量命令后等待至少 80ms，读取 6 字节数据并换算：
            湿度 = RH_reg / 2^20 × 100（%）
            温度 = temp_reg / 2^20 × 200 - 50（°C）

        Returns:
            tuple or (): (湿度, 温度)，忙碌时返回空元组
        """
        # 发送测量命令
        self.i2c.write(self.slave_addr, b'\x00', 0, self.MEASURE_CMD, len(self.MEASURE_CMD))

        # 等待数据就绪（至少 80ms）
        sleep_ms(80)
        r_data = bytearray([0x00] * 6)
        self.i2c.read(self.slave_addr, b'\x00', 0, r_data, 6, 80)

        busy = 0
        if not busy:
            # 湿度数据：[1]的8位 + [2]的8位 + [3]的高4位 = 20位
            RH_reg_data = (r_data[1] << 12) | (r_data[2] << 4) | (r_data[3] >> 4)
            RH = RH_reg_data / (1 << 20) * 100

            # 温度数据：[3]的低4位 + [4]的8位 + [5]的8位 = 20位
            temp_reg_data = ((r_data[3] & 0x0F) << 16) | (r_data[4] << 8) | r_data[5]
            temp = temp_reg_data / (1 << 20) * 200 - 50

            return RH, temp
        else:
            return ()

    def check_comfort(self, temp, rh):
        """根据温湿度判断舒适度。

        实际应用场景：智能家居温控、办公环境监测、仓储环境管理等。

        Args:
            temp: 温度，单位 °C
            rh: 湿度，单位 %

        Returns:
            str: 舒适度描述
        """
        if temp < 18:
            return "偏冷"
        elif temp > 28:
            return "偏热"
        elif rh < 30:
            return "偏干燥"
        elif rh > 70:
            return "偏潮湿"
        else:
            return "舒适"

    def monitor(self, interval_ms=1000):
        """持续监控温湿度并输出舒适度。

        Args:
            interval_ms: 采样间隔，单位毫秒，默认 1000ms
        """
        self.init()
        sleep_ms(1000)
        while True:
            res = self.read()
            if res:
                rh, temp = res
                comfort = self.check_comfort(temp, rh)
                print("温度: %.1f°C | 湿度: %.1f%% | 状态: %s" % (temp, rh, comfort))
            else:
                print("读取失败")
            sleep_ms(interval_ms)


if __name__ == '__main__':
    sensor = AHT20()
    sensor.monitor(interval_ms=1000)
```



