# client.py

import socket
import json
from modules.vehicle import Vehicle


client_type = "robot"
packet_type = "hello"
app_id = "123adalsdjfhaldfjkahl234234234"
command = ""


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
soc.connect(("192.168.1.143", 12345))

packet_string = '{\"packet_type\":' + '\"' + packet_type + '\"' \
        + ',\"app_id\":' + '\"' + app_id + '\"' \
        + ',\"client_type\":' + '\"' + client_type + '\"' \
        + ',\"command\":' + '\"' + command + '\"}'
print ("Sending {}".format(packet_string))
soc.send(packet_string.encode("utf8")) # we must encode the string to bytes  

result_bytes = soc.recv(4096) # the number means how the response can be in bytes  
result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode
print("Result from server is {}".format(result_string))  

packet_type = "normal"

vehicle = Vehicle()
vehicle.start()

    
while True:
    
    result_bytes = soc.recv(4096) # the number means how the response can be in bytes  
    result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode
    print("Result from server is {}".format(result_string))  

    try:
        server_object = json.loads(result_string)
        command = server_object['command']
        vehicle.COMMAND = command

    finally:
        pass

    if command == "q":
        soc.close()
        break