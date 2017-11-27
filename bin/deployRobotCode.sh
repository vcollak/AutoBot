#!/bin/sh
# Scirpt will deploy the robot code to RAspberry PI. It assumes that 
# the modules and settings directories already exist there
#
# Example Paramters: 
# HOST="192.168.1.44"
# USER="pi"
# DESTPATH="/home/pi/robot"

#Deplpys the code to the robot

if [ "$#" -eq 3 ]
then

    scp ../app/clientRobot.py $USER@$HOST:$DESTPATH
    scp ../app/modules/vehicle.py $USER@$HOST:$DESTPATH
    scp ../app/modules/pololu_drv8835_rpi.py $USER@$HOST:$DESTPATH/modules
    scp ../app/settings/settings.py $USER@$HOST:$DESTPATH/settings

else
    echo "Usage: $0 Host User DestinationPath"
    exit 1
fi