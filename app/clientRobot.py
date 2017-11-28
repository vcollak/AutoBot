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

""" Main Robot client code. This sits on the robot, connects to the server, 
and receive commands from the server 
"""

import socket
import json
import logging
import sys
import time

from modules.vehicle import Vehicle
from settings import settings

CLIENT_TYPE = "robot"
SLEEP_TIME = 15


HOST = settings.Settings.HOST_REMOTE.value
PORT = settings.Settings.PORT.value
APP_ID = settings.Settings.APP_ID.value

logging.basicConfig(level = settings.Settings.LOGGING_LEVEL.value)

def connect():
    """ Connects to the server and sends the initial hello packet. """
    packet_type = "hello"
    command = ""

    try:

        logging.info("Connecting to {}:{}".format(HOST, PORT))

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        soc.connect((HOST, PORT))

        logging.info("Connected")

        packet_string = generate_packet_string(packet_type, command)
        logging.debug("Sending {}".format(packet_string))
        soc.send(packet_string.encode("utf8")) # we must encode the string to bytes  

        result_bytes = soc.recv(4096) # the number means how the response can be in bytes  
        result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode
        logging.debug("Result from server is {}".format(result_string))  

        return soc

    except:
        logging.critical("Unable to connect to {}:{}".format(HOST, PORT))
        return


def robot_loop(soc, vehicle):
    """ Main loop. This will loop forever and send commands to the Vehicle """
    
    while True:
        
        try:
            logging.debug("Start Loop and wait for command...")
            result_bytes = soc.recv(4096) # the number means how the response can be in bytes  
            result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode
            logging.debug("Result from server is {}".format(result_string))  
            server_object = json.loads(result_string)
            command = server_object['command']
            vehicle.COMMAND = command
            time.sleep(0.1) 

        except:
            logging.error("Unable to receive command from the server" + str(sys.exc_info()))
            break

        
def generate_packet_string(packet_type,command):
    """ Return the JSON packet to be sent to the server. """
    
    packet_string = '{\"packet_type\":' + '\"' + packet_type + '\"' \
        + ',\"app_id\":' + '\"' + APP_ID + '\"' \
        + ',\"client_type\":' + '\"' + CLIENT_TYPE + '\"' \
        + ',\"command\":' + '\"' + command + '\"}'

    return packet_string

def main():
    """ Main function. It will connect, access the vehicle and loop for commands from the server."""
    
    vehicle = Vehicle()
    vehicle.start()

    while True:
        
        #connect to the server
        soc = connect() 

        if soc:
            
            #will loop until disconnected or fatal error
            robot_loop(soc, vehicle)
            time.sleep(0.1) 
        
        else:
            logging.error("Unable to connect to {}:{}. Retrying after {} secs...".format(HOST, PORT,SLEEP_TIME))
            time.sleep(SLEEP_TIME)



if __name__ == "__main__":
    main()
