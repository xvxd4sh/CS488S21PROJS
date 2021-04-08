# ----- receiver.py -----

#!/usr/bin/env python

from socket import *
import sys
import select
import json

def parse_list(list):
	for value in list:
		print(value)

host="0.0.0.0"
port = int(sys.argv[1])
s = socket(AF_INET,SOCK_DGRAM)
s.bind((host,port))

addr = (host,port)
buf = 1024

data,addr = s.recvfrom(buf)
resultlist = []
count = -1
endflag = False

try:
	while(data):
		result = data.decode('utf-8')
		if(result[4:7] == "END"):
			packetdata = result[7:-1]
			packetsegment = result[0:4]
			endflag = True
		else:
			packetdata = result[4:-1]
#			print(packetdata)
			packetsegment = result[0:4]
		resultlist.append(packetdata)
		count = count+1
		ack = packetsegment + "added"
		s.sendto(ack.encode(), addr)
		if(len(resultlist) >=  2):
			if(resultlist[count] == resultlist[count-1]):
				resultlist.pop()
				count = count - 1
		if(len(resultlist) == 100):
			parse_list(resultlist)
			resultlist = []
			count = -1
#		result = json.loads(result)
#		print(result.strip("\n"))
#		print((result["data"]).trip("\n"))
		s.settimeout(5)
		if(endflag == True):
			break
		data,addr = s.recvfrom(buf)
		s.settimeout(None)
except timeout:
	s.close()
	parse_list(resultlist)



s.close()
parse_list(resultlist)
