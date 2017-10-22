from __future__ import print_function
import time
from pololu_drv8835_rpi import motors, MAX_SPEED
import threading


class Vehicle(threading.Thread):
      
  COMMAND = ""
      
  def run(self):
        print("Started vehicle")

        while True:

          if self.COMMAND == "forward":
                self.forward()
          elif self.COMMAND == "stop":
                self.stop()
          elif self.COMMAND == "backward":
                self.backward()
          elif self.COMMAND == "left":
                self.left()
          elif self.COMMAND == "right":
                self.right()
              
        return

  def stop(self):

    print("Motor 1 and 2 stopped") 
    motors.setSpeeds(0, 0)

    while self.COMMAND == "stop":
      pass

  def forward(self):
    
    motors.setSpeeds(0, 0)
    print("Motor 1 and 2 forward") 

    initial_speeds = list(range(0, MAX_SPEED, 1)) 
    self.run_motors(initial_speeds, False)

    normal_speeds =  [MAX_SPEED] * 10
    while self.COMMAND == "forward":
      self.run_motors(normal_speeds, False)

  def backward(self):
    
    motors.setSpeeds(0, 0)
    print("Motor 1 and 2 backward") 

    initial_speeds = list(range(0, -MAX_SPEED, -1)) 
    self.run_motors(initial_speeds, False)

    normal_speeds =  [-MAX_SPEED] * 10
    while self.COMMAND == "backward":
      self.run_motors(normal_speeds, False)

  def left(self):
       
    motors.setSpeeds(0, 0)
    print("Left") 

    initial_speeds = list(range(0, -MAX_SPEED, -1)) 
    self.run_motors(initial_speeds, True)

    normal_speeds =  [-MAX_SPEED] * 10
    while self.COMMAND == "left":
      self.run_motors(normal_speeds, True)
  
  def right(self):
       
    motors.setSpeeds(0, 0)
    print("Right") 

    initial_speeds = list(range(0, MAX_SPEED, 1)) 
    self.run_motors(initial_speeds, True)

    normal_speeds =  [MAX_SPEED] * 10
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

  
