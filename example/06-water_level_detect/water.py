
"""
@file      : water.py
@author    : Aaron Chen
@brief     : Class-based water level sensor demo using ADC with water level conversion
@version   : 0.3
@date      : 2026-06-02
@copyright : Copyright (c) 2026
"""

from misc import ADC
import _thread
import utime


class WaterLevelSensor(object):
    """水位传感器类，通过 ADC 采集电压并换算为水位高度，支持分级报警。

    应用场景：水箱液位监测、漏水检测、洪水预警等。
    通过设置 warn_level 和 alert_level 阈值实现三级状态指示。

    状态分级：
        - 正常：水位 < warn_level
        - 偏高警告：warn_level <= 水位 < alert_level
        - 过高报警：水位 >= alert_level
    """

    def __init__(self, adc_channel=None, ref_voltage=3300, max_water_level=60,
                 warn_level=15, alert_level=35,
                 sample_count=10, sample_interval_ms=5):
        """初始化水位传感器实例。

        Args:
            adc_channel: ADC 通道，默认使用 ADC1
            ref_voltage: 参考电压，单位 mV，默认 3300mV（3.3V）
            max_water_level: 传感器最大量程水位，单位 mm，默认 60mm
            warn_level: 警告水位阈值，单位 mm，默认 15mm
            alert_level: 报警水位阈值，单位 mm，默认 35mm
            sample_count: 每次采样次数，用于求均值降噪，默认 10 次
            sample_interval_ms: 采样间隔，单位毫秒，默认 5ms
        """
        self.adc = ADC()
        self.adc_channel = self.adc.ADC1 if adc_channel is None else adc_channel
        self.ref_voltage = ref_voltage
        self.max_water_level = max_water_level
        self.warn_level = warn_level
        self.alert_level = alert_level
        self.sample_count = sample_count
        self.sample_interval_ms = sample_interval_ms
        self.is_running = False

    def open(self):
        """打开 ADC 通道。"""
        self.adc.open()

    def read_voltage(self):
        """多次采样求均值，降低 ADC 读取噪声。

        Returns:
            float: 平均电压值（ADC 原始读数的均值）
        """
        adc_sum = 0
        for _ in range(self.sample_count):
            adc_sum += self.adc.read(self.adc_channel)
            utime.sleep_ms(self.sample_interval_ms)
        return adc_sum / self.sample_count

    def read_level(self):
        """读取电压并换算为水位高度。

        换算公式：水位 = (电压均值 / 参考电压) × 最大量程

        注意：此公式假设电压与水位呈线性关系，实际应用中需根据传感器
        特性曲线进行标定校准。

        Returns:
            tuple: (电压均值, 水位高度 mm)
        """
        voltage_avg = self.read_voltage()
        water_level = (voltage_avg / self.ref_voltage) * self.max_water_level
        return voltage_avg, round(water_level, 2)

    def check_status(self, level):
        """根据水位高度判断当前状态。

        实际应用场景：水箱液位监测、漏水报警、洪水预警等。

        Args:
            level: 水位高度，单位 mm

        Returns:
            str: 状态描述（"正常" / "偏高警告" / "过高报警"）
        """
        if level < self.warn_level:
            return "正常"
        elif level < self.alert_level:
            return "偏高警告"
        else:
            return "过高报警"

    def monitor(self, interval_sec=1):
        """后台监控循环，持续采样并输出水位和状态。

        Args:
            interval_sec: 监控间隔，单位秒，默认 1 秒
        """
        self.is_running = True
        while self.is_running:
            voltage, level = self.read_level()
            status = self.check_status(level)
            print("水位: {:.2f} mm | 电压: {:.1f} | 状态: {}".format(level, voltage, status))
            utime.sleep(interval_sec)

    def start(self, interval_sec=1):
        """启动后台监控线程。

        Args:
            interval_sec: 监控间隔，单位秒，默认 1 秒
        """
        self.open()
        _thread.start_new_thread(self.monitor, (interval_sec,))

    def stop(self):
        """停止后台监控线程。"""
        self.is_running = False


if __name__ == '__main__':
    water_sensor = WaterLevelSensor(
        ref_voltage=3300,
        max_water_level=60,
        warn_level=15,
        alert_level=35,
        sample_count=10,
        sample_interval_ms=5,
    )
    water_sensor.start(interval_sec=1)

    # 主线程保持运行，等待后台监控
    while True:
        utime.sleep_ms(1000)