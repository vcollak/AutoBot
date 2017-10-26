from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import logging
from settings import settings
import socket
import time


class ControllerWebSocketServer(WebSocket):

    CLIENT_TYPE = "controller"
    
    def handleMessage(self):
        # echo message back to client
        self.sendMessage(self.data)
        
        packet_string = generate_packet_string("normal", self.data)
        send_message(soc, packet_string)
        logging.debug("Sent: {}".format(packet_string))

        logging.warn(self.data)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')
    
def generate_packet_string(packet_type,command):
    """ Return the JSON packet to be sent to the server. """

    app_id = settings.Settings.APP_ID.value

    packet_string = '{\"packet_type\":' + '\"' + packet_type + '\"' \
        + ',\"app_id\":' + '\"' + app_id + '\"' \
        + ',\"client_type\":' + '\"' + CLIENT_TYPE + '\"' \
        + ',\"command\":' + '\"' + command + '\"}'

    return packet_string

def server_connect():
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

#set up loging
logging.basicConfig(level = settings.Settings.LOGGING_LEVEL.value)

host = settings.Settings.HOST.value
port = settings.Settings.PORT.value

CLIENT_TYPE = "controller"

soc = server_connect()

#start the web socket server used by the controller
server = SimpleWebSocketServer(host, port + 1, ControllerWebSocketServer)
server.serveforever()   
