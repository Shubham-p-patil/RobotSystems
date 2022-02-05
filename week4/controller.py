import time
import os
import sys

_path = os.getcwd() + '/lib'
sys.path.append(_path)

from picarx_opencv import *

class Controller():
    def __init__(self,px,scaling_factor=40):
        self.sf = scaling_factor
        self.px = px
        
    def control_car(self,pos):
        try:
            self.px.set_dir_servo_angle(pos*self.sf)
            self.px.forward(40)
            time.sleep(0.1)
        finally:
            self.px.stop()

        
    def camera_control(self,frame):
        try:
            lane_lines=detect_lane(frame)
            frame_shape=frame.shape
            angle,lines = calculate_heading(lane_lines,frame_shape[1],frame_shape[0])
            angle_to_deg = int((angle*180)/3.14)
            self.px.set_dir_servo_angle(angle_to_deg*0.7)
            self.px.forward(15)
            time.sleep(0.1)
        except:
            self.px.stop()

    def control_car_concurrently(self,bus, delay, kill_thread):
        while not kill_thread.is_set():
            self.control_car(bus.read())
            time.sleep(delay)