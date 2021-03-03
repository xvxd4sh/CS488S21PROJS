#!/usr/bin/enc python3

import sys 
import socket
import selectors
import types 
import time

if len(sys.argv) != 4: 
    print("usage:", sys.argv[0], "<server hostname> <port> <Time>")

buff = 1024 
packet_count = 0 

Time = sys.argv[3]
port = sys.argv[2]
host = sys.argv[1]

testdata = 'x'*(buff-1) + '\n'

# make the TCP socket 
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#connecting to listening server
server_add = (host, port)
sock.connect(server_add)
print("connecting to", host, "at port: ", port)

timeout = time.time() + Time
while time.time() < timeout:
    sock.sendall(testdata)
    recieved = sock.recv(buff)
    print (recieved)

sock.close()
"""
To measure bandwidth we need to find the maximum number of bits we can pass 
we use the time in seconds and then devide the amount of bits that we were 
able to send and then divide by the time (while the loop is happening, it counts 
the amount of packets that passes and multiply with buffer size at the end)

throughput(which is the amount of data passing thorugh a system)/time 
(howmany*Buffersize)/seconds 

while loop based on time idea 

timeout = time.time() + <amount of seconds> 
while time.time() < timeout:
        do action 

"""
