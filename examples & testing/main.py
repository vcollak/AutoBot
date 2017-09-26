
from __future__ import print_function
import time
#from pi.motors import motors, MAX_SPEED
from pololu_drv8835_rpi import motors, MAX_SPEED
import click
import sys
from enum import Enum


class Vehicle_State(Enum):
    
    stopped  = 0
    forward  = 1
    backward = 2
    left     = 3
    right    = 4
    

class Vehicle:
    
    def __init__(self, *args, **kwargs):
        self.vehicle_state = Vehicle_State.stopped

    def forward(self):
        
        if self.vehicle_state == Vehicle_State.stopped:
            
            #accelrate and then full speed
            speeds = list(range(0,MAX_SPEED, 1)) + [MAX_SPEED] * 10

        elif self.vehicle_state == Vehicle_State.forward:
            
            #full speed
            speeds = [MAX_SPEED] * 10

        elif self.vehicle_state == Vehicle_State.backward:

            #decelrate, accelrate, then full speed
            speeds = list(range(MAX_SPEED, 0, -1)) + \
                list(range(0,MAX_SPEED, 1)) + [MAX_SPEED] * 10 + \
                [MAX_SPEED] * 10


        else:
            
            #if right ot left then stop, accelrate and full speed
            speeds = [0] + list(range(0,MAX_SPEED, 1)) + [MAX_SPEED] * 10

        try:

            print(speeds)

            for speed in speeds:
                motors.setSpeeds(speed, speed)
                time.sleep(0.005)
        
        finally:

            self.vehicle_state = Vehicle_State.forward



    def backward(self):
        self.vehicle_state = Vehicle_State.backward
        motors.setSpeeds(0, 0)

    def left(self):
        self.vehicle_state = Vehicle_State.left
        motors.setSpeeds(0, 0)

    def right(self):
        self.vehicle_state = Vehicle_State.right
        motors.setSpeeds(0, 0)

    def stop(self):
        self.vehicle_state = Vehicle_State.stopped
        motors.setSpeeds(0, 0)
        

vehicle = Vehicle()


print("w = forward   s = backward   a = left   d = right   x = stop   q = quit")
print()

while True:
    key = click.getchar()

    if key == "w":
        print ("forward")
        vehicle.forward()

    elif key == "s":
        print ("backward")
        vehicle.backward()

    elif key == "a":
        print ("left")
        vehicle.left()

    elif key == "d":
        print ("right")
        vehicle.right()

    elif key == "x" :
        print ("stop")
        vehicle.stop()
        
    elif key == "q":
        sys.exit()



