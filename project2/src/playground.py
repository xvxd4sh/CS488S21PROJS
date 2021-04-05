#!/usr/bin/env python 

import json 
import subprocess 
import os
from socket import * 
import socket
import time
import select
import sys

def make_packet(data): 
	temp_packet = {"data": data}
	return temp_packet	

	
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "10.0.0.1"
port= 5599 
buf = 1024 
addr = (host, port) 

#packet_buffer = []*2
ackdata = []

s.setblocking(0)
count = 1 

data = sys.stdin.readline() 
data = data.strip()
packet = make_packet(data) 
while (data):
#	print("packet"+ str(count+1)) 
#	s.sendto(testdata[count].encode(),addr) 
#	print( "ackdata " + str(ackdata)) 
#	print (" sending out packet " + str(count)) 
#	s.settimeout(1) 
#	try: 
#		ACK, addrs = s.recvfrom(buf) 
#		ackdata[count] = "ack for " + str(count) + " recvd"
#		print ("ackdata after ack " + str(ackdata))
#		count = count +1 
#	except socket.timeout: 
#		print("packetlost ... retransmitting")
	packet = json.dumps(packet)
	s.sendto(bytes(packet),addr) 
	s.settimeout(1)
	try: 
#		s.sendto(bytes(packet),addr) 
#		s.settimeout(1)
		ACK, addrs = s.recvfrom(buf)
		tempack = ACK.decode('utf-8') 
		print(tempack)
		ackdata.append("ack for" + str(count) + " recvd") 
		print("ackdata after ack" + str(ackdata))
		data = sys.stdin.readline()
		data = data.strip() 
		if not data: 
			break
		packet = make_packet(data)  
		count = count + 1
	except socket.timeout: 
		print("packet lost ... retransmiting")

	
print(ackdata)
print("done")
s.close()
