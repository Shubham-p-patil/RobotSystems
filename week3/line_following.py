
import sys,os

_path = os.getcwd() + '/lib'
sys.path.append(_path)

import time

# from utils import reset_mcu
# reset_mcu()

from picarx_improved import Picarx

from sensor import Sensor
from interpretation import Interpretation
from controller import Controller

if __name__ == "__main__":

    sensitivity = 200
    polarity = 1
    scale = 80
    runtime = 10
    speed = 40

    car = Picarx()
    sensor = Sensor()
    interpreter = Interpretation(sensitivity, polarity)
    control = Controller(car,scale)

    t = time.time()
    while time.time() - t < runtime:
        readings = sensor.get_grayscale_data()
        direction = interpreter.processing(readings)
        angle = control.control_car(direction)
        car.forward(speed=speed)
    car.stop()