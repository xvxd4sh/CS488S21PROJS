from socket import *
import select 
import json

buf = 1024  
host = "10.0.0.1" 
port= 5599 


s = socket(AF_INET,SOCK_DGRAM) 
s.bind((host,port)) 



data, addr = s.recvfrom(buf) 
result = ""
resultlist=[]
count = -1
try: 
	while(data): 
		result = data.decode('utf-8')
#		print(type(result)) 
		result = json.loads(result)
#		print(result) 
#		print(type(result))
#		resultdumped = json.dumps(result)
		resultlist.append(result)
		count = count + 1
		ack = "acknowledge "+ str(result)
		s.sendto(ack.encode(),addr)
		if not data: 
			break
		s.settimeout(2)
		if(count>=3 ): 
			resultlistjson = resultlist[count-1] 
			print(type(resultlistjson))
			print(resultlistjson['data'])
			if(resultlistjson['data'] == result['data']): 
				resultlist.pop()
		data,addr = s.recvfrom(buf) 
		print(resultlist) 
	print(resultlist)
	print("hello") 		
except timeout: 
	s.close()
	
print(resultlist)
