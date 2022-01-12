import sys
sys.path.append(r'/home/pi/RobotSystems/lib')

import logging
from logdecorator import log_on_start , log_on_end , log_on_error
logging_format = "%( asctime ) s : %( message ) s "
logging.basicConfig( format = logging_format , level = logging.INFO , datefmt ="% H :% M :% S ")
logging.getLogger().setLevel( logging.DEBUG )

from utils import reset_mcu
reset_mcu()

from picarx import Picarx
import time


@log_on_start(logging.DEBUG, "Start maneuvering...")
@log_on_end(logging.DEBUG, "Motion executed successfully")
def forwardBackward():
    try:
        px = Picarx()
        
        px.forward(30)
        time.sleep(0.5)
        px.backward(30)
        time.sleep(0.5)

        px.forward(0)
        time.sleep(1)
    finally:
        px.forward(0)

if __name__ == "__main__":

    forwardBackward()