from socket import *
import time
import sys

#HOST = '10.0.0.2'
#PORT = 5599
BUFFER_Size = 1000

if(len(sys.argv) == 4):
	print("usage:", sys.argv[0], "<server hostname> <port> <time>");
else:
	print("Error: missing or additional arguments");
	sys.exit();

HOST = sys.argv[1]
PORT = int(sys.argv[2])
TIME = int(sys.argv[3])
testdata = '0'*BUFFER_Size
#print(PORT);
#print(type(sys.argv[3]));

if(PORT < 1024 or PORT > 65535):
	print("Error: port number must be in the range 1024 to 65535");
	sys.exit();

s = socket(AF_INET, SOCK_STREAM)
t_pre = time.time()
s.connect((HOST, PORT))
t1 = time.time()
print(t1)

timeout = t1 + TIME
sizeappend = 0
while time.time() < timeout:
        s.send(bytes(testdata , 'utf-8'))
        sizeappend += 1000
t_post = time.time()
#data = s.recv(2048)
s.close()
#print( "whole time frame with connect: ", (t_post - t_pre))
#print( "whole time frae without connec: ", (t_post - t1))
#print( "difference t1 and t_pre", (t1 - t_pre))
print( "sent=" , round(((sizeappend)/1024)/1024 * 1000) , "KB")
print( "rate=", ((sizeappend/TIME)*8)* 10**-6, "Mbps")
#print(data) 

"""
1 kilobyte (KB) = 1000 bytes (B)
1 megabyte (MB) = 1000 Kilobyte (KB)
1 Byte (B)      = 8 bits (b)
"""


"""
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

