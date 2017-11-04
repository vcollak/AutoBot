""" Vehicle class. This gets commands and send them to motor driver """

from __future__ import print_function
import time
from pololu_drv8835_rpi import motors, MAX_SPEED
import threading
import logging
import settings
from settings import settings

class Vehicle(threading.Thread):
    """ Vehicle class interprests the commands and sends right messages to motor driver """
      
    COMMAND = ""
      
    def run(self):
        
        #set up logging
        logging.basicConfig(level = settings.Settings.LOGGING_LEVEL.value)
        
        logging.info("Started vehicle")

        while True:

            if self.COMMAND == "forward":
                self.forward_loop()

            elif self.COMMAND == "stop":
                self.stop_loop()

            elif self.COMMAND == "backward":
                self.backward_loop()

            elif self.COMMAND == "left":
                self.left_loop()

            elif self.COMMAND == "right":
                self.right_loop()
                
        

    def stop_loop(self):
        
        logging.info("Motor 1 and 2 stopped") 
        motors.setSpeeds(0, 0)

        #loop until we get another command. 
        while self.COMMAND == "stop":
            pass

    def forward_loop(self):
    
        motors.setSpeeds(0, 0)
        logging.info("Motor 1 and 2 forward") 

        initial_speeds = list(range(0, MAX_SPEED, 1)) 
        self.run_motors(initial_speeds, False)

        normal_speeds =  [MAX_SPEED] * 10

        #loop until we get a different command
        while self.COMMAND == "forward":
            self.run_motors(normal_speeds, False)

    def backward_loop(self):
    
        motors.setSpeeds(0, 0)
        logging.info("Motor 1 and 2 backward") 

        initial_speeds = list(range(0, -MAX_SPEED, -1)) 
        self.run_motors(initial_speeds, False)

        normal_speeds =  [-MAX_SPEED] * 10

        #loop until we get a different command
        while self.COMMAND == "backward":
            self.run_motors(normal_speeds, False)

    def left_loop(self):
       
        motors.setSpeeds(0, 0)
        logging.info("Motor Left") 

        initial_speeds = list(range(0, -150, -1)) 
        self.run_motors(initial_speeds, True)

        normal_speeds =  [-150] * 10

        #loop until we get a different command
        while self.COMMAND == "left":
            self.run_motors(normal_speeds, True)

    def right_loop(self):
       
        motors.setSpeeds(0, 0)
        logging.info("Motor Right") 

        initial_speeds = list(range(0, 150, 1)) 
        self.run_motors(initial_speeds, True)

        normal_speeds =  [150] * 10

        #loop until we get a different command
        while self.COMMAND == "right":
            self.run_motors(normal_speeds, True)

    def run_motors(self, speeds, same):
        for speed in speeds:
            if same:
                motors.motor1.setSpeed(speed)
                motors.motor2.setSpeed(speed)
            else:
                motors.motor1.setSpeed(speed)
                motors.motor2.setSpeed(-speed)
            
            time.sleep(0.005) 

  
