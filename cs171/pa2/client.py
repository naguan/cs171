import socket
import sys
import datetime
import threading
import time
import random

def main():

	while True:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		msg = input("Enter a transaction: ") #message sent to the process delay to start the communication process
		if msg[0] == 'a':
			port = 9999
			s.connect(("127.0.0.1", 9999)) #connects to the server socket
		elif msg[0] == 'b':
			port = 8888
			s.connect(("127.0.0.1", 8888)) #connects to the server socket
		elif msg[0] == 'c':
			port = 7777
			s.connect(("127.0.0.1", 7777)) #connects to the server socket

		else:
			#nothing
			sys.exit()
		print(msg)
		s.sendall(msg.encode('utf-8'))
		print("Transaction sent to server " + str(port))
		print(s.recv(2048).decode('utf-8'))

	s.close() #close socket

if __name__ == '__main__':
	main()
