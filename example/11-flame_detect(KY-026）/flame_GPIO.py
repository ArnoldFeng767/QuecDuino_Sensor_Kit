from machine import Pin,ExtInt
import utime


# 配置GPIO为输入，上拉
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PU)
gpio1=Pin(Pin.GPIO30,Pin.OUT,Pin.PULL_DISABLE,0)
def main():
    # 假设传感器检测到火焰时输出低电平（0）
    while True:
        if gpio.read() == 0:
            gpio1.write(1)
            print("检测到火焰")
        else:
            gpio1.write(0)
            print("没有检测到火焰")
        utime.sleep(1)
if __name__ == "__main__":
    main()
        