#!/usr/bin/env python 

import sys 

X_AXIS_VALUE = 29 

totals = [0]*X_AXIS_VALUE 

for fname in sys.argv[1:]:
	i = 0
	with open(fname) as f: 
		for line in f: 
			if i >= X_AXIS_VALUE: break
			timestamp, bytes = line.split(',')
			if (float(time) > i): 
				if (float(time) < i +1): 
				 	totals[i] += int(bytes) 
				i += 1

for i in range (1, X_AXIS_VALUE): 
	print ("%d, %d" % (i, totals[i] - totals[i-1]))
			
