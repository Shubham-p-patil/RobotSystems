import threading
import cv2
from rossros import *
from controller import InfraredController, UltrasonicController
from interpretation import InfraredInterpreter, UltrasonicInterpreter
from sensor import InfraredSensor, UltrasonicSensor
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
    thresh = 20
    car = Picarx()
    method = input("Line following or Lane Following(1 or 2):\n")
    if method == '1':
        infra_sensor = InfraredSensor()
        infra_interpreter = InfraredInterpreter(sensitivity, polarity)
        infra_control = InfraredController(car, scale)

        sonar_sensor = UltrasonicSensor()
        sonar_interpreter = UltrasonicInterpreter(thresh=thresh)
        sonar_control = UltrasonicController(speed=speed)

        t = time.time()
        while time.time() - t < runtime:
            readings = infra_sensor.get_grayscale_data()
            direction = infra_interpreter.processing_data(readings)
            angle = infra_control.control_car(direction)
            car.forward(speed=speed)

            # setup busses grayscale
            infra_sensor_values_bus = Bus(initial_message=[0, 0, 0],
                                          name="sensor values bus")
            infra_interpreter_bus = Bus(initial_message=0,
                                        name="sensor interpreter bus")

            # ultrasonic sensor busses
            sonar_values_bus = Bus(initial_message=0,
                                   name="ultrasonic sensor bus")
            sonar_interpreter_bus = Bus(initial_message=False,
                                        name="ultrasonic interpreter bus")

            # delay values (seconds)
            sensor_delay = 0.1
            interpreter_delay = 0.1
            control_delay = 0.1

            # grayscale sensor threads
            infra_read = Producer(infra_sensor.get_grayscale_data,
                                  output_busses=infra_sensor_values_bus,
                                  delay=0.09,
                                  name="Greyscale Sensor Reading")

            infra_interpret = ConsumerProducer(infra_interpreter.processing_data,
                                               input_busses=infra_sensor_values_bus,
                                               output_busses=infra_interpreter_bus,
                                               delay=0.1,
                                               name="Greyscale Sensor Processing")

            infra_control = Consumer(infra_control.control_car,
                                     input_busses=infra_interpreter_bus,
                                     delay=0.1,
                                     name="Greyscale Steering Controller")

            sonar_read = Producer(sonar_sensor.distance_reading,
                                  output_busses=sonar_values_bus,
                                  delay=0.09,
                                  name="Ultrasonic Sensor Reading")

            sonar_interpret = ConsumerProducer(sonar_interpreter.obstacle_detection_response,
                                               input_busses=sonar_values_bus,
                                               output_busses=sonar_interpreter_bus,
                                               delay=0.1,
                                               name="Ultrasonic  Sensor Processing")
            sonar_control = Consumer(sonar_control.avoid_obstacle,
                                     input_busses=sonar_interpreter_bus,
                                     delay=0.1,
                                     name="Ultrasonic Steering Controller")

            thread_list = [infra_read, infra_interpret, infra_control,
                           sonar_read, sonar_interpret, sonar_control]
            runConcurrently(thread_list)
        car.stop()
    else:
        control = InfraredController(car, scale)
        t = time.time()

        # for angle in range(0,-65,-1):
        #     car.set_camera_servo1_angle(angle)
        #     time.sleep(0.01)

        while time.time() - t < runtime:
            ret, frame = cap.read()
            control.camera_control(frame)
        car.stop()
