"""
@file      : AHT20.py
@author    : Aaron Chen (aaron.chen@example.com)
@brief     : AHT20 temperature and humidity sensor.
@version   : 0.1
@date      : 2026-04-21
@copyright : Copyright (c) 2024
"""


from machine import I2C
from utime import sleep_ms


class AHT20(object):
    """AHT20 温湿度传感器类，通过 I2C 读取温度和湿度数据。

    舒适度等级：
        COMFORT_COLD   (-1): 偏冷
        COMFORT_GOOD   (0):  舒适
        COMFORT_WARM   (1):  偏热
        COMFORT_DRY    (2):  偏干燥
        COMFORT_HUMID  (3):  偏潮湿

    典型用法:
        sensor = AHT20()
        rh, temp = sensor.read()
        comfort = sensor.check_comfort(temp, rh)
        sensor.monitor()
    """

    COMFORT_COLD = -1
    COMFORT_GOOD = 0
    COMFORT_WARM = 1
    COMFORT_DRY = 2
    COMFORT_HUMID = 3

    _COMFORT_LABELS = {
        -1: "偏冷", 0: "舒适", 1: "偏热", 2: "偏干燥", 3: "偏潮湿",
    }

    def __init__(self):
        """初始化 AHT20 传感器实例，配置 I2C 通信。"""
        self._i2c = I2C(I2C.I2C0, I2C.STANDARD_MODE)
        self._addr = 0x38
        self._RESET_CMD = b'\xBA'
        self._INIT_CMD = b'\xE1'
        self._MEASURE_CMD = b'\xAC\x33\x00'
        self._callback = None

    # ---- 回调 ----

    def set_callback(self, callback):
        """设置温湿度回调。

        Args:
            callback: 回调函数，签名 callback(temp, rh, comfort_code)
        """
        self._callback = callback

    # ---- 传感器控制 ----

    def reset(self):
        """软复位传感器。"""
        self._i2c.write(self._addr, b'\x00', 0, self._RESET_CMD, len(self._RESET_CMD))
        sleep_ms(20)

    def init(self):
        """初始化传感器，配置校准参数。"""
        self._i2c.write(self._addr, b'\x00', 0, self._INIT_CMD, len(self._INIT_CMD))

    # ---- 读取 ----

    def read(self):
        """读取温湿度数据。

        发送测量命令后等待至少 80ms，读取 6 字节数据并换算：
            湿度 = RH_reg / 2^20 × 100（%）
            温度 = temp_reg / 2^20 × 200 - 50（°C）

        Returns:
            tuple or (): (湿度%, 温度°C)，数据异常时返回空元组
        """
        self._i2c.write(self._addr, b'\x00', 0, self._MEASURE_CMD, len(self._MEASURE_CMD))
        sleep_ms(80)

        r_data = bytearray([0x00] * 6)
        self._i2c.read(self._addr, b'\x00', 0, r_data, 6, 80)

        # 检查传感器状态：bit[7] = 1 表示忙碌
        if r_data[0] & 0x80:
            return ()

        # 湿度：[1]的8位 + [2]的8位 + [3]的高4位 = 20位
        RH_reg = (r_data[1] << 12) | (r_data[2] << 4) | (r_data[3] >> 4)
        RH = RH_reg / (1 << 20) * 100

        # 温度：[3]的低4位 + [4]的8位 + [5]的8位 = 20位
        temp_reg = ((r_data[3] & 0x0F) << 16) | (r_data[4] << 8) | r_data[5]
        temp = temp_reg / (1 << 20) * 200 - 50

        return RH, temp

    # ---- 舒适度 ----

    @staticmethod
    def check_comfort(temp, rh):
        """根据温湿度判断舒适度。

        Args:
            temp: 温度 °C
            rh:   湿度 %

        Returns:
            int: COMFORT_COLD / COMFORT_GOOD / COMFORT_WARM / COMFORT_DRY / COMFORT_HUMID
        """
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
        """获取舒适度等级的中文标签。"""
        return cls._COMFORT_LABELS.get(code, "未知")

    # ---- 监控 ----

    def monitor(self, interval_ms=1000):
        """持续监控温湿度并输出舒适度。

        Args:
            interval_ms: 采样间隔 ms，默认 1000
        """
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
