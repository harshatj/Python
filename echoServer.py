#!/usr/bin/python

import sys, getopt
import socket
from thread import *

helpmsg = '''
OPTIONS:
-c		Continuous echo mode.
-h		Display the available options
-ip IPADD	Specify the server IP Address
-t TCP/UDP	Specify the transport layer protocol.
-v		Print the software version
''';
version = 'version1.0'
HOST = '127.0.0.1'
protocol = 'TCP'
continouos = False 
PORT = 4002
debug = 0

def main(argv):
	inputfile = ''
	outputfile = ''
	global protocol
	global HOST
	
	try:
		opts, args = getopt.getopt(argv,"hvct:ip:",["ifile=","ofile=","ip="])
	except getopt.GetoptError:
		print sys.argv[0]+' opcion no reconocida'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print helpmsg
			sys.exit()
		elif opt == "-v":
			print  sys.argv[0]+" "+version
			sys.exit()
		elif opt == "-c":
			continouos = True
			print  "continouos "
		elif opt in ("-t"):
			protocol = arg
			if protocol == "TCP":
				print "protocolo "+arg
			elif protocol == "UDP":
				print "protocolo "+arg
			else:
				print "Wrong Protocol "+arg
				sys.exit()
		elif opt in ("-ip", "--ip", "ip"):
			HOST = arg
			print  HOST+" "+version

# 
# This Function handles connections. This will be used to create threads
def clientthread(conn):
    #This function Sends message to connected client
    #conn.send('Welcome to the server course EE544 Fall 2014. Type something and hit enter\n') #send only takes string
     
    #We enter an infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client up to 1024 bytes
        data = conn.recv(1024)
        reply = data
        if not data: 
            break
     
        conn.sendall(reply)
     
    #came out of loop
    conn.close()
	
################
def udpServer():
	global HOST
	global PORT
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print 'UDP Socket bind complete'
	
	#Bind socket to local host and port
	try:
		s.bind((HOST, PORT))
	except socket.error as msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	print 'Socket bind complete'
	
	#now keep talking with the client
	while 1:
		#wait to accept a connection - blocking call
		conn, addr = s.recvfrom(1024)
		s.sendto(conn, addr)
	s.close()
################
def tcpServer():
	global HOST
	global PORT
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'TCP Socket bind complete'
	
	#Bind socket to local host and port
	try:
		s.bind((HOST, PORT))
	except socket.error as msg:
		print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	
	print 'Socket bind complete'
	
	s.listen(10)
	print 'Socket now listening'
	
	#now keep talking with the client
	while 1:
		#wait to accept a connection - blocking call
		conn, addr = s.accept()
		print 'Connected with ' + addr[0] + ':' + str(addr[1])
		
		#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
		start_new_thread(clientthread ,(conn,))
	s.close()
		
################

if __name__ == "__main__":
	main(sys.argv[1:])

if protocol == "TCP":
	tcpServer()
elif protocol == "UDP":
	udpServer()

