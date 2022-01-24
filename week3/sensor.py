import sys,os

_path = os.getcwd() + '/lib'
sys.path.append(_path)


try :
    from adc import ADC

    from utils import reset_mcu
    reset_mcu()

    time . sleep (0.01)
except ImportError :
    print (" This computer does not appear to be a PiCar - X system ( ezblock is not present ) . Shadowing hardware calls with substitute functions ")
    from sim_ezblock import *
    

class Sensor(object):
    def __init__(self):
        self.chn_0 = ADC("A0")
        self.chn_1 = ADC("A1")
        self.chn_2 = ADC("A2")
        
    def get_grayscale_data(self):
        adc_value_list = []
        adc_value_list.append(self.chn_0.read())
        adc_value_list.append(self.chn_1.read())
        adc_value_list.append(self.chn_2.read())
        return adc_value_list


# if __name__ == "__main__":
#     import time
#     GM = Sensor(950)
#     while True:
#         print(GM.get_grayscale_data())
#         time.sleep(1)
