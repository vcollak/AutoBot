###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Vladimir Collak
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

""" 
Vehicle class. The class is used by robotClient.py to get the commands
(forward, bacward, left, right, stop) and send the appropriate signals to 
the Pololu motor drive. The class assumes 2 motors

Todo:
    * extend, so the class can support 4 motors

"""



from __future__ import print_function
import time
import threading
import logging

from modules.pololu_drv8835_rpi import motors, MAX_SPEED
import settings
from settings import settings

class Vehicle(threading.Thread):
    """ Vehicle class interprests the commands and sends right messages to motor driver """
      
    COMMAND = ""
      
    def run(self):
        """ Runs when the vehicle start is called """
        
        #set up logging
        logging.basicConfig(level = settings.Settings.LOGGING_LEVEL.value)
        
        logging.info("Started vehicle")

        while True:

            if self.COMMAND == "forward":
                self._forward_loop()

            elif self.COMMAND == "stop":
                self._stop_loop()

            elif self.COMMAND == "backward":
                self._backward_loop()

            elif self.COMMAND == "left":
                self._left_loop()

            elif self.COMMAND == "right":
                self._right_loop()
            
            time.sleep(0.1)  
        

    def _stop_loop(self):
        """ User called stop. Loop while it's still a stop command """

        logging.info("Motor 1 and 2 stopped") 
        motors.setSpeeds(0, 0)

        #loop until we get another command. 
        while self.COMMAND == "stop":
            time.sleep(0.1) 

    def _forward_loop(self):
        """ User called forward. Loop while it's still a forward command """
    
        #stop the motors
        motors.setSpeeds(0, 0)
        logging.info("Motor 1 and 2 forward") 

        #ramp up from 0 to MAX_SPEED
        initial_speeds = list(range(0, MAX_SPEED, 1)) 
        self._run_motors(initial_speeds, False, self.COMMAND)

        #MAX_SPEED 10 times
        normal_speeds =  [MAX_SPEED] * 10

        #loop until we get a different command
        while self.COMMAND == "forward":
            self._run_motors(normal_speeds, False,self.COMMAND)
            time.sleep(0.1) 

    def _backward_loop(self):
        """ User called backward. Loop while it's still a backward command """
    
        #stop motors
        motors.setSpeeds(0, 0)
        logging.info("Motor 1 and 2 backward") 

        #ramp up to MAX_SPEED
        initial_speeds = list(range(0, -MAX_SPEED, -1)) 
        self._run_motors(initial_speeds, False,self.COMMAND)

        #max speed 10 times
        normal_speeds =  [-MAX_SPEED] * 10

        #loop until we get a different command
        while self.COMMAND == "backward":
            self._run_motors(normal_speeds, False,self.COMMAND)
            time.sleep(0.1) 

    def _left_loop(self):
        """ User called left. Loop while it's still a left command """
       
        #stop motors
        motors.setSpeeds(0, 0)
        logging.info("Motor Left") 

        #ramp up to 75. Slower than MAX_SPEED
        initial_speeds = list(range(0, -75, -1)) 
        self._run_motors(initial_speeds, True,self.COMMAND)

        #10 more times at 75
        normal_speeds =  [-75] * 10

        #loop until we get a different command
        while self.COMMAND == "left":
            self._run_motors(normal_speeds, True,self.COMMAND)
            time.sleep(0.1) 

    def _right_loop(self):
        """ User called right. Loop while it's still a right command """
       
        #stop motors
        motors.setSpeeds(0, 0)
        logging.info("Motor Right") 

        #ramp up to 75
        initial_speeds = list(range(0, 75, 1)) 
        self._run_motors(initial_speeds, True,self.COMMAND)

        #75 10 times
        normal_speeds =  [75] * 10

        #loop until we get a different command
        while self.COMMAND == "right":
            self._run_motors(normal_speeds, True,self.COMMAND)
            time.sleep(0.1) 

    def _run_motors(self, speeds, same, command):
        """ Runs both motors given the speeds list and instructions 
        
        Args:
            speeds (list): List of speeds to send to motors
            same (Boolean): If same, both motors will run in the same direction.
                this actually makes them spin oposite so the vehicle will turn.
                If not the same the vehicle will go forward or backward - depending
                on in speeds are positive or negative
        """

        for speed in speeds:
            if same:
                motors.motor1.setSpeed(speed)
                motors.motor2.setSpeed(speed)
            else:
                motors.motor1.setSpeed(speed)
                motors.motor2.setSpeed(-speed)
            
            time.sleep(0.005) 

            if command != self.COMMAND:
                logging.debug("Detected command chage. Existing run_motors loop.")
                break

  
