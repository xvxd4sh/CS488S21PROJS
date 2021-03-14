from socket import *
import time
import sys

if(int(sys.argv[2]) < 1024 or int(sys.argv[2]) > 65535):
	print("Error: port number must be in the range 1024 to 65535")
	sys.exit()
elif(len(sys.argv) == 4):
        print("usage:", sys.argv[0], "<server hostname> <port> <time>")
else:
        print("Error: missing or additional arguments")
        sys.exit()


HOST = sys.argv[1]
PORT = int(sys.argv[2])
TIME = int(sys.argv[3])
BUFFER_Size = 1000
testdata = '0'*BUFFER_Size

s = socket(AF_INET, SOCK_STREAM)
s.connect((HOST, PORT))
t1 = time.time()

timeout = t1 + TIME
sizeappend = 0
while time.time() < timeout:
        s.send(bytes(testdata , 'utf-8'))
        sizeappend += 1000
t_post = time.time()
#data = s.recv(2048)
s.close()
Transfersize = round((((sizeappend)/1024)/1024) * 1000)
Bandwidth =  round((((sizeappend/TIME)*8)*(10**-6)), 3)
print( "sent={} KB ".format(Transfersize), "rate={} Mbps".format(Bandwidth))


"""
NOTES

1 kilobyte (KB) = 1000 bytes (B)
1 megabyte (MB) = 1000 Kilobyte (KB)
1 Byte (B)      = 8 bits (b)

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

