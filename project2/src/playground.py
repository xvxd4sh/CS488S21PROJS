#!/usr/bin/env python 

import json 
import subprocess 
import os
from socket import * 
import socket
import time
import select

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = "10.0.0.1"
port= 5599 
buf = 1024 
addr = (host, port) 
strACK = ''
testdata=["1000","2000","3000","4000","5000","6000","7000","8000","9000","10000"
	 ,"11000" ,"12000","13000","14000","15000","16000","17000","18000","19000"
	 ,"20000"]

ackdata = ['']*20
#print(ackdata)
#for data in testdata:
#	count = 0
	#print(data)
#	if (ackdata[count] != ''):
#		ticks = time.time()
#		s.sendto(testdata[count].encode(),addr)
#		print("sending .." + testdata[count]) 
#		ACK, address = s.recvfrom(buf) 
#		postticks = time.time()
#		strACK = ACK.decode()
#		if(strACK != ''): 
#			print(strACK)
#			print("getting ack") 
#			ackdata[count] = "ack" + str(count+1) +  "recv"
#			count = count + 1
#		elif(postticks - ticks > 10): 
#			count = count - 1
#			print("waiting")
#
#count =1 
#s.setblocking(0) 
#while(testdata[count-1] != ''):
#	print(count)
#	print(ackdata[count-1])  
##	if (ackdata[count] == ''):
		#ticksout = time.time() + .1
		#print(ticksout) 
#	s.sendto(testdata[count-1].encode(),addr)
#	print("ackdata " + str(ackdata)) 
#	print("sending out ... " + str(count)) 
	#while (time.time() < ticksout):
#	print("starting process") 
#	s.settimeout(1)
#	try: 
#		ACK, address = s.recvfrom(buf)
#		print ("got ack")
#		ackdata[count-1] = "ack" + str(count) + "rexc"
#		print ("ackdata " + str(ackdata))
#		count = count + 1
#		#s.settimeout(None)
#	except socket.timeout: 
#		#count = count - 1
#		print("packet lost .. retransmitting ")
#		if(ACK != ''): 
#			print("getting ack") 
#			ackdata[count] = "ack " + str(count+1) + " recx"
#			getACK = True
#			count = count + 1 
#			break
#		if((time.time() >= ticksout) and getACK == False): 
#			count = count - 1 
#			print("waiting .. ")
#	if(count == 21): 
#		break


s.setblocking(0)
count = 0 
while (count < 20):
	print("packet"+ str(count+1)) 
	s.sendto(testdata[count].encode(),addr) 
	print( "ackdata " + str(ackdata)) 
	print (" sending out packet " + str(count)) 
	s.settimeout(1) 
	try: 
		ACK, addrs = s.recvfrom(buf) 
		ackdata[count] = "ack for " + str(count) + " recvd"
		print ("ackdata after ack " + str(ackdata))
		count = count +1 
	except socket.timeout: 
		print("packetlost ... retransmitting") 

print(ackdata)
print("done")
s.close()
