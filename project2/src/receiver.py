# ----- receiver.py -----

#!/usr/bin/env python

from socket import *
import sys
import select

host="0.0.0.0"
port = int(sys.argv[1])
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf = 1024
#f = open("RECEIVED_FILE",'wb')

data,addr = s.recvfrom(buf)
result = ""
try:
	while(data):
		result = data.decode('utf-8')
		#print(type(result))
		print(result.strip("\n"))
		#f.write(data)
		s.settimeout(2)
		data,addr = s.recvfrom(buf)
except timeout:
	#f.close()
	s.close()
