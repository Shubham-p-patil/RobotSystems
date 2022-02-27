
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
import cv2
# from vilib import Vilib

# Vilib.camera_start(True)
cap=cv2.VideoCapture(0)

if __name__ == "__main__":

    sensitivity = 200
    polarity = 1
    scale = 80
    runtime = 10
    speed = 40

    car = Picarx()
    method  = input("Line following or Lane Following(1 or 2):\n")
    if method == 1:
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
    else:
        control = Controller(car,scale)
        t = time.time()
        
        # for angle in range(0,-65,-1):
        #     car.set_camera_servo1_angle(angle)
        #     time.sleep(0.01)

        while time.time() - t < runtime:
            ret,frame=cap.read()
            control.camera_control(frame)
        car.stop()
        

