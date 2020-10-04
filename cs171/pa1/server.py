import socket
from _thread import *
import threading 
import datetime
import sys

def inThread(connect, port):
	while True:
		data = connect.recv(2048).decode('utf-8') #recv the data sent from network process

		if data: #if some type of data is recv
			print("Time request received from: " + str(port))
			time = datetime.datetime.now() 
			print("Time:" + str(time))
			connect.sendall(str(time).encode('utf-8')) #send the current time to network process
			print("")
		
	connect.close()

def main():
	host = "127.0.0.1"
	port = 8889

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.bind((host, port)) #binds the server to a port and host ip
		print("Server created")
	except:
		print("Bind failed.")
		sys.exit()

	print("Server binded to port: " + str(port))
	s.listen(2) #listens to connections
	print("Server waiting...")

	while True:
		connect, addr = s.accept()
		ip, port = str(addr[0]), str(addr[1])
		print("Now connected with " + ip + ":" + port)		
		start_new_thread(inThread, (connect, port, )) #starts new thread per network process connection to recv independent delays per process

	s.close()

if __name__ == '__main__':
	main()
