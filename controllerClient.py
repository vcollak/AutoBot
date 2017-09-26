# client.py

import socket
import json


client_type = "controller"
packet_type = "hello"
app_id = "123adalsdjfhaldfjkahl234234234"
command = ""


soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
soc.connect(("127.0.0.1", 12345))

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

while True:


    command = input("What you want to proceed my dear client?\n") 
    packet_string = '{\"packet_type\":' + '\"' + packet_type + '\"' \
        + ',\"app_id\":' + '\"' + app_id + '\"' \
        + ',\"client_type\":' + '\"' + client_type + '\"' \
        + ',\"command\":' + '\"' + command + '\"}'
    print ("Sending {}".format(packet_string))
    soc.send(packet_string.encode("utf8")) # we must encode the string to bytes  
    result_bytes = soc.recv(4096) # the number means how the response can be in bytes  
    result_string = result_bytes.decode("utf8") # the return will be in bytes, so decode
    print("Result from server is {}".format(result_string))  

    if command == "q":
        soc.close()
        break