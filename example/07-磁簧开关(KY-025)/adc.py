from misc import ADC
import _thread
import utime

def fun():
    while True:
        num=adc.read(adc.ADC0)
        utime.sleep(1)
        print(num)#输出的电压值会随着磁场强度的变化而线性改变


if __name__=='__main__':
    adc = ADC()
    adc.open()
    _thread.start_new_thread(fun,())