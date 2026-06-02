# Obstacle Detection Module

## 1. Module Introduction

The obstacle detection module is an infrared reflective digital detection device, also known as an infrared obstacle avoidance module, which is used for short-distance obstacle detection, tracking, obstacle avoidance, and limit triggering; it judges whether there is an obstacle in front through infrared emission and reception, with advantages such as fast response, small size, 3.3V/5V compatibility, direct GPIO reading, strong anti-interference, and long service life.

**Module Composition:**

![](../../media/obstacle1.png)

**Working Principle:**

The working principle is that the infrared light emitting tube **emits infrared light**, and the infrared light receiving tube **receives infrared light**. When **no reflected infrared light is received**, the OUT pin outputs **high level**; when **reflected infrared light is received**, the OUT pin outputs **low level**.

## 2. Connection Example

Connect the peripherals to the development board one by one according to the table and picture instructions

| Peripheral  | Development Board |
| ----------- | ----------------- |
| Module（+） | 3.3V              |
| Module（-） | GND               |
| Module（S） | PIN4(GPIO31)      |

![](../../media/obstacle2.png)

## 3.Driver Code

```python
from machine import Pin, ExtInt
import utime

# KY-032 Pin Description:
#   VCC: 3.3-5V
# GND: Ground
#   OUT: Digital Output (No Obstacle = High Level 1, Obstacle Present = Low Level 0)
#   EN: Enable Pin (Optional, default enabled when floating)
# Note: There are two potentiometers on the module to adjust the detection distance and sensitivity

# Configure GPIO as input, pull-up
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)

# ==================== Polling Mode ====================
def main_polling():
    print("KY-032 obstacle avoidance sensor (polling mode)")
    while True:
        if gpio.read() == 0:
            print("Obstacle detected")
        else:
            print("No Obstacles")
        utime.sleep_ms(200)


# ==================== Interrupt Mode ====================
obstacle_flag = False

def irq_handler(args):
    global obstacle_flag
    if gpio.read() == 0:
        obstacle_flag = True

def main_interrupt():
    global obstacle_flag
    ext = ExtInt(ExtInt.GPIO31, ExtInt.IRQ_FALLING, ExtInt.PULL_PU, irq_handler)
    ext.enable()
    print("KY-032 obstacle avoidance sensor (interrupt mode)")
    while True:
        if obstacle_flag:
            print("Obstacle detected")
            obstacle_flag = False
        else:
            print("No Obstacles")
        utime.sleep_ms(200)


if __name__ == '__main__':
    main_polling()
    # main_interrupt()  # Switch to interrupt mode

```

 