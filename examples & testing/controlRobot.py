
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
        try:
            motors.setSpeeds(MAX_SPEED, -MAX_SPEED)
        finally:
            self.vehicle_state = Vehicle_State.forward

    def backward(self):
        try:
            motors.setSpeeds(-MAX_SPEED, MAX_SPEED)
        finally:
            self.vehicle_state = Vehicle_State.backward
        
    def left(self):
        try:
            motors.setSpeeds(-100, -100)
        finally:
            self.vehicle_state = Vehicle_State.left
    
    def right(self):
        try:
            motors.setSpeeds(100, 100)
        finally:
            self.vehicle_state = Vehicle_State.right
    
    def stop(self):
        try:
            motors.setSpeeds(0, 0)
        finally:
            self.vehicle_state = Vehicle_State.stopped
        

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



