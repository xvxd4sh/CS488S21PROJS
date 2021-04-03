#!/usr/bin/env python 

import json 
import subprocess 
import os 
from socket import * 


s = socket(AF_INET, SOCK_DGRAM)
host = "10.0.0.1"
port= 5599 
buf = 1024 
addr = (host, port) 

 
testdata=["1000","2000","3000","4000","5000","6000","7000","8000","9000","10000"
	 ,"11000" ,"12000","13000","14000","15000","16000","17000","18000","19000"
	 ,"20000"]

ackdata = ['']*20

for count, data in enumerate(testdata):
	while (ackdata[count] == ''):
		s.sendto(testdata[count].encode(),addr)
		print("sending .." + testdata[count])  
		ACK, address = s.recvfrom(1024) 
		if(ACK != ''): 
			print("getting ack") 
			ackdata[count] = "ack" + str(count+1) +  "recv"
		else: 
			print("waiting")
		
	
print(ackdata)
print("done")
s.close()	
