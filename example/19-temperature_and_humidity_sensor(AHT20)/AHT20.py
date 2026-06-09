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
