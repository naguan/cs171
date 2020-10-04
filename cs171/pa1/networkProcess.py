import socket
import threading 
import datetime
import sys
import random
import time
from _thread import *

def inThread(host, cPort,connect, ip, port):
	sc= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sc.connect((host, cPort)) #allows for the process to be connected to the server in a thread
		print("Network Process created")
	except:
		print("Connection failed.")
		sys.exit()
	print("Network Process connected to server: " + str(cPort))


	while True:
		data = connect.recv(1024).decode('utf-8') #recv from client
		d1 = random.randint(1,5) #produces the first random delay
		d2 = random.randint(1,5) #produces the second random delay
		print("Time request received by: " + str(ip) + ":" + str(port))	 	
		print("Delay: " + str(d1))
		print("Delay: " + str(d2))
		print("")
		if data: #if any type of data is received
			time.sleep(d1) #delay the time by d1
			d1 = str(d1) #converts the int to str
			sc.sendall(d1.encode('utf-8')) #send to server
		data = sc.recv(2048).decode('utf-8') #recv from server

		time.sleep(d2) #delay the time by d2
		connect.sendall(data.encode('utf-8')) #sends the received time from the server
		
	#close all opened sockets	
	connect.close()	
	sc.close()
	sb.close()

def main():
	host = "127.0.0.1"
	bPort = 9999 #client port
	cPort = 8889 #server port
	#sb = socket bind for clients; sc = socket connect for server
	
	sb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sb.bind((host, bPort))
	except:
		print("Bind failed. ")
		sys.exit()
	print("Network Process binded to port: " + str(bPort))

	while True:
		sb.listen(2) #enables connections; up to 2
		connect, addr = sb.accept() #init vars to the accepted connection
		ip, port = str(addr[0]), str(addr[1]) #splits connected addr into ip and port 
		print("Now connected with client: " + ip + ":" + port)
		sc= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		start_new_thread(inThread, (host, cPort, connect, ip, port)) #starts new thread per connection to the network pro

if __name__ == '__main__':
	main()
	
