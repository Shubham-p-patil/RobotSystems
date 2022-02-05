
import threading
import cv2
from bus import Bus
from controller import Controller
from interpretation import Interpretation
from sensor import Sensor
from picarx_improved import Picarx
import concurrent.futures
import time
import sys
import os

_path = os.getcwd() + '/lib'
sys.path.append(_path)

_stop_requested = threading.Event()

# from utils import reset_mcu
# reset_mcu()


# from vilib import Vilib

# Vilib.camera_start(True)
cap = cv2.VideoCapture(0)


def sigint_handler(sig, frame):
    global _stop_requested
    _stop_requested.set()


if __name__ == "__main__":

    sensitivity = 200
    polarity = 1
    scale = 80
    runtime = 10
    speed = 40

    car = Picarx()
    method = input("Line following or Lane Following(1 or 2):\n")
    if method == '1':
        sensor = Sensor()
        interpreter = Interpretation(sensitivity, polarity)
        control = Controller(car, scale)
        t = time.time()
        while time.time() - t < runtime:
            readings = sensor.get_grayscale_data()
            direction = interpreter.processing_data(readings)
            angle = control.control_car(direction)
            car.forward(speed=speed)

            sensor_values_bus = Bus()
            interpreter_bus = Bus()

            # delay values (seconds)
            sensor_delay = 0.1
            interpreter_delay = 0.1
            control_delay = 0.1

            with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
                eSensor = executor.submit(
                    sensor.read_sensordata_concurrently, sensor_values_bus, sensor_delay, _stop_requested)
                eInterpreter = executor.submit(interpreter.interpret_data_concurrently,
                                               sensor_values_bus, interpreter_bus, interpreter_delay, _stop_requested)
                eController = executor.submit(
                    control.control_car_concurrently, interpreter_bus, control_delay, _stop_requested)
                eSensor.result()
        car.stop()
    else:
        control = Controller(car, scale)
        t = time.time()

        # for angle in range(0,-65,-1):
        #     car.set_camera_servo1_angle(angle)
        #     time.sleep(0.01)

        while time.time() - t < runtime:
            ret, frame = cap.read()
            control.camera_control(frame)
        car.stop()
