""" Main Robot client code. This connects to the server and receive commands from the server """

import socket
import json
from modules.vehicle import Vehicle
from settings import settings
import logging
import sys
import time

CLIENT_TYPE = "robot"
SLEEP_TIME = 15

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
        logging.debug("Sending {}".format(packet_string))
        soc.send(packet_string.encode("utf8")) # we must encode the string to bytes  

        result_bytes = soc.recv(4096) # the number means how the response can be in bytes  
        result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode
        logging.debug("Result from server is {}".format(result_string))  

        return soc

    except:
        logging.critical("Unable to connect to {}:{}".format(host, port))
        return


def robot_loop(soc, vehicle):
    """ Main loop. This will loop forever and send commands to the Vehicle """
    
    while True:
        
        try:
            result_bytes = soc.recv(4096) # the number means how the response can be in bytes  
            result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode
            logging.debug("Result from server is {}".format(result_string))  
            server_object = json.loads(result_string)
            command = server_object['command']
            vehicle.COMMAND = command

        except:
            logging.error("Unable to receive command from the server" + str(sys.exc_info()))
            break

        
def generate_packet_string(packet_type,command):
    """ Return the JSON packet to be sent to the server. """
    
    app_id = settings.Settings.APP_ID.value
    
    packet_string = '{\"packet_type\":' + '\"' + packet_type + '\"' \
        + ',\"app_id\":' + '\"' + app_id + '\"' \
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
        
        else:
            logging.error("Unable to connect to {}:{}. Retrying after {} secs...".format(host, port,SLEEP_TIME))
            time.sleep(SLEEP_TIME)



if __name__ == "__main__":
    main()
