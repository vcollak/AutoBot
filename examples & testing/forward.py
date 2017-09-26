
from __future__ import print_function
import time
#from pi.motors import motors, MAX_SPEED
from pololu_drv8835_rpi import motors, MAX_SPEED
import click
import sys
from enum import Enum

    

try:

    """
    speeds_forward = [MAX_SPEED]
    
    print (speeds_forward)
    

    for speeds_forward in speeds_forward:
        motors.setSpeeds(speeds_forward, - speeds_forward)
        time.sleep(0.005)
    """
    motors.setSpeeds(480, -480)

finally:
    pass
    
time.sleep(0.5)
motors.setSpeeds(0,0)
