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

    舒适度等级：
        COMFORT_COLD(-1):偏冷, COMFORT_GOOD(0):舒适, COMFORT_WARM(1):偏热,
        COMFORT_DRY(2):偏干燥, COMFORT_HUMID(3):偏潮湿

    典型用法:
        sensor = AHT20()
        rh, temp = sensor.read()
        sensor.monitor()
    """

    COMFORT_COLD = -1
    COMFORT_GOOD = 0
    COMFORT_WARM = 1
    COMFORT_DRY = 2
    COMFORT_HUMID = 3

    def __init__(self):
        self._i2c = I2C(I2C.I2C0, I2C.STANDARD_MODE)
        self._addr = 0x38
        self._RESET_CMD = b'\xBA'
        self._INIT_CMD = b'\xE1'
        self._MEASURE_CMD = b'\xAC\x33\x00'
        self._callback = None

    def set_callback(self, callback):
        """设置温湿度回调。callback(temp, rh, comfort_code)"""
        self._callback = callback

    def reset(self):
        """软复位传感器。"""
        self._i2c.write(self._addr, b'\x00', 0, self._RESET_CMD, len(self._RESET_CMD))
        sleep_ms(20)

    def init(self):
        """初始化传感器，配置校准参数。"""
        self._i2c.write(self._addr, b'\x00', 0, self._INIT_CMD, len(self._INIT_CMD))

    def read(self):
        """读取温湿度数据。湿度=RH_reg/2^20*100%, 温度=temp_reg/2^20*200-50°C。

        Returns:
            tuple or (): (湿度%, 温度°C)，数据异常时返回空元组
        """
        self._i2c.write(self._addr, b'\x00', 0, self._MEASURE_CMD, len(self._MEASURE_CMD))
        sleep_ms(80)
        r_data = bytearray([0x00] * 6)
        self._i2c.read(self._addr, b'\x00', 0, r_data, 6, 80)
        # 检查传感器忙碌状态
        if r_data[0] & 0x80:
            return ()
        RH_reg = (r_data[1] << 12) | (r_data[2] << 4) | (r_data[3] >> 4)
        RH = RH_reg / (1 << 20) * 100
        temp_reg = ((r_data[3] & 0x0F) << 16) | (r_data[4] << 8) | r_data[5]
        temp = temp_reg / (1 << 20) * 200 - 50
        return RH, temp

    @staticmethod
    def check_comfort(temp, rh):
        """根据温湿度判断舒适度等级（数字常量）。"""
        if temp < 18:
            return AHT20.COMFORT_COLD
        elif temp > 28:
            return AHT20.COMFORT_WARM
        elif rh < 30:
            return AHT20.COMFORT_DRY
        elif rh > 70:
            return AHT20.COMFORT_HUMID
        else:
            return AHT20.COMFORT_GOOD

    @classmethod
    def comfort_label(cls, code):
        _labels = {-1:"偏冷", 0:"舒适", 1:"偏热", 2:"偏干燥", 3:"偏潮湿"}
        return _labels.get(code, "未知")

    def monitor(self, interval_ms=1000):
        """持续监控温湿度并输出舒适度。"""
        self.init()
        sleep_ms(1000)
        while True:
            res = self.read()
            if res:
                rh, temp = res
                comfort = self.check_comfort(temp, rh)
                label = self.comfort_label(comfort)
                print("温度: {:.1f}°C | 湿度: {:.1f}% | 状态: {}".format(temp, rh, label))
                if self._callback:
                    self._callback(temp, rh, comfort)
            else:
                print("读取失败")
            sleep_ms(interval_ms)


if __name__ == '__main__':
    sensor = AHT20()
    sensor.monitor(interval_ms=1000)
```



