import socket 
import sys
import datetime
import threading
import time
import random 



def main():
	newTime = datetime.datetime.now()
	timeAtRec = datetime.datetime.now()
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = "127.0.0.1"
	port = 9999
	try:
		s.connect((host, port)) #connects to the newtwork process socket
		print("Connected to Network Process")
	except: 
		print("Could not connect")
		sys.exit() #exits when connection cannot be made
	rho = 0.5 #drift time; cannot be float b/c python2.7 does not support float * timedate; use python3.0
	delta = 10 #resync time
	timedMsg = delta/(2*rho) #delay

	while True:
		msg = "time" #message sent to the process delay to start the communication process
		t1 = newTime + ((datetime.datetime.now() - timeAtRec) * (1 + rho)) #init time at time of send
		s.sendall(msg.encode('utf-8'))
		tutc = s.recv(2048).decode('utf-8')
		t2 = newTime + ((datetime.datetime.now() - timeAtRec) *  (1 + rho)) #init time at time of recv
		timeAtRec = datetime.datetime.now() #time at sync
		newTime = datetime.datetime.strptime(tutc, '%Y-%m-%d %H:%M:%S.%f') + ((t2-t1)/2) #new synced time

		print("T1: " + str(t1))
		print("Tutc: " + str(tutc))
		print("T2:  "+ str(t2))
		print("T': " + str(newTime))
		time.sleep(timedMsg) #waits delta/(2*rho) seconds before sending the next time request
		print("") #newline to make reading easier

	s.close() #close socket
 
if __name__ == '__main__':
	main()
