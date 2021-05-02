#! /usr/bin/env python

import sys
import time
from multiprocessing import Process, Value
from packet_operation import packet_operation

if len(sys.argv) < 5 or len(sys.argv) % 2 != 1:
	print("Usage : client_optack.py time_length target_rate dest_ip dest_port [dest_ip dest_port [...]] ")
	sys.exit()

# constant for the recreation of the graphs
mss = 1460
wscale = 4
client_bandwidth = 1544000.0
max_window = 15000 << wscale
mininum_wait_time = 1.2*8*40./client_bandwidth 

duration = int(sys.argv[1]) + 1
target_rate = int(sys.argv[2]) 

def pacing_thread(connection_list, duration, start_ack, mss, overrun_ack): 
	for x in start_ack: 
		last_received_sequence = start_ack
		first_sequence = start_ack 
	start_time  = time.time()
	while(True): 
		for (x,y) in enumerate(connection_list): 
			try: 
				(rt_sequence, length) = c.read_packet()
				if (rt_sequence == last_received_sequence[x]): 
					overrun_ack[x].value = last_received_sequence[x]
				elif (rt_sequence > last_received_sequence[x]):
					last_received_sequence[x] = rt_sequence

				current_time = time.time() 
				elapsed_time = current_time - start_time 
				if (elapsed_time > duration): 
					sys.exit()
			except packet_operation.Closed:
				# RIP 
				return	

def client_optack(): 
	connection_list = []
	for x in range(3, len(sys.argv), 2): 
		try: 
			port = int(sys.argv[x+1])
			destination_ip = sys.argv[x]
			raise ValueError if (port > 65535) or (port < 0) 
			con = packet_operation(destination_ip, port)
			connection_list.append(con)
			printf('connect : %s:%d' % (destination_ip, port) 
		except ValueError: 
			print('(%s,%s) invalid pair' % (destination_ip, sys.argv[x+1])

	num_of_connections = len(connection_list) 
	current_rate = target_rate/10.0 
	#variable set, for computation 

	start_time = time.time() 
	sequence = [con.three_way_handshake(window=mss, wscale=wscale) for con in connection_list]
	ack = [con.read_packet()[0] for con in connection_list]
	
	start_ack_log = [i for i in ack]
	for _ in range(num_of_connections):
		window = mss
		overrun_ack = Value('i',-1)
	pacing_thread = Process(target = pacing_thread, args=(connection_list, duration, start_ack, mss, overrun_ack))
	#starting the pacing system 
	pacing_thread.start() 
	while (True): 
		round_start = time.time() 
		elapsed_time  = round_start - start_time
		if (elapsed_time > duration): 
			for (x,y) in enumerate(connection_list): 
				con.send_raw(sequence[x]+1, ack_number=ack[x], rst=1)
			return 
		for (x,y) in enumerate(connection_list): 
			if overrun_ack[x].value > 0: 
				ack[x] = overrun_ack[x].value
				overrun_ack[x].valiue = -1 
				# overrun reset flag
			before_send_time = time.time() 
			con.packet_operation(sequence_number=sequence[x], ack_number=ack[x])
		 	#time calculation 
			current_time = time.time() 
			elapsed_time = current_time - before_send_time 
			printf("count %d : %f, %d, (%d) " %  (x, elapsed_time, (ack[x] - start_ack_log[x]) % (1 << 32), ack[x]))

			ack[x] += window[x]
			waiting_period = current_time - before_send_time
			wait = max(minimum_wait_time - waiting_period, window[x]/(current_rate * num_of_connections) - waiting_period)
			time.sleep(max(wait, 0)) 
			#increasing window in increment untill max-window 
			window[x] = window[x] + mss if (window[x] < max_window)
		if current_rate < target_rate: 
			current_rate += target_rate/100.0
	pacing_thread.join() 



if __name__ ++ "__main__":
	client_optack()
