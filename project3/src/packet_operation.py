import socket
import sys
import random
from struct import *

class packet_operation:
	s = None
	source = None
	destination = None
	flag = -1
	#Creating variables to be used later on

	def __init__(self, address, port):
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
			self.s.settimeout(10)
			self.destination = (address, port)
			self.source = socket.s.getsockname()
			self.s.connect(socket.destination)
		except socket.error:
			print("Error")
			sys.exit()

	def checksum(string):
		x = 0
		for y in range(0, len(string)):
			z = ord(string[y]) + ord(string[y + 1])
			x += z

		return x

	def packet_creation(self, sequence, ack = -1, string = "", fin = 0, syn = 0, rst = 0, window=5820, wscale = 0):
		if ack == -1
			ack = 0
			ack_sequence = 0
		else:
			ack = 1
			ack_sequence = ack


		source_address, source_port = self.source
		destination_address, destination_port = self.destination
		#this was too get the address and port from socket, now we will construct using similar
		#variables

		src_address = source_address
		dest_address = destination_address
		datagram = string
        	tcp_source = source_port
        	tcp_destination = destination_port
        	tcp_sequence = sequence % (1<<32)
        	tcp_ack_seq = ack
        	#flags
        	tcp_fin = fin
        	tcp_syn = syn
        	tcp_rst = rst
        	tcp_psh = 0
        	tcp_ack = ack
        	tcp_urg = 0
        	tcp_window = socket.htons (window)
        	tcp_check = 0
        	tcp_urg_ptr = 0

        	tcp_flags = tcp_fin + (tcp_syn << 1) + (tcp_rst << 2) + (tcp_psh <<3) + (tcp_ack << 4) + (tcp$

        	tcp_wscale_kind = 3
        	tcp_wscale_len = 3
        	tcp_wscale_shift = wscale
        	tcp_wscale = (tcp_wscale_shift << 8) + (tcp_wscale_len << 16) + (tcp_wscale_kind << 24)

	        if tcp_syn == 1:
	                tcp_off = 6
        	        tcp_offset_res = (tcp_off << 4) + 0
        	        tcp_header = pack('!hhllbbhhhl' , tcp_source, tcp_dest, tcp_seq, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr, tcp_wscale)
        	else:
        	        tcp_off = 5
        	        tcp_offset_res = (tcp_off << 4) + 0
        	        tcp_header = pack('!hhllbbhhh' , tcp_source, tcp_destination, tcp_sequence, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window, tcp_check, tcp_urg_ptr)
	

	        source_addr = socket.inet_aton( src_address )
	        destination_addr = socket.inet_aton(dest_address)
	        protocol = socket.IPPROTO_TCP
	        tcp_length = len(tcp_header) + len(datagram)
		a = 0
	        tcp_psh = pack('!4s4sBBH' , source_addr , destination_addr , a , protocol , tcp_length)
	        tcp_psh = tcp_psh + tcp_header + datagram
	
	        tcp_checksum = checksum(tcp_psh)
	
	        if tcp_syn == 1:
	                tcp_header = pack('!hhllbbh' , tcp_source, tcp_destination, tcp_sequence, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window) + pack('H', tcp_check) + pack('!HL', tcp_urg_ptr, tcp_wscale)
	        else:
	                tcp_header = pack('!hhllbbh' , tcp_source, tcp_destination, tcp_sequence, tcp_ack_seq, tcp_offset_res, tcp_flags, tcp_window) + pack('h', tcp_checksum) + pack('!h', tcp_urg_ptr)$

	        packet = tcp_header + datagram

	        self.s.sendto(packet, (dest_ip , 0 ))    

		if self.fin != -1:
			raise self.Closed
		elif ack == self.fin:
			return False

		return True


	def three_way_handshake(self, string="Get / HTTP/1.0\r\n\r\n", window=5840, wscale=0):
		number = random.Random()
		sequence_number = number.randint(0, 1<<32-1)
		self.packet_creation(sequence_number, syn = 1, window = window, wscale = wscale)
		sequence,_ = self.read_packet()
		sequence_number += 1
		self.packet_creation(sequence_number, ack = sequence+1)
		self.packet_creation(sequence_number, ack = sequence+1, string=string)
		return sequence_number + len(string)


	def read_packet(self, buffer = 65535):
		while True:
			packet = self.s.recvfrom(buffer)
			(sequence_number, string) = self.parse(packet[0])
			return (sequence_number, string)

	def parse(self, packet):
		# Code from http://www.binarytides.com/python-packet-sniffer-code-linux/
		# Code from Alexander Schuab<axschaub@stanford.edu>
	        """
	        Takes a packet as input. Returns the sequence number and the payload size
	        of the packet if it corresponds to a packet from the expected flow, or (-1, -1) otherwise
	        """
	        ip_header = packet[0:20]
	
	        #now unpack them :)
	        iph = unpack('!BBHHHBBH4s4s' , ip_header)
	
	        version_ihl = iph[0]
	        version = version_ihl >> 4
	        ihl = version_ihl & 0xF
	
	        iph_length = ihl * 4
	
	        tcp_header = packet[iph_length:iph_length+20]
	
	        #now unpack them :)
	        tcph = unpack('!HHLLBBHHH' , tcp_header)
	
	        source_port = tcph[0]
	        dest_port = tcph[1]
	        sequence = tcph[2]
	        #acknowledgement = tcph[3]
	        doff_reserved = tcph[4]
	        tcph_length = doff_reserved >> 4
	
	        fin_flag = (tcph[5] & 0x1) != 0
	        rst_flag = (tcph[5] & 0x4) != 0
	
	        #print "Src port : %d, Dest port : %s, sequence : %d" % (source_port, dest_port, sequence)
	
	        expected_dest = self.src_addr[1]
	        expected_src = self.dest_addr[1]
	
	        if expected_src != source_port or expected_dest != expected_dest:
	        	return (-1,-1) # we could also throw an exception, but it might slow us down
	
	        h_size = iph_length + tcph_length * 4
	        data_size = len(packet) - h_size
	        if fin_flag:
	        	# On receiving a FIN, send an ACK for the last received packet number + 1
	        	data_size += 1
			self.fin = sequence+data_size
        	if rst_flag:
            		raise self.Closed

        	return (sequence, data_size)


	def shutdown(self, sequence):
		self.packet_creation(sequence, fin = 1, ack = self.fin)
		self.fin = -1
		temp_ack = self.read_packet()
		self.packet_creation(sequence+1, ack = self.fin, rst = 1)

	class Closed(Exception):
		pass
