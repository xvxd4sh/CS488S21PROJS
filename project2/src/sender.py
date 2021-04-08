# ----- sender.py ------

#!/usr/bin/env python
from socket import *
import socket
import sys
import os
import collections


s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
host = sys.argv[1]
port = int(sys.argv[2])
buf =1024
addr = (host,port)
s.setblocking(0)

packetdata = ""
packetsequence = "1203"
ackbuffer = []
count = 0
endflag = False
windowsize = 10
windowcount = 0
slidingwindow = collections.deque()
#command = "ping -qc3 " + host + " 2>&1 | awk -F\'/\' \'END{print(/^rtt/? \"\"$6\"\":\"1\")}\'"
#temp = os.popen(command).read()

#TimeOut_RTT = float(temp)

line = sys.stdin.readline()
while True:
	if not line:
		datagram = packetsequence + "END" + packetdata
#		datagram = packetsequence + line
		datagram = datagram.encode()
#		slidingwindow.append(line.strip())
		if(s.sendto(bytes(datagram),addr)):
			print("sending...")
#			print(datagram)
			windowcount = windowcount + 1
		try:
			s.settimeout(2)
			ACK, addrs = s.recvfrom(buf)
			ackdata = ACK.decode('utf-8')
			ackbuffer.append(ackdata)
#			print(ackbuffer)
			count = count + 1
		except socket.timeout:
			print("packet loss...retransmitting")
		break
	if((sys.getsizeof(packetdata)-1 + sys.getsizeof(line)) < buf):
#		data += line
		packetdata += str(line)
#		print(packetdata)
		line = sys.stdin.readline()
	else:
#		print(line)
#		print(packetdata)
		datagram = packetsequence + packetdata
		datagram = datagram.encode()
		if(s.sendto(bytes(datagram),addr)):
			print("sending...")
#			print(packetdata)
#		packetdata = ""
#		line = sys.stdin.readline()
#		packetdata = str(line)
#		print(packetdata)
		try:
			s.settimeout(2)
			ACK, addrs = s.recvfrom(buf)
			s.settimeout(None)
			ackdata = ACK.decode('utf-8')
			ackbuffer.append(ackdata)
#			print(ackbuffer)
			packetdata = ""
			if not line:
				break
#			print(count)
			count = count + 1
		except socket.timeout:
			print("packet loss...retransmitting")


#		if(s.sendto(bytes(data, 'utf-8'),addr)):
#			print("sending...")
#			print(datagram)
#		data = line
#		datagram = json.loads(datagram)
#		datagram["data"] = str(line)

s.close()

