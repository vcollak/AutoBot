#!/bin/sh

scp robotClient.py pi@192.168.1.44:/home/pi/robot/drv8835-motor-driver-rpi/
scp modules/vehicle.py pi@192.168.1.44:/home/pi/robot/drv8835-motor-driver-rpi/modules
scp settings/settings.py pi@192.168.1.44:/home/pi/robot/drv8835-motor-driver-rpi/settings