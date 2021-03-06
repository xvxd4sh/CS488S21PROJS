#!/usr/bin/env python 

from mininet.topo import Topo 
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net  import Mininet

from argparse import ArgumentParser

import sys
import os
import math

PORT = 5002
def parse_args():
	parser = ArgumentParser(description="OPT-ACK attack") 	
	parser.add_argument('--bw_server', '-B', type=float,
			help=" Bandwidth of servers (Mb/s)", default=100.)
	parser.add_argument('--delay', type=float, help="Link propagration delay (ms)", default=10.) 
	parser.add_argument('--dir', '-d', help= "output directory", required=True) 
	parser.add_argument('--time','-t',type=int, help= "length of experiment(s)", default=20) 
	parser.add_argument('--server_count', '-n',type=int, help="Number of server spawn", default=1)
	parser.add_argument('--target_rate', '-r', type=float,
		 help="Target bandwidth for the client to keep (Mb/s)", default=80.) 

	args = parser.parse_args(); 
	args.target_rate *= (1000000.0/8.0)
	#argument is the parameter for each experimentation. converted to B/s instead of Mb/s
	return args

class BBTopo(Topo): 
	# one router, one client, and n servers 

	def build(self, n=1): 
		switch = self.addSwitch('s0')
		h0 = self.addHost('h0')
		self.addLink(h0, switch, bw=1.544, delay="%fms" % args.delay,max_queue_size=1000) 
		
		for i in range(1, n+1):
			server = self.addHost('server%d' % i)
			self.addLink(server, switch, bw=args.bw_server, delay="%fms" % args.delay, max_queue_size=1000)
		return

 
def test_attack(args): 
	topo = BBTopo(n=args.server_count)
	net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink, autoStaticArp=True) 
	net.start()
	server_id = "" 
	for i in range(1, args.server_count+1):
  		server = net.get('server%d' % i)
  		#starting each server using its corresponding ID 
  		#server.open deternmines what theyre running
  		server.popen("python server.py -p %d --duration %d --dir %s -i %s" % (PORT, args.time, args.dir, server.IP()), shell=True)
		server_id += "%s %d " % (server.IP(), PORT)

	h0 = net.get('h0') 
	h0.popen("iptables -t filter -I OUTPUT -p tcp --dport %d --tcp-flags RST RST -j DROP" % PORT)
	# after countless hours, RST was an issue that need suppressing 
	h0.popen("python client_optack.py %d %d %s > /dev/null 2> /dev/null" % (args.time, args.target_rate, server_id), shell=True).wait()


	net.stop()

if __name__ == "__main__": 
	args = parse_args()
	test_attack(args) 
	
