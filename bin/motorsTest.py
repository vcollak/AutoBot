

""" Tests the motors using the Pololu library 
The script sends forward and backward command to both motors
This script can be found: https://github.com/pololu/drv8835-motor-driver-rpi
"""

from __future__ import print_function
import time

#change path to app so we can call the vehicle class and settings
import os.path, sys
splitPath =  os.path.split(os.path.dirname(os.path.realpath(__file__)))
appPath = splitPath[0] + "/app"
sys.path.append(appPath)
sys.path.append(appPath + "/modules")
sys.path.append(appPath + "/settings")


from pololu_drv8835_rpi import motors, MAX_SPEED

# Set up sequences of motor speeds.
test_forward_speeds = list(range(0, MAX_SPEED, 1)) + \
  [MAX_SPEED] * 200 + list(range(MAX_SPEED, 0, -1)) + [0]  

test_reverse_speeds = list(range(0, -MAX_SPEED, -1)) + \
  [-MAX_SPEED] * 200 + list(range(-MAX_SPEED, 0, 1)) + [0]  

try:
    motors.setSpeeds(0, 0)

    print("Motor 1 forward")
    for s in test_forward_speeds:
        motors.motor1.setSpeed(s)
        time.sleep(0.005)

    print("Motor 1 reverse")
    for s in test_reverse_speeds:
        motors.motor1.setSpeed(s)
        time.sleep(0.005)

    print("Motor 2 forward")
    for s in test_forward_speeds:
        motors.motor2.setSpeed(s)
        time.sleep(0.005)

    print("Motor 2 reverse")
    for s in test_reverse_speeds:
        motors.motor2.setSpeed(s)
        time.sleep(0.005)

finally:
  # Stop the motors, even if there is an exception
  # or the user presses Ctrl+C to kill the process.
  motors.setSpeeds(0, 0)