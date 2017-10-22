""" Main Controller client code. Sends commands to server for the robot """

import socket
import json
import logging
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
    
    while True:

        soc = connect()

        if soc:
            
            while True:
                
                try:

                    command = input("Enter command:\n") 
                    packet_string = generate_packet_string("normal", command)
                    send_message(soc, packet_string)

                except:
                    
                    logging.critical("Unable to send message.")
                    break

        else:
            
            logging.error("Unable to connect to {}:{}. Retrying after {} secs...".format(host, port, SLEEP_TIME))
            time.sleep(SLEEP_TIME)


        
if __name__ == "__main__":
    main()