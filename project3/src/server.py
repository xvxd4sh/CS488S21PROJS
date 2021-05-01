#!/usr/bin/env python2

import socket
import time
import sys
import struct
import os
from argparse import ArgumentParser

def parse_args():
	parser = ArgumentParser(description="server side")
	parser.add_argument("--port", "-p", type=int, help="Port number", default=5002)
	parser.add_argument("--ipaddr", "-i", type=str, help="IP address", default="localhost")
	parser.add_argument("--duration", "-d", type=int, help="Time after stream ends", default=-1)
	parser.add_argument("--dir", type=str, help="save result into directory", default=None)

	return parser.parse_args()


def server(address, port, dir, duration):
	#We create the server using socket programming
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.settimeout(10)
	if dir is not None: 
		try: 
			os.makedirs(dir) 
		except OSError: 
			pass 
	s.bind((address,port))
	s.listen(10)
	c, addr = s.accept()
	start_time = time.time()

	datagram_update = 0
	directory = open(dir+"/%s.csv" % address, 'w+') if dir is not None else sys.stdout
	while True:
		current_time = time.time()
		elapsed = current_time - start_time
		if duration > 0 and elapsed >= duration:
			break
		try:
			c.send("0"*20000)
		except:
			break
		
		datagram_update += 20000
		directory.write(elapsed +", "+ datagram_update + "\n")
	c.close()
	s.close()
	if directory is not sys.stdout:
		directory.close()

if __name__ == "__main__":
	args = parse_args()
	server(args.ipaddr, args.port, args.dir, args.duration)
