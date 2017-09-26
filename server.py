# server.py

import queue
import json

"""
Protocol Payload 
client_type = "controller" | "robot"
packet_type = "setup" | "normal"
command = "forward" | "backward" | "left" | "right" | "stop"
"""

APP_ID = "123adalsdjfhaldfjkahl234234234"

def client_thread(conn, ip, port, MAX_BUFFER_SIZE = 4096):
    

    def get_client_data():
        # the input is in bytes, so decode it
        input_from_client_bytes = conn.recv(MAX_BUFFER_SIZE)

        # MAX_BUFFER_SIZE is how big the message can be
        # this is test if it's sufficiently big
        import sys
        siz = sys.getsizeof(input_from_client_bytes)
        if  siz >= MAX_BUFFER_SIZE:
            print("The length of input is probably too long: {}".format(siz))

        # decode input and strip the end of line
        input_from_client = input_from_client_bytes.decode("utf8").rstrip()
        print ("From client: {}".format(input_from_client))

        #start adding data to the queue and respond OK to client
        res = "ok"
        vysl = res.encode("utf8")  # encode the result string
        conn.sendall(vysl)  # send it to client

        return input_from_client

    def parse_client_data(input_from_client):
        
        try:
            input_from_client_object = json.loads(input_from_client)
        except:
            print("Incorrect protocol. Unable to pars JSON") 

        return input_from_client_object
    


    try:

        input_from_client = get_client_data() 
        input_from_client_object = parse_client_data(input_from_client)           

        try:
            command = input_from_client_object['command']
            client_type = input_from_client_object["client_type"]
            packet_type = input_from_client_object["packet_type"]
            app_id = input_from_client_object["app_id"]

        except:
            print("Incorrect protocol. Unable to extract commands")

        if client_type == "robot":
            
            while True:
                    
                if q.qsize() > 0:
                    print("Queue size: {}".format(q.qsize()))

                while not q.empty():
                    
                    data_from_queue = q.get()

                    print ("Sending from queue: {}".format(data_from_queue))
                    vysl =data_from_queue.encode("utf8")  # encode the result string
                    conn.sendall(vysl)  # send it to client

        elif client_type == "controller":
            
            while command != "q":
                
                input_from_client = get_client_data() 
                input_from_client_object = parse_client_data(input_from_client)           

                try:
                    command = input_from_client_object['command']
                    client_type = input_from_client_object["client_type"]
                    packet_type = input_from_client_object["packet_type"]
                    app_id = input_from_client_object["app_id"]
                    
                except:
                    print("Incorrect protocol. Unable to extract commands")
                        
                #add to the queue
                if packet_type != "hello":
                    q.put(input_from_client)


        if command == "q":    

            print('Connection ' + ip + ':' + port + " sending OK and ending...")
            res = "ok"
            vysl = res.encode("utf8")  # encode the result string
            conn.sendall(vysl)  # send it to client
            conn.close()  # close connection
            print('Connection ' + ip + ':' + port + " ended")

                
            
        print("exiting...")

    except ConnectionResetError:
        print("Client sent reset. Exiting...")
      

def start_server():

    import socket
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this is for easy starting/killing the app
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')

    try:
        soc.bind(("127.0.0.1", 12345))
        print('Socket bind complete')
    except socket.error as msg:
        import sys
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    #Start listening on socket
    soc.listen(10)
    print('Socket now listening')

    # for handling task in separate jobs we need threading
    from threading import Thread

    # this will make an infinite loop needed for 
    # not reseting server for every client
    while True:
        conn, addr = soc.accept()
        ip, port = str(addr[0]), str(addr[1])
        print('Accepting connection from ' + ip + ':' + port)
        try:
            Thread(target=client_thread, args=(conn, ip, port)).start()
        except:
            print("Terible error!")
            import traceback
            traceback.print_exc()
    soc.close()


q = queue.Queue()   
start_server()

