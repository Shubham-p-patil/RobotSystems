import sys
sys.path.append(r'/home/pi/RobotSystems/lib')
from utils import reset_mcu
reset_mcu()

from picarx import Picarx     
import time

if __name__ == "__main__":
    wheel_direction = 1
    direction =1
    if direction == 'l':
        wheel_direction *= -1
    try:
        px = Picarx()

        px.forward(30)
        time.sleep(0.5)
        
        px.forward(0)
        time.sleep(1)

        for angle in range(0,wheel_direction*45,wheel_direction):
            px.set_dir_servo_angle(angle)
            time.sleep(0.01)   
        
        px.forward(0)
        time.sleep(1)

        px.backward(30)
        time.sleep(0.7)
        
        px.forward(0)
        time.sleep(1)

        for angle in range(wheel_direction*45,wheel_direction*-45,wheel_direction*-1):
            px.set_dir_servo_angle(angle)
            time.sleep(0.01)   
        
        px.forward(0)
        time.sleep(1)

        px.backward(20)
        time.sleep(0.7)
        
        px.forward(0)
        time.sleep(1)

        for angle in range(wheel_direction*-45,wheel_direction*45,wheel_direction):
            px.set_dir_servo_angle(angle)
            time.sleep(0.01)   
    
        px.forward(0)
        time.sleep(1)
        
        px.forward(30)
        time.sleep(0.3)   

        px.forward(0)
        time.sleep(1)
        
        for angle in range(wheel_direction*45,0,wheel_direction*-1):
            px.set_dir_servo_angle(angle)
            time.sleep(0.01)
        
        px.forward(0)
        time.sleep(1)
        
        px.forward(10)
        time.sleep(0.2)   

        px.forward(0)
        time.sleep(1)
    finally:
        px.forward(0)