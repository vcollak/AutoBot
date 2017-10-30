from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import logging
from settings import settings
import socket
import time
import json


class ControllerWebSocketServer(WebSocket):

    CLIENT_TYPE = "controller"
    host = ""
    port = ""
    soc = None
    
    
    def handleMessage(self):
        
        #host and port for the command server
        self.host = settings.Settings.HOST.value
        self.port = settings.Settings.PORT.value

        if not self.soc:
            self.soc = self.server_connect()
            
        if self.soc:
            
            try:

                packet_string = self.data

                logging.debug("Received: {}".format(packet_string))

                (command, client_type, packet_type, app_id, client_data) = self.get_commands(packet_string)

                if app_id != settings.Settings.APP_ID.value:
                    self.sendMessage("Wrong APP_ID. Unathorized client. Closing connection.")
                    return
                
                self.send_message(self.soc, self.generate_packet_string(packet_type,command))
                logging.debug("Sent: {}".format(packet_string))
                self.sendMessage("OK")

            except:
                self.sendMessage("ERROR")

                self.soc.close()
                self.soc = None
        else:
            
            logging.critical("Unable to connect to {}:{}".format(host, port))
            self.sendMessage("Unable to connect to {}:{}".format(host, port))

    def handleConnected(self):
        logging.info("Client {} connected".format(self.address))

    def handleClose(self):
        logging.info("Client {} disconnected".format(self.address))
        
    def get_commands(self,packet_string):
        
        try:

            input_from_client_object = json.loads(packet_string)
            
            command = input_from_client_object['command']
            client_type = input_from_client_object["client_type"]
            packet_type = input_from_client_object["packet_type"]
            app_id = input_from_client_object["app_id"]

        except:
            logging.warning("Incorrect protocol. Unable to extract commands")
            return

        return (command, client_type, packet_type, app_id, input_from_client_object)


    def generate_packet_string(self,packet_type,command):
        """ Return the JSON packet to be sent to the server. """

        app_id = settings.Settings.APP_ID.value

        packet_string = '{\"packet_type\":' + '\"' + packet_type + '\"' \
            + ',\"app_id\":' + '\"' + app_id + '\"' \
            + ',\"client_type\":' + '\"' + self.CLIENT_TYPE + '\"' \
            + ',\"command\":' + '\"' + command + '\"}'

        return packet_string

    def server_connect(self):
        """ Connects to the server and sends the initial hello packet. """
        packet_type = "hello"
        command = ""

        try:

            logging.info("Connecting to {}:{}".format(self.host, self.port))

            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
            self.soc.connect((self.host, self.port))

            logging.info("Connected")

            packet_string = self.generate_packet_string(packet_type, command)
            self.send_message(self.soc,packet_string)
            return self.soc

        except:
            logging.critical("Unable to connect to {}:{}".format(self.host, self.port))
            return

    def send_message(self,soc, packet_string):
            
        logging.debug("Sending {}".format(packet_string))
        soc.send(packet_string.encode("utf8")) # we must encode the string to bytes  
        result_bytes = soc.recv(4096) # the number means how the response can be in bytes  
        result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode
        logging.debug("Result from server is {}".format(result_string))

    
#set up loging
logging.basicConfig(level = settings.Settings.LOGGING_LEVEL.value)

#host and port for the websocker server
host = settings.Settings.HOST.value
port = settings.Settings.PORT.value

#start the web socket server used by the controller
server = SimpleWebSocketServer(host, port + 1, ControllerWebSocketServer)
logging.info("Server UP on {}:{}".format(host, port + 1))
server.serveforever()   
    

