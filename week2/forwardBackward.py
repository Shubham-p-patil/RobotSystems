import sys,os
# sys.path.append(r'/home/pi/RobotSystems/lib')
_path = os.getcwd() + '/lib'
sys.path.append(_path)

import logging
from logdecorator import log_on_start , log_on_end , log_on_error
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

from picarx_improved import Picarx
import time


@log_on_start(logging.DEBUG, "Start maneuvering...")
@log_on_end(logging.DEBUG, "Motion executed successfully")
def forwardBackward():
    try:
        px = Picarx()
        
        px.forward(30)
        time.sleep(1)
        px.backward(30)
        time.sleep(1)

        px.forward(0)
        time.sleep(1)
    finally:
        px.forward(0)

if __name__ == "__main__":
    
    forwardBackward()