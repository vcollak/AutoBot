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

""" Tests server code by mimicking what the controller calls
    Can call any commands, but should test with: forward, backward, left, right, stop
 """

import socket
import json
import logging

#change path to root so we can call settings
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from settings import settings
import time


CLIENT_TYPE = "controller"
SLEEP_TIME = 5

host = settings.Settings.HOST.value
port = settings.Settings.PORT.value
app_id = settings.Settings.APP_ID.value

logging.basicConfig(level = settings.Settings.LOGGING_LEVEL.value)

def connect():
    """ Connects to the server and sends the initial hello packet. """
    packet_type = "hello"
    command = ""

    try:

        logging.info("Connecting to {}:{}".format(host, port))

        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        soc.connect((host, port))

        logging.info("Connected")

        packet_string = generate_packet_string(packet_type, command)
        send_message(soc,packet_string)
        return soc

    except:
        logging.critical("Unable to connect to {}:{}".format(host, port))
        return

def send_message(soc, packet_string):
    
    logging.debug("Sending {}".format(packet_string))
    soc.send(packet_string.encode("utf8")) # we must encode the string to bytes  
    result_bytes = soc.recv(4096) # the number means how the response can be in bytes  
    result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode
    logging.debug("Result from server is {}".format(result_string)) 


def generate_packet_string(packet_type,command):
    """ Return the JSON packet to be sent to the server. """
    
    app_id = settings.Settings.APP_ID.value
    
    packet_string = '{\"packet_type\":' + '\"' + packet_type + '\"' \
        + ',\"app_id\":' + '\"' + app_id + '\"' \
        + ',\"client_type\":' + '\"' + CLIENT_TYPE + '\"' \
        + ',\"command\":' + '\"' + command + '\"}'

    return packet_string

def main():
    
    loop = True

    print ("Commands: forward, backward, left, right, stop")
    print ("Enter: 'exit' to exit the script")
    print()
    print()
    
    
    while loop:

        soc = connect()

        if soc:
            
            while loop:
                
                try:

                    print()
                    command = input("Enter command ('exit' to quit):\n") 

                    if command == "exit":
                        logging.info("Exiting...")
                        loop = False
                        break

                    packet_string = generate_packet_string("normal", command)
                    send_message(soc, packet_string)
                    logging.debug("Sent: {}".format(packet_string))

                except:
                    
                    logging.critical("Unable to send message.")
                    break

        else:
            
            logging.error("Unable to connect to {}:{}. Retrying after {} secs...".format(host, port, SLEEP_TIME))
            time.sleep(SLEEP_TIME)


        
if __name__ == "__main__":
    main()