import config
import serverY
import serverZ
import networkProcess

import socket
import threading 
import datetime
import sys
import random
import time
import queue
from _thread import *
 

total = 100

def replyThread(host, cPort, clientInput, connect,):	
	config.timestamp = config.timestamp + 1
	config.currentStamp = config.timestamp - 1
	request = connect.recv(2048).decode('utf-8')
	if clientInput[0] == 'b':
		serverLetter = 'y'
		procId = 2
	if clientInput[0] == 'c':
		serverLetter = 'z'
		procId = 3
	print("REQUEST <" + str(config.currentStamp) + ","+ str(procId) +"> received from server " + serverLetter + " (Logical time:"+ str(config.timestamp) +")")
	config.timestamp = config.timestamp + 1
	if request == "REQUEST":
		msg = "REPLY"
		print("REPLY for <" + str(config.currentStamp) + "," + str(procId) + "> sent to server "  + serverLetter + " (Logical time:"+ str(config.timestamp) +")")
		connect.sendall(msg.encode('utf-8'))
	release = connect.recv(2048).decode('utf-8')
	config.timestamp = config.timestamp + 2
	if release == "RELEASE":
		config.timestamp = config.timestamp + 3
		print("RELEASE for <" + str(config.currentStamp) + "," + str(procId) + "> received from server "  + serverLetter + " (Logical time:"+ str(config.timestamp) +")")

def requestThread(host, cPort,connect, ip, port, userInput, bPort,):
	global total
	config.currentStamp = config.timestamp + 1
	print("Transaction received from A (Logical time:" + str(config.timestamp) + ")")
	config.timestamp = config.timestamp + 1
	sc= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sc.connect((host, cPort)) #allows for the process to be connected to the network server in a thread
		print("connected")
	except:
		print("Connection failed.")
		sys.exit()	
	f = open("ledgerA", "a+")
	clientInput = userInput
	msg = str(bPort)
	print("REQUEST <" + str(config.currentStamp) + ",1> sent to all")
	sc.sendall(msg.encode('utf-8'))
	config.timestamp = config.timestamp + 2
	msg = sc.recv(2048).decode('utf-8')
	if msg == 'REPLY': #print reply recv mesgs btween timestamp++ statements
		config.timestamp = config.timestamp + 1
		print("REPLY to <"+ str(config.currentStamp) + ",1> received from server y (Logical time: " + str(config.timestamp) + ")")
		config.timestamp = config.timestamp + 1
		print("REPLY to <"+ str(config.currentStamp) + ",1> received from server z (Logical time: " + str(config.timestamp) + ")")
		config.timestamp = config.timestamp + 1
		print("Run critical section for <" + str(config.currentStamp) + ",1> (Logical time: " + str(config.timestamp) + ")")
		f.write(userInput)
		total = total + float(clientInput[4:])

	msg = "RELEASE" 
	config.timestamp = config.timestamp + 1
	sc.sendall(msg.encode('utf-8'))
	print("RELEASE for <" + str(config.currentStamp) + ",1> sent to all (Logical time: " + str(config.timestamp) + ")")
	connect.sendall(clientInput.encode('utf-8'))
	f.close
def main():
	host = "127.0.0.1"
	bPort = 9999 #client port
	cPort = 9998 #netProc port connect
	#sb = socket bind for clients; sc = socket connect for networkProc
	global total
	
	sb = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sb.bind((host, bPort))
		print("Binded + connected")
	except:
		print("Bind failed.")
		sys.exit()

	print("Server x started (Logical time:" + str(config.timestamp) + ")")
	
	while True:
		sb.listen() #enables connections; up to 2
		connect, addr = sb.accept() #init vars to the accepted connection
		ip, port = str(addr[0]), str(addr[1]) #splits connected addr into ip and port 
		userInput = connect.recv(2048).decode('utf-8')
		config.timestamp = config.timestamp + 1
		if len(userInput) > 0 :
			if userInput[0] == 'a':
				start_new_thread(requestThread, (host, cPort, connect, ip, port, userInput, bPort))
			if userInput == "REQUEST":
				config.timestamp = config.timestamp + 1
				userInput = connect.recv(2048).decode('utf-8')
				start_new_thread(replyThread, (host, cPort, userInput,connect,))
		else:
			start_new_thread(replyThread, (host, cPort, userInput,connect,))


	sb.close()
	sc.close()

if __name__ == '__main__':
	main()
