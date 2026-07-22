# 水位检测模块

## **一、** **模块介绍**

水位监测模块是**电阻式液体检测传感器**，用于检测水位高度、有无水、漏水报警等场景；通过导电探针检测液面变化，输出模拟，具备**响应快、体积小、3.3V兼容、直接接 ADC、使用寿命长**等优点。

**工作原理：**

Water Sensor水位传感器能够监测水位。该模块主要是利用三极管的电流放大原理：当液位高度使三极管的基极与电源正极导通的时候，在三极管的基极和发射极之间就会产生一定大小的电流，此时在三极管的集电极和发射极之间就会产生一个一定放大倍数的电流，该电流经过发射极的电阻产生特点电压，被AD转换器采集。

## 二、 连接示例

根据表格和图片指导，将外设与开发板一一对应连接

| 外设      | 开发板     |
| --------- | ---------- |
| 模块（+） | 3.3V       |
| 模块（-） | GND        |
| 模块（S） | A1（ADC1） |

![](../../media/water1.png)

## 三、 驱动代码

```python
from misc import ADC
import _thread
import utime


class WaterLevelSensor(object):
    """水位传感器类，通过 ADC 采集电压并换算为水位高度，支持分级报警与回调。

    状态分级：
        STATUS_NORMAL  (0): 正常
        STATUS_WARNING (1): 警告
        STATUS_ALERT   (2): 报警

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

    _STATUS_LABELS = {0: "正常", 1: "偏高警告", 2: "过高报警"}

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

    def set_callback(self, callback):
        """设置状态变化回调函数。

        Args:
            callback: 回调函数，签名 callback(level_mm, status_code, status_label)
        """
        self._callback = callback

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
        """获取状态码对应的中文标签。"""
        return cls._STATUS_LABELS.get(status_code, "未知")

    def _monitor(self, interval_sec):
        """后台监控循环，持续采样并输出水位和状态。"""
        while self._is_running:
            voltage, level = self.read_level()
            status = self.check_status(level)
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


if __name__ == '__main__':
    def on_status(level, status, label):
        if status == WaterLevelSensor.STATUS_ALERT:
            print("!!! 水位过高报警 !!!")

    sensor = WaterLevelSensor(
        ref_voltage=3300, max_water_level=60,
        warn_level=15, alert_level=35,
        sample_count=10, sample_interval_ms=5,
    )
    sensor.set_callback(on_status)
    sensor.start(interval_sec=1)

    while True:
        utime.sleep_ms(1000)
```

 