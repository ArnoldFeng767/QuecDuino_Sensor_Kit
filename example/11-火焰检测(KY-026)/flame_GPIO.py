from machine import Pin,ExtInt
import utime


# 配置GPIO为输入，下拉
gpio = Pin(Pin.GPIO31, Pin.IN, Pin.PULL_PD)
gpio1=Pin(Pin.GPIO30,Pin.OUT,Pin.PULL_DISABLE,0)
def main():
    # 传感器检测到火焰时输出高电平（1）
    while True:
        if gpio.read() == 0:
            gpio1.write(0)
        else:
            gpio1.write(1)
            print("检测到火焰")
        utime.sleep_ms(100)
if __name__ == "__main__":
    main()
        