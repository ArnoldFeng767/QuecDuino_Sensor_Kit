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
    """水位传感器类，通过 ADC 采集电压并换算为水位高度，支持分级报警与回调。

    状态分级：
        STATUS_NORMAL  (0): 正常
        STATUS_WARNING (1): 警告
        STATUS_ALERT   (2): 报警

    典型用法:
        sensor = WaterLevelSensor(warn_level=15, alert_level=35)
        def on_alert(level, status):
            print("报警! 水位 {}mm".format(level))
        sensor.set_callback(on_alert)
        sensor.start()

    Args:
        adc_channel:       ADC 通道，默认 ADC1
        ref_voltage:       参考电压 mV，默认 3300（3.3V）
        max_water_level:   传感器最大量程 mm，默认 60
        warn_level:        警告水位阈值 mm，默认 15
        alert_level:       报警水位阈值 mm，默认 35
        sample_count:      单次采样次数（均值降噪），默认 10
        sample_interval_ms: 采样间隔 ms，默认 5
    """

    STATUS_NORMAL = 0
    STATUS_WARNING = 1
    STATUS_ALERT = 2

    _STATUS_LABELS = {
        0: "正常",
        1: "偏高警告",
        2: "过高报警",
    }

    def __init__(self, adc_channel=None, ref_voltage=3300, max_water_level=60,
                 warn_level=15, alert_level=35,
                 sample_count=10, sample_interval_ms=5):
        self._adc = ADC()
        self._adc_channel = self._adc.ADC1 if adc_channel is None else adc_channel
        self._ref_voltage = ref_voltage
        self._max_water_level = max_water_level
        self._warn_level = warn_level
        self._alert_level = alert_level
        self._sample_count = sample_count
        self._sample_interval_ms = sample_interval_ms
        self._callback = None
        self._is_running = False
        self._last_level = 0
        self._last_voltage = 0.0
        self._last_status = self.STATUS_NORMAL

    # ---- 回调 ----

    def set_callback(self, callback):
        """设置状态变化回调函数。

        Args:
            callback: 回调函数，签名 callback(level_mm, status_code, status_label)
        """
        self._callback = callback

    # ---- 阈值 ----

    @property
    def warn_level(self):
        return self._warn_level

    @warn_level.setter
    def warn_level(self, value):
        self._warn_level = value

    @property
    def alert_level(self):
        return self._alert_level

    @alert_level.setter
    def alert_level(self, value):
        self._alert_level = value

    # ---- 读取 ----

    def read_voltage(self):
        """多次采样求均值，降低 ADC 读取噪声。

        Returns:
            float: 平均 ADC 值
        """
        adc_sum = 0
        for _ in range(self._sample_count):
            adc_sum += self._adc.read(self._adc_channel)
            utime.sleep_ms(self._sample_interval_ms)
        return adc_sum / self._sample_count

    def read_level(self):
        """读取电压并换算为水位高度（单次，不启动监控）。

        换算公式：水位 = (电压均值 / 参考电压) × 最大量程

        Returns:
            tuple: (电压均值, 水位 mm)
        """
        voltage_avg = self.read_voltage()
        water_level = (voltage_avg / self._ref_voltage) * self._max_water_level
        return voltage_avg, round(water_level, 2)

    # ---- 状态 ----

    def check_status(self, level):
        """根据水位判断状态码。

        Args:
            level: 水位高度 mm

        Returns:
            int: STATUS_NORMAL / STATUS_WARNING / STATUS_ALERT
        """
        if level < self._warn_level:
            return self.STATUS_NORMAL
        elif level < self._alert_level:
            return self.STATUS_WARNING
        else:
            return self.STATUS_ALERT

    @classmethod
    def status_label(cls, status_code):
        """获取状态码对应的中文标签。

        Args:
            status_code: STATUS_NORMAL / STATUS_WARNING / STATUS_ALERT

        Returns:
            str: 状态标签
        """
        return cls._STATUS_LABELS.get(status_code, "未知")

    # ---- 监控 ----

    def _monitor(self, interval_sec):
        """后台监控循环，持续采样并输出水位和状态。"""
        while self._is_running:
            voltage, level = self.read_level()
            status = self.check_status(level)
            self._last_voltage = voltage
            self._last_level = level
            self._last_status = status

            label = self.status_label(status)
            print("水位: {:.2f} mm | 电压: {:.1f} | 状态: {}".format(level, voltage, label))

            if self._callback:
                self._callback(level, status, label)

            utime.sleep(interval_sec)

    def start(self, interval_sec=1):
        """启动 ADC 并开启后台监控线程。

        Args:
            interval_sec: 监控间隔，单位秒，默认 1s
        """
        self._adc.open()
        self._is_running = True
        _thread.start_new_thread(self._monitor, (interval_sec,))

    def stop(self):
        """停止后台监控线程。"""
        self._is_running = False


# ---- 独立运行测试 ----
if __name__ == '__main__':
    def on_status(level, status, label):
        if status == WaterLevelSensor.STATUS_ALERT:
            print("!!! 水位过高报警 !!!")

    sensor = WaterLevelSensor(
        ref_voltage=3300,
        max_water_level=60,
        warn_level=15,
        alert_level=35,
        sample_count=10,
        sample_interval_ms=5,
    )
    sensor.set_callback(on_status)
    sensor.start(interval_sec=1)

    while True:
        utime.sleep_ms(1000)
