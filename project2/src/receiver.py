# ----- receiver.py -----

#!/usr/bin/env python

from socket import *
import sys
import select

host="10.0.0.1"
port = int(sys.argv[1])
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf=1024

f = open("RECEIVED_FILE",'wb')

data,addr = s.recvfrom(buf)
try:
    while(data):
        f.write(data)
        s.settimeout(2)
        data,addr = s.recvfrom(buf)
except timeout:
    f.close()
    s.close()
    print("File Downloaded")
