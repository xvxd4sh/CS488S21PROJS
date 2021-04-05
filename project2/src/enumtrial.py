#!/usr/bin/env python 
import sys 

line_buffer= []*2
line = sys.stdin.readline()
line_buffer.append(line)
line2 = sys.stdin.readline()
line_buffer.append(line2)
print(line_buffer)
enflag = False
while line: 
	print(line_buffer)
	print(line_buffer[0])
	line = sys.stdin.readline()
	if line_buffer[1] == "\n": 
		print("no next") 
	line_buffer.append(line)
	line_buffer.pop(0)

 
	
