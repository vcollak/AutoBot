# server.py

import queue
import json
import logging
from settings import settings

"""
Protocol Payload 
client_type = "controller" | "robot"
packet_type = "setup" | "normal"
command = "forward" | "backward" | "left" | "right" | "stop"
"""


def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):

    def get_client_data():
        # the input is in bytes, so decode it
        input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)
        
        # MAX_BUFFER_SIZE is how big the message can be
        # this is test if it's sufficiently big
        import sys
        siz = sys.getsizeof(input_from_client_bytes)
        if  siz >= MAX_BUFFER_SIZE:
            logging.warning("The length of input is probably too long: {}".format(siz))

        # decode input and strip the end of line
        input_from_client = input_from_client_bytes.decode("utf8").rstrip()
        logging.debug("Received from client: {}".format(input_from_client))
        
        #start adding data to the queue and respond OK to client
        res = "ok"
        vysl = res.encode("utf8")  # encode the result string
        conn.sendall(vysl)  # send it to client

        return input_from_client

    def parse_client_data(input_from_client):
        
        try:
            input_from_client_object = json.loads(input_from_client)

        except:
            logging.warning("Incorrect protocol. Unable to parse JSON")
            return 

        return input_from_client_object

    def get_commands():
            
        input_from_client = get_client_data() 
        input_from_client_object = parse_client_data(input_from_client)           

        try:
            command = input_from_client_object['command']
            client_type = input_from_client_object["client_type"]
            packet_type = input_from_client_object["packet_type"]
            app_id = input_from_client_object["app_id"]

        except:
            logging.warning("Incorrect protocol. Unable to extract commands")
            return

        return (command, client_type, packet_type, app_id, input_from_client)  

    def send_quit_to_client():
        logging.info('Client ' + ip + ':' + port + " sent quit.")
        res = "ok"
        vysl = res.encode("utf8")  # encode the result string
        conn.sendall(vysl)  # send it to client
        conn.close()  # close connection
        logging.info('Connection ' + ip + ':' + port + ' ended')

    def robot_loop():
        
        logging.info(ip + ":" + port + " - robot connected")
            
        remain_in_loop = True
        while remain_in_loop:
            
            if q.qsize() > 0:
                logging.debug("Queue size: {}".format(q.qsize()))

            while not q.empty():
                
                data_from_queue = q.get()
                logging.debug("Sending from queue to robot: {}".format(data_from_queue))
                vysl = data_from_queue.encode("utf8")  # encode the result string

                try:
                    conn.sendall(vysl)  # send it to client

                except BrokenPipeError:
                    logging.critical("Unable to send to robot client. Broken pipe.")
                    remain_in_loop = False

    def controller_loop(command):
        
        logging.info(ip + ":" + port + " - controller connected")

        while command != "quit":
            
            try:
                #get commands from the client
                (command, client_type,packet_type, app_id, input_from_client) = get_commands()
            
            except:
                logging.error("Unable to parse commands")
                return command

            if command == "quit":
                return command

            #add to the queue
            if packet_type != "hello":
                q.put(input_from_client)

     
    
    try:

        #get commands from client
        (command, client_type,packet_type, app_id, input_from_client) = get_commands()

        if app_id != settings.Settings.APP_ID.value:
            logging.info("Wrong APP_ID. Unathorized client. Closing connection.")
            send_quit_to_client()
            return
            
        #loop until clients exits or fail
        if client_type == "robot":
            robot_loop()
        elif client_type == "controller":
            command = controller_loop(command)

        #either client can send "quit" to exit
        if command == "quit":    
            send_quit_to_client()

        logging.info("Exiting client {}:{}".format(ip,port))

    except ConnectionResetError:
        #TODO - need to handle this better. if the thread exists
        #should re-start it
        logging.error("Client {}:{} sent reset. Exiting...".format(ip, port))
    except:
        logging.error("Unable to parse client message. Closing connection.")
        send_quit_to_client()
      

def start_server():

    import socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    #no dely on TCP send
    soc.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    logging.debug("Socket started")
    
    try:
        
        host = settings.Settings.HOST.value
        port = settings.Settings.PORT.value

        soc.bind((host, port))
        logging.info("Server UP on {}:{}".format(host,port))
        

    except socket.error as msg:

        import sys
        logging.critical('Socket bind failed. Critical Error : ' + str(sys.exc_info()))
        logging.critical("Exiting...")
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    logging.info("Socket now accepting connections...")
    
    # for handling task in separate jobs we need threading
    from threading import Thread

    # this will make an infinite loop needed for 
    # not reseting server for every client
    while True:
        
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        logging.debug('Accepting connection from ' + ip + ':' + port)

        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            logging.error("Unable to create client_thread.")
            
            import traceback
            traceback.print_exc()

    soc.close()

#set up loging
logging.basicConfig(level = settings.Settings.LOGGING_LEVEL.value)

#server will use this queue to gather commands 
#from controllers and send to robots
q = queue.Queue()   

start_server()


