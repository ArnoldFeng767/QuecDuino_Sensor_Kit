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
from machine import Pin
import _thread
import utime
# 传感器参数配置
REF_VOLTAGE = 3300       # 参考电压 (mV)，3.3V供电为3300，5V供电为5000
MAX_WATER_LEVEL = 60     # 最大水位量程 (mm)，Water Sensor检测面积高度为60mm
SAMPLE_COUNT = 10        # 均值滤波采样次数
SAMPLE_INTERVAL_MS = 5   # 每次采样间隔 (ms)

def water_level_get(adc):
    """
    获取水位值 (mm)
    通过多次ADC采样取均值滤波，再换算为实际水位深度
    公式: water_level = (voltage / ref_voltage) * max_water_level
    """
    adc_sum = 0
    for _ in range(SAMPLE_COUNT):
        adc_sum += adc.read(adc.ADC1)
        utime.sleep_ms(SAMPLE_INTERVAL_MS)
    voltage_avg = adc_sum / SAMPLE_COUNT  # 平均电压值 (mV)

    water_level = (voltage_avg / REF_VOLTAGE) * MAX_WATER_LEVEL
    return voltage_avg, round(water_level, 2)


def fun():
    while True:
        voltage, level = water_level_get(adc)
        print("电压: {:.1f} mV | 水位: {:.2f} mm".format(voltage, level))
        utime.sleep(1)


if __name__ == '__main__':
    adc = ADC()
    adc.open()
    _thread.start_new_thread(fun, ())


```

 