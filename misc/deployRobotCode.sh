#!/bin/sh

#Deplpys the code to the robot
scp ../clientRobot.py pi@192.168.1.44:/home/pi/robot/
scp ../modules/vehicle.py pi@192.168.1.44:/home/pi/robot/modules
scp ../modules/pololu_drv8835_rpi.py pi@192.168.1.44:/home/pi/robot/modules
scp ../settings/settings.py pi@192.168.1.44:/home/pi/robot/settings